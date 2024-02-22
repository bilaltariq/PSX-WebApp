import dash
from dash import dcc, html, Input, Output, callback
import dash_table
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc


# Create a connection to the SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# External CSS stylesheet
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/superhero/bootstrap.min.css']

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Filter Card"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label('Start Date: '),
                            dcc.DatePickerSingle(
                                id='start-date-picker',
                                min_date_allowed=datetime(2010, 1, 1),
                                max_date_allowed=datetime.today(),
                                initial_visible_month=datetime.today() - timedelta(days=180),
                                date=datetime.today() - timedelta(days=180)
                            )
                        ])
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('End Date: '),
                            dcc.DatePickerSingle(
                                id='end-date-picker',
                                min_date_allowed=datetime(2010, 1, 1),
                                max_date_allowed=datetime.today(),
                                initial_visible_month=datetime.today(),
                                date=datetime.today()
                            )
                        ])
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Sector'),
                            dcc.Dropdown(
                                id='sector-dropdown'
                            )
                        ])
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Stock'),
                            dcc.Dropdown(
                                id='stock-dropdown'
                            )
                        ])
                    ], className='mb-3'),
                ]),
                dbc.CardFooter("Footer"),
            ]),
            width=12
        )
    ], style={'height': '10pct'})
])




# # Callback to update sector dropdown options
# @callback(
#     Output('sector-dropdown', 'options'),
#     [Input('start-date-picker', 'date'),
#      Input('end-date-picker', 'date')]
# )
# def update_sector_options(start_date, end_date):
#     query = "SELECT DISTINCT SectorName FROM meta_data"
#     sectors = cursor.execute(query).fetchall()
#     sectors = [sector[0] for sector in sectors]
#     return [{'label': sector, 'value': sector} for sector in sectors]

# # Callback to update stock dropdown options based on selected sector
# @callback(
#     Output('stock-dropdown', 'options'),
#     [Input('sector-dropdown', 'value')]
# )
# def update_stock_options(selected_sector):
#     query = f"SELECT DISTINCT name FROM meta_data WHERE SectorName = '{selected_sector}'"
#     stocks = cursor.execute(query).fetchall()
#     stocks = [stock[0] for stock in stocks]
#     return [{'label': stock, 'value': stock} for stock in stocks]

# # Callback to display the graph or table based on selected options
# @callback(
#     Output('visualization-container', 'children'),
#     [Input('show-graph-btn', 'n_clicks')],
#     state=[
#         Input('start-date-picker', 'date'),
#         Input('end-date-picker', 'date'),
#         Input('sector-dropdown', 'value'),
#         Input('stock-dropdown', 'value'),
#         Input('visualization-dropdown', 'value')
#     ]
# )
# def update_visualization(n_clicks, start_date, end_date, selected_sector, selected_stock, visualization_type):
#     if n_clicks > 0:
#         # Query data from database based on selected options
#         query = f"SELECT psx_data.Date, psx_data.Close, meta_data.Symbol, meta_data.name, meta_data.SectorName " \
#                 f"FROM psx_data " \
#                 f"INNER JOIN meta_data ON psx_data.ticker = meta_data.Symbol " \
#                 f"WHERE meta_data.SectorName = '{selected_sector}' " \
#                 f"AND meta_data.name = '{selected_stock}' " \
#                 f"AND psx_data.Date BETWEEN '{start_date}' AND '{end_date}'"

#         data = pd.read_sql_query(query, conn)

#         if visualization_type == 'line':
#             # Create and return the line graph
#             fig = {
#                 'data': [
#                     {'x': data['Date'], 'y': data['Close'], 'type': 'line', 'name': selected_stock}
#                 ],
#                 'layout': {
#                     'title': f'{selected_stock} Closing Prices',
#                     'xaxis': {'title': 'Date'},
#                     'yaxis': {'title': 'Closing Price'}
#                 }
#             }
#             return dcc.Graph(figure=fig)
#         elif visualization_type == 'table':
#             # Create and return the data table
#             return DataTable(
#                 id='table',
#                 columns=[{"name": i, "id": i} for i in data.columns],
#                 data=data.to_dict('records')
#             )

if __name__ == '__main__':
    app.run_server(debug=True)
