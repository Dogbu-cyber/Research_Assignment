import os
from dash import dcc
import plotly.graph_objects as go

# Dictionaries mapping int: year to tuple: (net_income, operating_income, summary)
msft_year_to_data ={} 
aapl_year_to_data ={} 
import re

def extract_data(text):
    """
    Extracts net income, operating income, and summary from the given text.

    Parameters:
    text (str): The text to extract data from.

    Returns:
    tuple: A tuple containing net income, operating income, and summary.
    """
    # Regular expressions to match net income, operating income, and summary
    net_income_match = re.search(r'Net Income: -?(\$[\d,]+)', text, re.IGNORECASE)
    operating_income_match = re.search(r'Operating Income: -?(\$[\d,]+)', text, re.IGNORECASE)
    summary_match = re.search(r'summary:(.*)', text, re.IGNORECASE | re.DOTALL)

    # Extract and clean the matched data
    net_income = int(net_income_match.group(0).replace(',', '').replace('$', '').replace('Net Income: ', ''))
    operating_income = int(operating_income_match.group(0).replace(',', '').replace('$', '').replace('Operating Income: ', '')) 
    summary = summary_match.group(1).strip() if summary_match else None

    return (net_income, operating_income, summary)

def populate_dicts(company_path):
    """
    Populates dictionaries with data extracted from insights files.

    Parameters:
    company_path (str): The path to the directory containing the company's insights files.

    Returns:
    None
    """
    # Iterate over each year's insights file in the company's directory
    for year_folder in os.listdir(company_path):
        year = int(year_folder.split('-')[1])
        if (year > 90 and year < 100):
            year += 1900
        else:
            year += 2000
        insights_file_path = os.path.join(company_path, year_folder, 'insights.txt')
        if os.path.exists(insights_file_path):
            with open(insights_file_path, 'r') as file:
                insights = file.read()
                data = extract_data(insights)
                net_income = data[0]
                operating_income = data[1]
                summary = data[2]
                if company_path.split('/')[0] == 'Microsoft':
                    msft_year_to_data[year] = [net_income, operating_income, summary]
                elif company_path.split('/')[0] == 'Apple':
                    aapl_year_to_data[year] = [net_income, operating_income, summary]

ticker_to_name= {"AAPL": "Apple", "MSFT": "Microsoft"}

# Populate dictionaries for each ticker symbol
for ticker,name in ticker_to_name.items():
    path = f"{name}/sec-edgar-filings/{ticker}/10-K"
    populate_dicts(path)

# Sort the data by year
msft_sorted = sorted(msft_year_to_data.items())
aapl_sorted = sorted(aapl_year_to_data.items())

# Extract the years and incomes for each company
msft_years = [item[0] for item in msft_sorted]
msft_net_incomes = [item[1][0] for item in msft_sorted]
msft_operating_incomes = [item[1][1] for item in msft_sorted]

aapl_years = [item[0] for item in aapl_sorted]
aapl_net_incomes = [item[1][0] for item in aapl_sorted]
aapl_operating_incomes = [item[1][1] for item in aapl_sorted]

def create_chart(years, incomes, title, color):
    """
    Creates a bar chart of incomes over years.

    Parameters:
    years (list): The years to be plotted on the x-axis.
    incomes (list): The incomes to be plotted on the y-axis.
    title (str): The title of the chart.
    color (str): The color of the bars in the chart.

    Returns:
    dcc.Graph: A Dash Core Components Graph object representing the chart.
    """
    # Create a bar chart
    fig = go.Figure(data=[go.Bar(
        x=years,
        y=incomes,
        marker_color=color,  
        text=incomes,
        textposition='outside',
        hovertext=[f'Year: {year}<br>Income: {income}' for year, income in zip(years, incomes)],
        hoverinfo='text',
        marker_line_color='rgb(0, 0, 0)', 
        marker_line_width=1.5,  
    )])

    # Update the layout of the chart
    fig.update_layout(
        title_text=title,
        xaxis_title="Year",
        yaxis_title="Income (in millions)",
        bargap=0.2,  
        bargroupgap=0.1,  
        xaxis=dict(
            tickmode='array', 
            tickvals=years,  
            ticktext=years 
        ),
        height=600,
        template='plotly_dark', 
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})