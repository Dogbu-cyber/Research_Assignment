from sec_edgar_downloader import Downloader
import os
from bs4 import BeautifulSoup
import re

# Dictionary to map ticker symbols to company names
ticker_to_name = {"AAPL": "Apple", "MSFT": "Microsoft"}

# Start and end dates for downloading 10-K filings
start = "1995-01-01"
end = "2023-12-31"

def download_10K(ticker):
    """
    Downloads 10-K filings for a given ticker symbol.

    Parameters:
    ticker (str): The ticker symbol of the company.

    Returns:
    None
    """
    name = ticker_to_name[ticker]
    print(f"Downloading 10-K for {ticker}")
    dl = Downloader(company_name=None, email_address=None, download_folder=f"{name}")
    dl.get("10-K", ticker, after=start, before=end, download_details=True)
    print("DONE :)")

def extract_item_8(company_path):
    """
    Extracts the ITEM 8 section from 10-K filings.

    Parameters:
    company_path (str): The path to the directory containing the company's 10-K filings.

    Returns:
    None
    """
    # Defining the regex pattern to capture text between "ITEM 8" and "ITEM 9A"
    pattern = r"(?s)\bITEM\s*(&nbsp;)?8\.? .*?(?=\bITEM\s*(&nbsp;)?9\.?)"

    company_name = company_path.split('/')[0]

    for year_folder in os.listdir(company_path):
        year = year_folder.split('-')[1]
        file_path = os.path.join(company_path, year_folder, 'full-submission.txt')

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                text = file.read()
                # Search the document for ITEM 8 to ITEM 9A sections
                matches = re.finditer(pattern, text, re.IGNORECASE)

                for match in matches:
                    section = match.group(0)
                    # Check if the section contains "net income" and "operating income" keywords
                    if all(keyword.lower() in section.lower() for keyword in ["net income", "operating income"]):
                        print(f"ITEM 8 section found in {company_name} for year {year}:")
                        soup = BeautifulSoup(section, 'html.parser')
                        section_text = soup.get_text()
                        section_text = re.sub(r'\s+', ' ', section_text)
                        section_file_path = os.path.join(company_path, year_folder, 'section 8 Text.txt')
                        with open(section_file_path, 'w', encoding='utf-8') as section_file:
                            section_file.write(section_text)

# Download 10-K filings and extract ITEM 8 section for each ticker symbol
for ticker in ticker_to_name:
    path = f"{ticker_to_name[ticker]}/sec-edgar-filings/{ticker}/10-K"
    download_10K(ticker)
    extract_item_8(path)