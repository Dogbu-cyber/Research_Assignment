## Project Documentation

### Overview

This project aims to visualize and analyze key financial indicators—net income and operating income—for Apple and Microsoft over the past two decades. These metrics were selected to provide a comprehensive view of the companies' profitability and growth.

Available Routes

/: The home page displays links to the financial data for Apple and Microsoft.
/stock/<string:stock_name>/<int:year>: Shows the net income, operating income, and a financial summary for the specified stock and year.
/dash/apple: Visualizes Apple's net income and operating income trends over the years using Dash.
/dash/microsoft: Visualizes Microsoft's net income and operating income trends over the years using Dash.

Modules

pull_data.py: Utilizes the SEC Edgar library to download Form 10-K filings and extracts data from the "Item 8" section using regular expressions.
llm_analyze.py: Leverages the AWS Bedrock API to retrieve and analyze net income and operating income for a specified company and year. Generates a summary of the financial health based on the "Item 8" text and stores this information in a structured text file.
generate_charts.py: Produces bar charts visualizing net income and operating income over time, and manages data storage within dictionaries.

Design Process

1. Data Acquisition and Preparation (Relevant files: pull_data.py)
   
The initial challenge was managing the extensive size of the 10-K filings to facilitate effective analysis by our language models. Utilizing the regex (regular expression library), I identified the specific sections in the HTML marked as "Financials and Supplementary Data." By extracting and isolating the text from this section, I reduced the data scope significantly—from about 4-5 million tokens in documents post-1990s to a more manageable 40-50 thousand tokens. This reduction made the documents compatible with flagship AI models like Google Gemini and Anthropic's Claude, which are designed to handle extensive datasets efficiently.

2. Insight Generation (Relevant files: llm_analyze.py)
   
Choosing the appropriate language model (LLM) was a pivotal decision. Due to cost constraints, OpenAI’s GPT series was not considered. Open-source models like Llama and Mistral were evaluated, but their token limits and frequent inaccuracies in data representation made them less viable. After reviewing alternatives, Google’s Gemini 1.5 Pro and Anthropic’s Claude 3 Haiku models stood out, particularly for their data handling capabilities. The Claude 3 Haiku model, accessed via AWS Bedrock, offered the best cost-performance balance, with total API costs under 60 cents for this project.

3. Visualization and Interface Development (Relevant files/folders: templates, static, app.py, generate_charts.py)
   
Developing the user interface presented another major challenge. While I had some familiarity with Django, I opted for Flask due to its simplicity and appropriateness for smaller-scale projects. Initially, I utilized matplotlib’s pyplots for visualizations; however, to enhance the aesthetic and quality of the presentations, I transitioned to using Plotly and Dash. These libraries integrate well with Flask and offer advanced features for creating and displaying interactive charts, significantly improving the user experience.

Closing Remarks

I had a lot of fun working on this project and learned a great deal. Prior to this, I had minimal experience in creating web applications and using regular expressions (regex). Determining how to extract specific parts from the 10-K forms was both frustrating and time-consuming. However, I'm ultimately glad that I persevered and continued to seek a solution.

### Dependencies

To run this project, you will need to install the following dependencies:

- **Python:** Programming language used for developing the application.
- **Flask:** Micro web framework for building web applications.
- **Dash:** Framework for building interactive web-based dashboards.
- **Plotly:** Library for creating interactive plots and graphs.
- **SEC-Edgar:** Library for downloading filings from the U.S. Securities and Exchange Commission.
- **Anthropic:** API for accessing AWS services for Claude.
- **Regular Expressions (re):** Module for text manipulation using regular expressions.

### Usage

#### Starting the Server

Hosted at: https://dogbureke.pythonanywhere.com/

Or, execute the following command to start the Flask server:

```bash
python app.py

