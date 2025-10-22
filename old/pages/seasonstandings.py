import dash
from dash import dcc, html, Output, Input, callback
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import math


dash.register_page(__name__, name='Season Standings')

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

# Dataframe Construction
df = pd.merge(lap_times,drivers[['driverId','code','driverRef']],how='left',on='driverId')
df = pd.merge(df,races[['raceId','name','date','year']],how='left',on='raceId')
df

# 2nd Dataframe

df2 = df
#df2 = pd.merge(lap_times,drivers[['driverId','code','driverRef']],how='left',on='driverId')
df2 = pd.merge(df2,driver_standings[['driverStandingsId','raceId','points']],how='left',on='raceId')
#df2
df_2019_2 = df2[df2['year'] == 2019]
df_2019_2

# Driver Position DataFrame
driver_position = drivers.merge(driver_standings,left_on='driverId',right_on='driverId',how = 'left')
driver_position = driver_position.merge(races,on = 'raceId',how = 'left')
#driver_position

# Points Historic
historic_points = df_2019_2.groupby('driverRef').agg({'points':'sum'}).sort_values('points',ascending=False).reset_index().head(10)
#historic_points

#For Final Position Per Race
df_results = results
df_results = df_results.merge(drivers[['driverId','code','driverRef']],how='left',on='driverId')
df_results = df_results.merge(races[['raceId','name','date','year']],how='left',on='raceId')

df_results.drop_duplicates(inplace=True)

df_results[df_results['position']==r'\N']=0
df_results['position'] = df_results['position'].astype(int)

# df 2019 season
df_2019 = df[df['year'] == 2019]
df_2019

#layout
layout = go.Layout(
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(color="black", family="Roboto"),

    xaxis = dict(
        ticklen=10, ticks="outside", tickcolor="white", # simple workaround to move labels from the ticks
        zeroline=True, zerolinecolor="#000", zerolinewidth=1, # zeroline
        gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True, # grids
        layer="above traces", # axis and grid above traces
        showline=True, linewidth=2, linecolor='black', # baseline
        dtick=1
    ),

    yaxis = dict(
        ticklen=10, ticks="outside", tickcolor="white", # simple workaround to move labels from the ticks
        zeroline=True, zerolinecolor="#000", zerolinewidth=1, # zeroline
        gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True, # grids
        layer="above traces", # axis and grid above traces
        showline=True, linewidth=2, linecolor='black', # baseline
    ),

    polar=dict(
        angularaxis=dict(
            ticklen=10, ticks="outside", tickcolor="rgba(0, 0, 0, 0)",
            gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True,
            layer="above traces", # axis and grid above traces
            showline=True, linewidth=2, linecolor='black', # baseline
        ),

        radialaxis=dict(
            ticklen=10, ticks="outside", tickcolor="rgba(0, 0, 0, 0)",
            gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True,
            layer="above traces", # axis and grid above traces
            showline=True, linewidth=2, linecolor='black', # baseline
        ),
        bgcolor="white",
    ),

    margin={"r":60,"t":60,"l":60,"b":60}
)

layout_results = go.Layout(
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(color="black", family="Roboto"),

    xaxis = dict(
        ticklen=10, ticks="outside", tickcolor="white", # simple workaround to move labels from the ticks
        zeroline=True, zerolinecolor="#000", zerolinewidth=1, # zeroline
        gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True, # grids
        layer="above traces", # axis and grid above traces
        showline=True, linewidth=2, linecolor='black', # baseline
        rangemode="tozero",
        dtick=1
    ),

    yaxis = dict(
        ticklen=10, ticks="outside", tickcolor="white", # simple workaround to move labels from the ticks
        zeroline=True, zerolinecolor="#000", zerolinewidth=1, # zeroline
        gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True, # grids
        layer="above traces", # axis and grid above traces
        showline=True, linewidth=2, linecolor='black', # baseline
    ),

    polar=dict(
        angularaxis=dict(
            ticklen=10, ticks="outside", tickcolor="rgba(0, 0, 0, 0)",
            gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True,
            layer="above traces", # axis and grid above traces
            showline=True, linewidth=2, linecolor='black', # baseline
        ),

        radialaxis=dict(
            ticklen=10, ticks="outside", tickcolor="rgba(0, 0, 0, 0)",
            gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True,
            layer="above traces", # axis and grid above traces
            showline=True, linewidth=2, linecolor='black', # baseline
        ),
        bgcolor="white",
    ),

    margin={"r":60,"t":60,"l":60,"b":60}
)

