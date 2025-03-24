import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random

# Sample stock data
def generate_data():
    return pd.DataFrame({
        'Stock': ['Apple', 'Meta', 'Google', 'Tesla'] * 5,
        'Price': [random.randint(100, 3000) for _ in range(20)],
        'Volume': [random.randint(50, 200) for _ in range(20)],
        'Market Share': [random.uniform(10, 40) for _ in range(20)],
        'Time': pd.date_range(start='1/1/2023', periods=20, freq='D')
    })

df = generate_data()

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Stock Dashboard", className="text-center"),
            html.Label("Select Stock"),
            dcc.Dropdown(
                id='stock-dropdown',
                options=[{'label': stock, 'value': stock} for stock in df['Stock'].unique()],
                value='Apple',
                clearable=False
            ),
            html.Label("Select Chart Type"),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Candlestick Chart', 'value': 'candlestick'}
                ],
                value='bar',
                clearable=False
            ),
            html.Label("Select Theme"),
            dcc.Dropdown(
                id='theme-dropdown',
                options=[{'label': 'Light Theme', 'value': 'light'},
                         {'label': 'Dark Theme', 'value': 'dark'}],
                value='light',
                clearable=False
            ),
            dcc.Interval(
                id='interval-update',
                interval=5000,  # Updates every 5 seconds
                n_intervals=0
            )
        ], width=3, className="bg-light p-3"),
        
        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Graph(id='price-chart'), width=6),
                dbc.Col(dcc.Graph(id='volume-chart'), width=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='market-share-chart'), width=6),
                dbc.Col(dcc.Graph(id='kpi-chart'), width=6)
            ])
        ], width=9)
    ])
], fluid=True)

# Callbacks for interactivity
@app.callback(
    [Output('price-chart', 'figure'), Output('volume-chart', 'figure'), 
     Output('market-share-chart', 'figure'), Output('kpi-chart', 'figure')],
    [Input('stock-dropdown', 'value'), Input('chart-type-dropdown', 'value'), 
     Input('interval-update', 'n_intervals')]
)
def update_charts(selected_stock, chart_type, n):
    global df
    df = generate_data()  # Simulating real-time data updates
    filtered_df = df[df['Stock'] == selected_stock]
    
    # Price Chart
    if chart_type == 'bar':
        price_fig = px.bar(filtered_df, x='Time', y='Price', title=f'{selected_stock} Price Trend')
    elif chart_type == 'line':
        price_fig = px.line(filtered_df, x='Time', y='Price', title=f'{selected_stock} Price Trend')
    else:
        price_fig = go.Figure(data=[go.Candlestick(
            x=filtered_df['Time'],
            open=filtered_df['Price'] - 5,
            high=filtered_df['Price'] + 10,
            low=filtered_df['Price'] - 15,
            close=filtered_df['Price']
        )])
        price_fig.update_layout(title=f'{selected_stock} Candlestick Chart')
    
    # Volume Chart
    volume_fig = px.area(filtered_df, x='Time', y='Volume', title=f'{selected_stock} Trading Volume')
    
    # Market Share Pie Chart
    market_fig = px.pie(filtered_df, values='Market Share', names='Stock', title=f'Market Share Distribution')
    
    # KPI Chart (Example: Moving Average of Price)
    kpi_fig = px.line(filtered_df, x='Time', y='Price', title=f'{selected_stock} KPI - Moving Average')
    
    return price_fig, volume_fig, market_fig, kpi_fig


    