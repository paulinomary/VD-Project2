## Season Standings

import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, name='Standings Season')

# All the csv files
circuits = pd.read_csv("circuits.csv")
constructor_results = pd.read_csv("constructor_results.csv")
constructor_standings = pd.read_csv("constructor_standings.csv")
constructors = pd.read_csv("constructors.csv")
driver_standings = pd.read_csv("driver_standings.csv")
drivers = pd.read_csv("drivers.csv")
lap_times = pd.read_csv("lap_times.csv")
pit_stops = pd.read_csv("pit_stops.csv")
qualifying =pd.read_csv("qualifying.csv")
races = pd.read_csv("races.csv")
results = pd.read_csv("results.csv")
seasons = pd.read_csv("seasons.csv")
sprint_results = pd.read_csv("sprint_results.csv")
status = pd.read_csv("status.csv")



driver_position = drivers.merge(driver_standings,left_on='driverId',right_on='driverId',how = 'left')
driver_position = driver_position.merge(races,on = 'raceId',how = 'left')
h = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h.rename(columns={'name_y':'circuit_name'},inplace=True)
viz = h.loc[:,['date','year','circuit_name','surname','points','wins']]

viz.dropna(inplace = True)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(options=viz.year.unique(),
                                     id='Choose-Year')
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                                  figure=px.histogram(viz, x='surname',
                                                      y='points'))
                    ], width=12
                )
            ]
        )
    ]
)



@callback(
    Output('line-fig', 'figure'),
    Input('Choose-Year', 'value')
)
def update_graph(value):
    if value is None:
        fig = px.histogram(viz, x='surname', y='points')
    else:
        dff = viz[viz.year==value]
        fig = px.histogram(dff, x='surname', y='points')
    return fig