marker = dict(
    color='black'
)
marker = dict(
    color='black'
)


# 2019
h2019 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2019.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2019 = h2019.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2019.dropna(inplace = True)

viz2019.points = viz2019.points.astype('int64')
viz2019.wins = viz2019.wins.astype('int64')
viz2019.date = pd.to_datetime(viz2019.date)
    
top2019 = viz2019[viz2019.loc[:,'year'] == 2019]
top2019 = top2019.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

fig2019 = go.Figure()
fig2019.add_trace(go.Bar(
                x=top2019['surname'],
                y=top2019['points'],
                name='2019 Drivers Standings',
                marker_color='grey'
            ))
fig2019.update_layout(layout_results)
fig2019.update_layout(title ="2019 Drivers Standings", xaxis_title="drivers",yaxis_title="points")

# 2020
h2020 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2020.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2020 = h2020.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2020.dropna(inplace = True)

viz2020.points = viz2020.points.astype('int64')
viz2020.wins = viz2020.wins.astype('int64')
viz2020.date = pd.to_datetime(viz2020.date)
    
top2020 = viz2020[viz2020.loc[:,'year'] == 2020]
top2020 = top2020.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

fig2020 = go.Figure()
fig2020.add_trace(go.Bar(
                x=top2020['surname'],
                y=top2020['points'],
                name='2020 Drivers Standings',
                marker_color='grey'
            ))
fig2020.update_layout(layout_results)
fig2020.update_layout(title ="2020 Drivers Standings", xaxis_title="drivers",yaxis_title="points")



# 2021
h2021 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2021.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2021 = h2021.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2021.dropna(inplace = True)

viz2021.points = viz2021.points.astype('int64')
viz2021.wins = viz2021.wins.astype('int64')
viz2021.date = pd.to_datetime(viz2021.date)
    
top2021 = viz2021[viz2021.loc[:,'year'] == 2021]
top2021 = top2021.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

fig2021 = go.Figure()
fig2021.add_trace(go.Bar(
                x=top2021['surname'],
                y=top2021['points'],
                name='2021 Drivers Standings',
                marker_color='grey'
            ))
fig2021.update_layout(layout_results)
fig2021.update_layout(title ="2021 Drivers Standings", xaxis_title="drivers",yaxis_title="points")

# 2022
h2022 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2022.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2022 = h2022.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2022.dropna(inplace = True)

viz2022.points = viz2022.points.astype('int64')
viz2022.wins = viz2022.wins.astype('int64')
viz2022.date = pd.to_datetime(viz2022.date)
    
top2022 = viz2022[viz2022.loc[:,'year'] == 2022]
top2022 = top2022.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

fig2022 = go.Figure()
fig2022.add_trace(go.Bar(
                x=top2022['surname'],
                y=top2022['points'],
                name='2022 Drivers Standings',
                marker_color='grey'
            ))
fig2022.update_layout(layout_results)
fig2022.update_layout(title ="2022 Drivers Standings", xaxis_title="drivers",yaxis_title="points")

layout = html.Div([
    html.P("Choose the Season: "),
    
    dcc.Dropdown(id="dropdown",
        options=[
            {'label': x, 'value': x}
for x in ['2019', '2020', '2021', '2022']
],
value='2019', clearable=False,),

        dcc.Graph(id='season', figure = fig2021),
    ])

@callback([Output('season','figure')], 
    [Input('dropdown','value')])

def display_figure(value):
    print(value)

    if value == '2019':
        return fig2019

    elif value == '2020':
        return fig2020

    elif value == '2021':
        return fig2021

    elif value == '2022':
        return fig2022