import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, callback
import pandas as pd

dash.register_page(__name__, name='Races')

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


df = pd.merge(lap_times,drivers[['driverId','code','driverRef']],how='left',on='driverId')
df = pd.merge(df,races[['raceId','name','date','year']],how='left',on='raceId')

df_2019 = df[df['year'] == 2019]

indexRB_2019 = df_2019[ (df_2019['code'] != 'VER') & (df_2019['code'] != 'GAS')  & (df_2019['code'] != 'ALB')].index
df_2019.drop(indexRB_2019 , inplace=True)

df_laps = df[(df['year']==2019)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')].copy()
df_laps.rename(columns={'position':'lap position'},inplace=True)
df_laps = df_laps.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps = df_laps.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps['stop'].fillna(0,inplace=True)
df_laps['stop']=df_laps['stop'].astype(int)
df_laps['stop'][df_laps['stop']==0] = ''
df_laps

df_2019_F = df_laps[(df_laps['year'] == 2019)]

df_laps_2020 = df[(df['year']==2020)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2020.rename(columns={'position':'lap position'},inplace=True)
df_laps_2020 = df_laps_2020.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2020 = df_laps_2020.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2020['stop'].fillna(0,inplace=True)
df_laps_2020['stop']=df_laps_2020['stop'].astype(int)
df_laps_2020['stop'][df_laps_2020['stop']==0] = ''

df_2020 = df_laps_2020[df_laps_2020['year'] == 2020]

df_laps_2021 = df[(df['year']==2021)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2021.rename(columns={'position':'lap position'},inplace=True)
df_laps_2021 = df_laps_2021.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2021 = df_laps_2021.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2021['stop'].fillna(0,inplace=True)
df_laps_2021['stop']=df_laps_2021['stop'].astype(int)
df_laps_2021['stop'][df_laps_2021['stop']==0] = ''

df_2021 = df_laps_2021[df_laps_2021['year'] == 2021]

df_laps_2022 = df[(df['year']==2022)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2022.rename(columns={'position':'lap position'},inplace=True)
df_laps_2022 = df_laps_2022.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2022 = df_laps_2022.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2022['stop'].fillna(0,inplace=True)
df_laps_2022['stop']=df_laps_2022['stop'].astype(int)
df_laps_2022['stop'][df_laps_2022['stop']==0] = ''

df_2022 = df_laps_2022[df_laps_2022['year'] == 2022]



all_options = {
    '2019': df_2019_F['name'].unique(),
    '2020': df_2020['name'].unique(),
    '2021': df_2021['name'].unique(),
    '2022': df_2022['name'].unique()
}

layout = html.Div([
    dcc.RadioItems(
        list(all_options.keys()),
        '2019',
        id='countries-radio',
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    html.Div(id='display-selected-values'),

    dbc.Row(
        dbc.Col(
                [
                    dcc.Graph(id='bar-fig',
                              figure=px.scatter(df_laps, x='lap', y='time',color = "driverRef"))
                ], width=12
            )
        )
])


@callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'))
def set_display_children(selected_country, selected_city):
    return u'{} took place in {}'.format(
        selected_city, selected_country,
    )
