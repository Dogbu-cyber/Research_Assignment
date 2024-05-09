from flask import Flask, render_template
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import generate_charts

# External stylesheets for Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Flask server
server = Flask(__name__)
# Dash app
app = Dash(__name__, server=server, routes_pathname_prefix='/dash/', external_stylesheets=external_stylesheets)

@server.route('/')
def home():
    """
    Home route that renders the home page.

    Returns:
    str: Rendered home page.
    """
    return render_template('home.html', msft_years = generate_charts.msft_years, aapl_years = generate_charts.aapl_years)

@server.route('/stock/<string:stock_name>/<int:year>')
def stock_year(stock_name, year):
    """
    Route that renders a page for a specific stock in a specific year.

    Parameters:
    stock_name (str): The name of the stock.
    year (int): The year.

    Returns:
    str: Rendered page for the stock in the year.
    """
    # Get the data for the specified stock and year
    if stock_name == 'apple':
        net_income, operating_income, summary = generate_charts.aapl_year_to_data[year]
        years = generate_charts.aapl_years
    elif stock_name == 'microsoft':
        net_income, operating_income, summary = generate_charts.msft_year_to_data[year]
        years = generate_charts.msft_years
    else:
        return f"404 Page Error"

    # Find the previous year with available data for comparison
    previous_year = None
    for y in reversed(years):
        if y < year:
            previous_year = y
            break

    # Get the data for the previous year
    if previous_year:
        prev_net_income, prev_operating_income, _ = generate_charts.aapl_year_to_data[previous_year] if stock_name == 'apple' else generate_charts.msft_year_to_data[previous_year]
    else:
        prev_net_income, prev_operating_income = None, None

    return render_template('year.html', year=year, stock_name=stock_name.capitalize(), net_income=net_income, operating_income=operating_income, summary=summary, prev_year=previous_year, prev_net_income=prev_net_income, prev_operating_income=prev_operating_income)

# Dash layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    Callback to update the page content based on the URL.

    Parameters:
    pathname (str): The URL pathname.

    Returns:
    str: The updated page content.
    """
    # Display the appropriate charts based on the URL
    if pathname == '/dash/apple':
        return html.Div([
            generate_charts.create_chart(generate_charts.aapl_years, generate_charts.aapl_net_incomes, 'Apple Net Income by Year', 'blue'),
            generate_charts.create_chart(generate_charts.aapl_years, generate_charts.aapl_operating_incomes, 'Apple Operating Income by Year', 'green'),
        ])
    elif pathname == '/dash/microsoft':
        return html.Div([
            generate_charts.create_chart(generate_charts.msft_years, generate_charts.msft_net_incomes, 'Microsoft Net Income by Year', 'red'),
            generate_charts.create_chart(generate_charts.msft_years, generate_charts.msft_operating_incomes, 'Microsoft Operating Income by Year', 'purple'),
        ])
    else:
        return "404 Page Error"

if __name__ == '__main__':
    server.run(debug=True)