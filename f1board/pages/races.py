import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, callback
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import math

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
# df 2019 season
df_2019 = df[df['year'] == 2019]
# 2019 with just RB drivers(RB & Toro roso)

indexRB_2019 = df_2019[ (df_2019['code'] != 'VER') & (df_2019['code'] != 'GAS')  & (df_2019['code'] != 'ALB')].index

df_2019.drop(indexRB_2019 , inplace=True)
# df Every lap of every GP 2019 SEASON

df_laps = df[(df['year']==2019)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')].copy()
df_laps.rename(columns={'position':'lap position'},inplace=True)
df_laps = df_laps.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps = df_laps.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps['stop'].fillna(0,inplace=True)
df_laps['stop']=df_laps['stop'].astype(int)
df_laps['stop'][df_laps['stop']==0] = ''
df_laps['seconds']=df_laps['milliseconds']/1000

# 2020 Season Gran Prixs info

df_laps_2020 = df[(df['year']==2020)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2020.rename(columns={'position':'lap position'},inplace=True)
df_laps_2020 = df_laps_2020.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2020 = df_laps_2020.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2020['stop'].fillna(0,inplace=True)
df_laps_2020['stop']=df_laps_2020['stop'].astype(int)
df_laps_2020['stop'][df_laps_2020['stop']==0] = ''
df_laps_2020['seconds']=df_laps_2020['milliseconds']/1000
df_laps_2020

# 2021 Season races info

df_laps_2021 = df[(df['year']==2021)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2021.rename(columns={'position':'lap position'},inplace=True)
df_laps_2021 = df_laps_2021.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2021 = df_laps_2021.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2021['stop'].fillna(0,inplace=True)
df_laps_2021['stop']=df_laps_2021['stop'].astype(int)
df_laps_2021['stop'][df_laps_2021['stop']==0] = ''
df_laps_2021['seconds']=df_laps_2021['milliseconds']/1000
df_laps_2021

# 2022 Season races info

df_laps_2022 = df[(df['year']==2022)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2022.rename(columns={'position':'lap position'},inplace=True)
df_laps_2022 = df_laps_2022.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2022 = df_laps_2022.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2022['stop'].fillna(0,inplace=True)
df_laps_2022['stop']=df_laps_2022['stop'].astype(int)
df_laps_2022['stop'][df_laps_2022['stop']==0] = ''
df_laps_2022['seconds']=df_laps_2022['milliseconds']/1000
df_laps_2022

# Gran Prixs of 2019 season
df_2019_F = df_laps[(df_laps['year'] == 2019)]
df_2019_F['name'].unique()

# 2020 Season
df_2020 = df_laps_2020[df_laps_2020['year'] == 2020]
df_2020

# 2021 Season
df_2021 = df_laps_2021[df_laps_2021['year'] == 2021]
df_2021

# 2022 Season
df_2022 = df_laps_2022[df_laps_2022['year'] == 2022]
df_2022

# Races: Graph Objects
layout = go.Layout(
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(color="black", family="Roboto"),

    xaxis = dict(
        ticklen=10, ticks="outside", tickcolor="white", # simple workaround to move labels from the ticks
        zeroline=True, zerolinecolor="#000", zerolinewidth=1, # zeroline
        gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True, # grids
        layer="above traces", # axis and grid above traces
        showline=True, linewidth=2, linecolor='black', # baseline
        rangemode="tozero",
        dtick=5
    ),

    yaxis = dict(
        ticklen=10, ticks="outside", tickcolor="white", # simple workaround to move labels from the ticks
        zeroline=True, zerolinecolor="#000", zerolinewidth=1, # zeroline
        gridcolor="#BBB", gridwidth=0.5, griddash='dot', showgrid=True, # grids
        layer="above traces", # axis and grid above traces
        showline=True, linewidth=2, linecolor='black',
        # baseline
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
# Defining Colors for each driver
indexRB_ver_19 = df_2019_F[(df_2019_F['code'] == 'VER')].index
df_2019_F.loc[indexRB_ver_19,'color'] = '#66c2a5'

indexRB_gasly_19 = df_2019_F[(df_2019_F['code'] == 'GAS')].index
df_2019_F.loc[indexRB_gasly_19,'color'] = '#fc8d62'

indexRB_albon_19 = df_2019_F[(df_2019_F['code'] == 'ALB')].index
df_2019_F.loc[indexRB_albon_19,'color'] = '#8da0cb'

# Australian Grand Prix

df_2019_F_AUST = df_2019_F[(df_2019_F['name'] == 'Australian Grand Prix')]
df_2019_AUST = df_2019_F_AUST.query("driverRef in ['gasly', 'max_verstappen','albon']")
#df_2019_AUST = df_2019_AUST.sort_values(by="seconds")
df_2019_AUST = df_2019_AUST.sort_values(by="lap")


df_2019_AUST_ver =df_2019_AUST[df_2019_AUST['code']=='VER']

df_2019_AUST_gas=df_2019_AUST[df_2019_AUST['code']=='GAS']

df_2019_AUST_alb =df_2019_AUST[df_2019_AUST['code']=='ALB']

fig2019_1 = go.Figure()

fig2019_1.add_trace(go.Scatter(x=df_2019_AUST_ver['lap'], y=df_2019_AUST_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_AUST_ver['color'],
                           marker=dict(color=df_2019_AUST_ver['color'])
))
fig2019_1.add_trace(go.Scatter(x=df_2019_AUST_gas['lap'], y=df_2019_AUST_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_AUST_gas['color'],
                           marker=dict(color=df_2019_AUST_gas['color'])
))


fig2019_1.add_trace(go.Scatter(x=df_2019_AUST_alb['lap'], y=df_2019_AUST_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_AUST_alb['color'])
))

fig2019_1.update_layout(layout)
fig2019_1.update_layout(title = '2019 Australian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Bahrain Grand Prix

df_2019_F_BAH = df_2019_F[(df_2019_F['name'] == 'Bahrain Grand Prix')]
df_2019_BAH = df_2019_F_BAH.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_BAH = df_2019_BAH.sort_values(by="lap")

df_2019_BAH_ver =df_2019_BAH[df_2019_BAH['code']=='VER']

df_2019_BAH_gas=df_2019_BAH[df_2019_BAH['code']=='GAS']

df_2019_BAH_alb =df_2019_BAH[df_2019_BAH['code']=='ALB']

fig2019_2 = go.Figure()

fig2019_2.add_trace(go.Scatter(x=df_2019_BAH_ver['lap'], y=df_2019_BAH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_BAH_ver['color'],
                           marker=dict(color=df_2019_BAH_ver['color'])
))
fig2019_2.add_trace(go.Scatter(x=df_2019_BAH_gas['lap'], y=df_2019_BAH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_BAH_gas['color'],
                           marker=dict(color=df_2019_BAH_gas['color'])
))


fig2019_2.add_trace(go.Scatter(x=df_2019_BAH_alb['lap'], y=df_2019_BAH_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_BAH_alb['color'])
))

fig2019_2.update_layout(layout)
fig2019_2.update_layout(title = '2019 Bahrain Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Chinese Grand Prix

df_2019_F_CHN = df_2019_F[(df_2019_F['name'] == 'Chinese Grand Prix')]
df_2019_CHN = df_2019_F_CHN.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_CHN = df_2019_CHN.sort_values(by="lap")

df_2019_CHN_ver =df_2019_CHN[df_2019_CHN['code']=='VER']

df_2019_CHN_gas=df_2019_CHN[df_2019_CHN['code']=='GAS']

df_2019_CHN_alb =df_2019_CHN[df_2019_CHN['code']=='ALB']

fig2019_3 = go.Figure()

fig2019_3.add_trace(go.Scatter(x=df_2019_CHN_ver['lap'], y=df_2019_CHN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_CHN_ver['color'],
                           marker=dict(color=df_2019_CHN_ver['color'])
))
fig2019_3.add_trace(go.Scatter(x=df_2019_CHN_gas['lap'], y=df_2019_CHN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_CHN_gas['color'],
                           marker=dict(color=df_2019_CHN_gas['color'])
))


fig2019_3.add_trace(go.Scatter(x=df_2019_CHN_alb['lap'], y=df_2019_CHN_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_CHN_alb['color'])
))

fig2019_3.update_layout(layout)
fig2019_3.update_layout(title = '2019 Chinese Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Azerbaijan Grand Prix

df_2019_F_AZB = df_2019_F[(df_2019_F['name'] == 'Azerbaijan Grand Prix')]
df_2019_AZB = df_2019_F_AZB.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_AZB = df_2019_AZB.sort_values(by="lap")

df_2019_AZB_ver =df_2019_AZB[df_2019_AZB['code']=='VER']

df_2019_AZB_gas=df_2019_AZB[df_2019_AZB['code']=='GAS']

df_2019_AZB_alb =df_2019_AZB[df_2019_AZB['code']=='ALB']

fig2019_4 = go.Figure()

fig2019_4.add_trace(go.Scatter(x=df_2019_AZB_ver['lap'], y=df_2019_AZB_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_AZB_ver['color'],
                           marker=dict(color=df_2019_AZB_ver['color'])
))
fig2019_4.add_trace(go.Scatter(x=df_2019_AZB_gas['lap'], y=df_2019_AZB_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_AZB_gas['color'],
                           marker=dict(color=df_2019_AZB_gas['color'])
))


fig2019_4.add_trace(go.Scatter(x=df_2019_AZB_alb['lap'], y=df_2019_AZB_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_AZB_alb['color'])
))

fig2019_4.update_layout(layout)
fig2019_4.update_layout(title = '2019 Azerbaijan Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Spanish Grand Prix

df_2019_F_SPN = df_2019_F[(df_2019_F['name'] == 'Spanish Grand Prix')]
df_2019_SPN = df_2019_F_SPN.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_SPN = df_2019_SPN.sort_values(by="lap")

df_2019_SPN_ver =df_2019_SPN[df_2019_SPN['code']=='VER']

df_2019_SPN_gas=df_2019_SPN[df_2019_SPN['code']=='GAS']

df_2019_SPN_alb =df_2019_SPN[df_2019_SPN['code']=='ALB']

fig2019_5 = go.Figure()

fig2019_5.add_trace(go.Scatter(x=df_2019_SPN_ver['lap'], y=df_2019_SPN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_SPN_ver['color'],
                           marker=dict(color=df_2019_SPN_ver['color'])
))
fig2019_5.add_trace(go.Scatter(x=df_2019_SPN_gas['lap'], y=df_2019_SPN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_SPN_gas['color'],
                           marker=dict(color=df_2019_SPN_gas['color'])
))


fig2019_5.add_trace(go.Scatter(x=df_2019_SPN_alb['lap'], y=df_2019_SPN_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_SPN_alb['color'])
))

fig2019_5.update_layout(layout)
fig2019_5.update_layout(title = '2019 Spanish Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Monaco Grand Prix

df_2019_F_MON = df_2019_F[(df_2019_F['name'] == 'Monaco Grand Prix')]
df_2019_MON = df_2019_F_MON.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_MON = df_2019_MON.sort_values(by="lap")

df_2019_MON_ver =df_2019_MON[df_2019_MON['code']=='VER']

df_2019_MON_gas=df_2019_MON[df_2019_MON['code']=='GAS']

df_2019_MON_alb =df_2019_MON[df_2019_MON['code']=='ALB']

fig2019_6 = go.Figure()

fig2019_6.add_trace(go.Scatter(x=df_2019_MON_ver['lap'], y=df_2019_MON_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_MON_ver['color'],
                           marker=dict(color=df_2019_MON_ver['color'])
))
fig2019_6.add_trace(go.Scatter(x=df_2019_MON_gas['lap'], y=df_2019_MON_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_MON_gas['color'],
                           marker=dict(color=df_2019_MON_gas['color'])
))


fig2019_6.add_trace(go.Scatter(x=df_2019_MON_alb['lap'], y=df_2019_MON_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_MON_alb['color'])
))

fig2019_6.update_layout(layout)
fig2019_6.update_layout(title = '2019 Monaco Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Canadian Grand Prix

df_2019_F_CAN = df_2019_F[(df_2019_F['name'] == 'Canadian Grand Prix')]
df_2019_CAN = df_2019_F_CAN.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_CAN = df_2019_CAN.sort_values(by="lap")

df_2019_CAN_ver =df_2019_CAN[df_2019_CAN['code']=='VER']

df_2019_CAN_gas=df_2019_CAN[df_2019_CAN['code']=='GAS']

df_2019_CAN_alb =df_2019_CAN[df_2019_CAN['code']=='ALB']

fig2019_7 = go.Figure()

fig2019_7.add_trace(go.Scatter(x=df_2019_CAN_ver['lap'], y=df_2019_CAN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_CAN_ver['color'],
                           marker=dict(color=df_2019_CAN_ver['color'])
))
fig2019_7.add_trace(go.Scatter(x=df_2019_CAN_gas['lap'], y=df_2019_CAN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_CAN_gas['color'],
                           marker=dict(color=df_2019_CAN_gas['color'])
))


fig2019_7.add_trace(go.Scatter(x=df_2019_CAN_alb['lap'], y=df_2019_CAN_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_CAN_alb['color'])
))

fig2019_7.update_layout(layout)
fig2019_7.update_layout(title = '2019 Canadian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# French Grand Prix

df_2019_F_FRA = df_2019_F[(df_2019_F['name'] == 'French Grand Prix')]
df_2019_FRA = df_2019_F_FRA.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_FRA = df_2019_FRA.sort_values(by="lap")

df_2019_FRA_ver =df_2019_FRA[df_2019_FRA['code']=='VER']

df_2019_FRA_gas=df_2019_FRA[df_2019_FRA['code']=='GAS']

df_2019_FRA_alb =df_2019_FRA[df_2019_FRA['code']=='ALB']

fig2019_8 = go.Figure()

fig2019_8.add_trace(go.Scatter(x=df_2019_FRA_ver['lap'], y=df_2019_FRA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_FRA_ver['color'],
                           marker=dict(color=df_2019_FRA_ver['color'])
))
fig2019_8.add_trace(go.Scatter(x=df_2019_FRA_gas['lap'], y=df_2019_FRA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_FRA_gas['color'],
                           marker=dict(color=df_2019_FRA_gas['color'])
))


fig2019_8.add_trace(go.Scatter(x=df_2019_FRA_alb['lap'], y=df_2019_FRA_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_FRA_alb['color'])
))

fig2019_8.update_layout(layout)
fig2019_8.update_layout(title = '2019 French Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Austrian Grand Prix

df_2019_F_AUT = df_2019_F[(df_2019_F['name'] == 'Austrian Grand Prix')]
df_2019_AUT = df_2019_F_AUT.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_AUT = df_2019_AUT.sort_values(by="lap")

df_2019_AUT_ver =df_2019_AUT[df_2019_AUT['code']=='VER']

df_2019_AUT_gas=df_2019_AUT[df_2019_AUT['code']=='GAS']

df_2019_AUT_alb =df_2019_AUT[df_2019_AUT['code']=='ALB']

fig2019_9 = go.Figure()

fig2019_9.add_trace(go.Scatter(x=df_2019_AUT_ver['lap'], y=df_2019_AUT_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_AUT_ver['color'],
                           marker=dict(color=df_2019_AUT_ver['color'])
))
fig2019_9.add_trace(go.Scatter(x=df_2019_AUT_gas['lap'], y=df_2019_AUT_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_AUT_gas['color'],
                           marker=dict(color=df_2019_AUT_gas['color'])
))


fig2019_9.add_trace(go.Scatter(x=df_2019_AUT_alb['lap'], y=df_2019_AUT_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_AUT_alb['color'])
))

fig2019_9.update_layout(layout)
fig2019_9.update_layout(title = '2019 Austrian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# British Grand Prix

df_2019_F_BRIT = df_2019_F[(df_2019_F['name'] == 'British Grand Prix')]
df_2019_BRIT = df_2019_F_BRIT.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_BRIT = df_2019_BRIT.sort_values(by="lap")

df_2019_BRIT_ver =df_2019_BRIT[df_2019_BRIT['code']=='VER']

df_2019_BRIT_gas=df_2019_BRIT[df_2019_BRIT['code']=='GAS']

df_2019_BRIT_alb =df_2019_BRIT[df_2019_BRIT['code']=='ALB']

fig2019_10 = go.Figure()

fig2019_10.add_trace(go.Scatter(x=df_2019_BRIT_ver['lap'], y=df_2019_BRIT_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_BRIT_ver['color'],
                           marker=dict(color=df_2019_BRIT_ver['color'])
))
fig2019_10.add_trace(go.Scatter(x=df_2019_BRIT_gas['lap'], y=df_2019_BRIT_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_BRIT_gas['color'],
                           marker=dict(color=df_2019_BRIT_gas['color'])
))


fig2019_10.add_trace(go.Scatter(x=df_2019_BRIT_alb['lap'], y=df_2019_BRIT_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_BRIT_alb['color'])
))

fig2019_10.update_layout(layout)
fig2019_10.update_layout(title = '2019 British Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# German Grand Prix

df_2019_F_GER = df_2019_F[(df_2019_F['name'] == 'German Grand Prix')]
df_2019_GER = df_2019_F_GER.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_GER = df_2019_GER.sort_values(by="lap")

df_2019_GER_ver =df_2019_GER[df_2019_GER['code']=='VER']

df_2019_GER_gas=df_2019_GER[df_2019_GER['code']=='GAS']

df_2019_GER_alb =df_2019_GER[df_2019_GER['code']=='ALB']

fig2019_11 = go.Figure()

fig2019_11.add_trace(go.Scatter(x=df_2019_GER_ver['lap'], y=df_2019_GER_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_GER_ver['color'],
                           marker=dict(color=df_2019_GER_ver['color'])
))
fig2019_11.add_trace(go.Scatter(x=df_2019_GER_gas['lap'], y=df_2019_GER_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_GER_gas['color'],
                           marker=dict(color=df_2019_GER_gas['color'])
))


fig2019_11.add_trace(go.Scatter(x=df_2019_GER_alb['lap'], y=df_2019_GER_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_GER_alb['color'])
))

fig2019_11.update_layout(layout)
fig2019_11.update_layout(title = '2019 German Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Hungarian Grand Prix

df_2019_F_HUN = df_2019_F[(df_2019_F['name'] == 'Hungarian Grand Prix')]
df_2019_HUN = df_2019_F_HUN.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_HUN = df_2019_HUN.sort_values(by="lap")


df_2019_HUN_ver =df_2019_HUN[df_2019_HUN['code']=='VER']

df_2019_HUN_gas=df_2019_HUN[df_2019_HUN['code']=='GAS']

df_2019_HUN_alb =df_2019_HUN[df_2019_HUN['code']=='ALB']

fig2019_12 = go.Figure()

fig2019_12.add_trace(go.Scatter(x=df_2019_HUN_ver['lap'], y=df_2019_HUN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_HUN_ver['color'],
                           marker=dict(color=df_2019_HUN_ver['color'])
))
fig2019_12.add_trace(go.Scatter(x=df_2019_HUN_gas['lap'], y=df_2019_HUN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_HUN_gas['color'],
                           marker=dict(color=df_2019_HUN_gas['color'])
))


fig2019_12.add_trace(go.Scatter(x=df_2019_HUN_alb['lap'], y=df_2019_HUN_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_HUN_alb['color'])
))

fig2019_12.update_layout(layout)
fig2019_12.update_layout(title = '2019 Hungarian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Belgian Grand Prix

df_2019_F_BEL = df_2019_F[(df_2019_F['name'] == 'Belgian Grand Prix')]
df_2019_BEL = df_2019_F_BEL.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_BEL = df_2019_BEL.sort_values(by="lap")

df_2019_BEL_ver =df_2019_BEL[df_2019_BEL['code']=='VER']

df_2019_BEL_gas=df_2019_BEL[df_2019_BEL['code']=='GAS']

df_2019_BEL_alb =df_2019_BEL[df_2019_BEL['code']=='ALB']

fig2019_13 = go.Figure()

fig2019_13.add_trace(go.Scatter(x=df_2019_BEL_ver['lap'], y=df_2019_BEL_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_BEL_ver['color'],
                           marker=dict(color=df_2019_BEL_ver['color'])
))
fig2019_13.add_trace(go.Scatter(x=df_2019_BEL_gas['lap'], y=df_2019_BEL_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_BEL_gas['color'],
                           marker=dict(color=df_2019_BEL_gas['color'])
))


fig2019_13.add_trace(go.Scatter(x=df_2019_BEL_alb['lap'], y=df_2019_BEL_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_BEL_alb['color'])
))

fig2019_13.update_layout(layout)
fig2019_13.update_layout(title = '2019 Belgian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Italian Grand Prix

df_2019_F_ITA = df_2019_F[(df_2019_F['name'] == 'Italian Grand Prix')]
df_2019_ITA = df_2019_F_ITA.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_ITA = df_2019_ITA.sort_values(by="lap")

df_2019_ITA_ver =df_2019_ITA[df_2019_ITA['code']=='VER']

df_2019_ITA_gas=df_2019_ITA[df_2019_ITA['code']=='GAS']

df_2019_ITA_alb =df_2019_ITA[df_2019_ITA['code']=='ALB']

fig2019_14 = go.Figure()

fig2019_14.add_trace(go.Scatter(x=df_2019_ITA_ver['lap'], y=df_2019_ITA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_ITA_ver['color'],
                           marker=dict(color=df_2019_ITA_ver['color'])
))
fig2019_14.add_trace(go.Scatter(x=df_2019_ITA_gas['lap'], y=df_2019_ITA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_ITA_gas['color'],
                           marker=dict(color=df_2019_ITA_gas['color'])
))


fig2019_14.add_trace(go.Scatter(x=df_2019_ITA_alb['lap'], y=df_2019_ITA_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_ITA_alb['color'])
))

fig2019_14.update_layout(layout)
fig2019_14.update_layout(title = '2019 Italian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Singapore Grand Prix

df_2019_F_SGP = df_2019_F[(df_2019_F['name'] == 'Singapore Grand Prix')]
df_2019_SGP = df_2019_F_SGP.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_SGP = df_2019_SGP.sort_values(by="lap")

df_2019_SGP_ver =df_2019_SGP[df_2019_SGP['code']=='VER']

df_2019_SGP_gas=df_2019_SGP[df_2019_SGP['code']=='GAS']

df_2019_SGP_alb =df_2019_SGP[df_2019_SGP['code']=='ALB']

fig2019_15 = go.Figure()

fig2019_15.add_trace(go.Scatter(x=df_2019_SGP_ver['lap'], y=df_2019_SGP_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_SGP_ver['color'],
                           marker=dict(color=df_2019_SGP_ver['color'])
))
fig2019_15.add_trace(go.Scatter(x=df_2019_SGP_gas['lap'], y=df_2019_SGP_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_SGP_gas['color'],
                           marker=dict(color=df_2019_SGP_gas['color'])
))


fig2019_15.add_trace(go.Scatter(x=df_2019_SGP_alb['lap'], y=df_2019_SGP_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_SGP_alb['color'])
))

fig2019_15.update_layout(layout)
fig2019_15.update_layout(title = '2019 Singapore Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Russian Grand Prix

df_2019_F_RUS = df_2019_F[(df_2019_F['name'] == 'Russian Grand Prix')]
df_2019_RUS = df_2019_F_RUS.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_RUS = df_2019_RUS.sort_values(by="lap")


df_2019_RUS_ver =df_2019_RUS[df_2019_RUS['code']=='VER']

df_2019_RUS_gas=df_2019_RUS[df_2019_RUS['code']=='GAS']

df_2019_RUS_alb =df_2019_RUS[df_2019_RUS['code']=='ALB']

fig2019_16 = go.Figure()

fig2019_16.add_trace(go.Scatter(x=df_2019_RUS_ver['lap'], y=df_2019_RUS_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_RUS_ver['color'],
                           marker=dict(color=df_2019_RUS_ver['color'])
))
fig2019_16.add_trace(go.Scatter(x=df_2019_RUS_gas['lap'], y=df_2019_RUS_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_RUS_gas['color'],
                           marker=dict(color=df_2019_RUS_gas['color'])
))


fig2019_16.add_trace(go.Scatter(x=df_2019_RUS_alb['lap'], y=df_2019_RUS_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_RUS_alb['color'])
))

fig2019_16.update_layout(layout)
fig2019_16.update_layout(title = '2019 Russian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Japanese Grand Prix

df_2019_F_JAP = df_2019_F[(df_2019_F['name'] == 'Japanese Grand Prix')]
df_2019_JAP = df_2019_F_JAP.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_JAP = df_2019_JAP.sort_values(by="lap")

df_2019_JAP_ver =df_2019_JAP[df_2019_JAP['code']=='VER']

df_2019_JAP_gas=df_2019_JAP[df_2019_JAP['code']=='GAS']

df_2019_JAP_alb =df_2019_JAP[df_2019_JAP['code']=='ALB']

fig2019_17 = go.Figure()

fig2019_17.add_trace(go.Scatter(x=df_2019_JAP_ver['lap'], y=df_2019_JAP_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_JAP_ver['color'],
                           marker=dict(color=df_2019_JAP_ver['color'])
))
fig2019_17.add_trace(go.Scatter(x=df_2019_JAP_gas['lap'], y=df_2019_JAP_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_JAP_gas['color'],
                           marker=dict(color=df_2019_JAP_gas['color'])
))


fig2019_17.add_trace(go.Scatter(x=df_2019_JAP_alb['lap'], y=df_2019_JAP_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_JAP_alb['color'])
))

fig2019_17.update_layout(layout)
fig2019_17.update_layout(title = '2019 Japanese Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Mexican Grand Prix

df_2019_F_MEX = df_2019_F[(df_2019_F['name'] == 'Mexican Grand Prix')]
df_2019_MEX = df_2019_F_MEX.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_MEX = df_2019_MEX.sort_values(by="lap")

df_2019_MEX_ver =df_2019_MEX[df_2019_MEX['code']=='VER']

df_2019_MEX_gas=df_2019_MEX[df_2019_MEX['code']=='GAS']

df_2019_MEX_alb =df_2019_MEX[df_2019_MEX['code']=='ALB']

fig2019_18 = go.Figure()

fig2019_18.add_trace(go.Scatter(x=df_2019_MEX_ver['lap'], y=df_2019_MEX_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_MEX_ver['color'],
                           marker=dict(color=df_2019_MEX_ver['color'])
))
fig2019_18.add_trace(go.Scatter(x=df_2019_MEX_gas['lap'], y=df_2019_MEX_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_MEX_gas['color'],
                           marker=dict(color=df_2019_MEX_gas['color'])
))


fig2019_18.add_trace(go.Scatter(x=df_2019_MEX_alb['lap'], y=df_2019_MEX_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_MEX_alb['color'])
))

fig2019_18.update_layout(layout)
fig2019_18.update_layout(title = '2019 Mexican Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# United States Grand Prix

df_2019_F_US = df_2019_F[(df_2019_F['name'] == 'United States Grand Prix')]
df_2019_US  = df_2019_F_US.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_US  = df_2019_US.sort_values(by="lap")

df_2019_US_ver =df_2019_US[df_2019_US['code']=='VER']

df_2019_US_gas=df_2019_US[df_2019_US['code']=='GAS']

df_2019_US_alb =df_2019_US[df_2019_US['code']=='ALB']

fig2019_19 = go.Figure()

fig2019_19.add_trace(go.Scatter(x=df_2019_US_ver['lap'], y=df_2019_US_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_US_ver['color'],
                           marker=dict(color=df_2019_US_ver['color'])
))
fig2019_19.add_trace(go.Scatter(x=df_2019_US_gas['lap'], y=df_2019_US_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_US_gas['color'],
                           marker=dict(color=df_2019_US_gas['color'])
))


fig2019_19.add_trace(go.Scatter(x=df_2019_US_alb['lap'], y=df_2019_US_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_US_alb['color'])
))

fig2019_19.update_layout(layout)
fig2019_19.update_layout(title = '2019 United States Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Brazilian Grand Prix

df_2019_F_BRZ = df_2019_F[(df_2019_F['name'] == 'Brazilian Grand Prix')]
df_2019_BRZ  = df_2019_F_BRZ.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_BRZ  = df_2019_BRZ.sort_values(by="lap")

df_2019_BRZ_ver =df_2019_BRZ[df_2019_BRZ['code']=='VER']

df_2019_BRZ_gas=df_2019_BRZ[df_2019_BRZ['code']=='GAS']

df_2019_BRZ_alb =df_2019_BRZ[df_2019_BRZ['code']=='ALB']

fig2019_20 = go.Figure()

fig2019_20.add_trace(go.Scatter(x=df_2019_BRZ_ver['lap'], y=df_2019_BRZ_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_BRZ_ver['color'],
                           marker=dict(color=df_2019_BRZ_ver['color'])
))
fig2019_20.add_trace(go.Scatter(x=df_2019_BRZ_gas['lap'], y=df_2019_BRZ_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_BRZ_gas['color'],
                           marker=dict(color=df_2019_BRZ_gas['color'])
))


fig2019_20.add_trace(go.Scatter(x=df_2019_BRZ_alb['lap'], y=df_2019_BRZ_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_BRZ_alb['color'])
))

fig2019_20.update_layout(layout)
fig2019_20.update_layout(title = '2019 Brazilian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Abu Dhabi Grand Prix

df_2019_F_ABH = df_2019_F[(df_2019_F['name'] == 'Abu Dhabi Grand Prix')]
df_2019_ABH  = df_2019_F_ABH.query("driverRef in ['gasly', 'max_verstappen','albon']")
df_2019_ABH  = df_2019_ABH.sort_values(by="lap")

df_2019_ABH_ver =df_2019_ABH[df_2019_ABH['code']=='VER']

df_2019_ABH_gas=df_2019_ABH[df_2019_ABH['code']=='GAS']

df_2019_ABH_alb =df_2019_ABH[df_2019_ABH['code']=='ALB']

fig2019_21 = go.Figure()

fig2019_21.add_trace(go.Scatter(x=df_2019_ABH_ver['lap'], y=df_2019_ABH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2019_ABH_ver['color'],
                           marker=dict(color=df_2019_ABH_ver['color'])
))
fig2019_21.add_trace(go.Scatter(x=df_2019_ABH_gas['lap'], y=df_2019_ABH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2019_ABH_gas['color'],
                           marker=dict(color=df_2019_ABH_gas['color'])
))


fig2019_21.add_trace(go.Scatter(x=df_2019_ABH_alb['lap'], y=df_2019_ABH_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2019_ABH_alb['color'])
))

fig2019_21.update_layout(layout)
fig2019_21.update_layout(title = '2019 Abu Dhabi Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# RACES: GRAPH OBJECTS

#fig2019_1 = go.Figure()
#df_2019_AUST['color']='#ffa007'
#indices_gasly = [0,1,3,6,10,15]
#df.loc[indices,'A'] = 16

# Defining Colors for each driver
indexRB_ver_20 = df_2020[(df_2020['code'] == 'VER')].index
df_2020.loc[indexRB_ver_20,'color'] = '#66c2a5'

indexRB_gasly_20 = df_2020[(df_2020['code'] == 'GAS')].index
df_2020.loc[indexRB_gasly_20,'color'] = '#fc8d62'

indexRB_albon_20 = df_2020[(df_2020['code'] == 'ALB')].index
df_2020.loc[indexRB_albon_20,'color'] = '#8da0cb'

indexRB_perez_20 = df_2020[(df_2020['code'] == 'PER')].index
df_2020.loc[indexRB_perez_20,'color'] = '#e78ac3'




# Austrian Grand Prix

df_2020_F_AUS = df_2020[(df_2020['name'] == 'Austrian Grand Prix')]
df_2020_AUS = df_2020_F_AUS.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_AUS = df_2020_AUS.sort_values(by="lap")



#fig25.add_trace(go.Scatter(x=df_2019_AUST['lap'], y=df_2019_AUST['seconds'],
 #                   mode='lines',
  #                  name='lines'))
#ver #ffa007
#gas #0035ff
#alb 00386b
df_2020_AUS_ver =df_2020_AUS[df_2020_AUS['code']=='VER']

df_2020_AUS_gas=df_2020_AUS[df_2020_AUS['code']=='GAS']

df_2020_AUS_alb =df_2020_AUS[df_2020_AUS['code']=='ALB']

df_2020_AUS_per =df_2020_AUS[df_2020_AUS['code']=='PER']

fig2020_1 = go.Figure()

fig2020_1.add_trace(go.Scatter(x=df_2020_AUS_ver['lap'], y=df_2020_AUS_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_AUS_ver['color'],
                           marker=dict(color=df_2020_AUS_ver['color'])
))
fig2020_1.add_trace(go.Scatter(x=df_2020_AUS_gas['lap'], y=df_2020_AUS_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_AUS_gas['color'],
                           marker=dict(color=df_2020_AUS_gas['color'])
))


fig2020_1.add_trace(go.Scatter(x=df_2020_AUS_alb['lap'], y=df_2020_AUS_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_AUS_alb['color'])
))

fig2020_1.add_trace(go.Scatter(x=df_2020_AUS_per['lap'], y=df_2020_AUS_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_AUS_per['color'])
))

fig2020_1.update_layout(layout)
fig2020_1.update_layout(title = '2020 Austrian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))

# Styrian Grand Prix

df_2020_F_STY = df_2020[(df_2020['name'] == 'Styrian Grand Prix')]
df_2020_STY = df_2020_F_STY.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_STY = df_2020_STY.sort_values(by="lap")

df_2020_STY_ver =df_2020_STY[df_2020_STY['code']=='VER']

df_2020_STY_gas=df_2020_STY[df_2020_STY['code']=='GAS']

df_2020_STY_alb =df_2020_STY[df_2020_STY['code']=='ALB']

df_2020_STY_per =df_2020_STY[df_2020_STY['code']=='PER']

fig2020_2 = go.Figure()

fig2020_2.add_trace(go.Scatter(x=df_2020_STY_ver['lap'], y=df_2020_STY_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_STY_ver['color'],
                           marker=dict(color=df_2020_STY_ver['color'])
))
fig2020_2.add_trace(go.Scatter(x=df_2020_STY_gas['lap'], y=df_2020_STY_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_STY_gas['color'],
                           marker=dict(color=df_2020_STY_gas['color'])
))


fig2020_2.add_trace(go.Scatter(x=df_2020_STY_alb['lap'], y=df_2020_STY_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_STY_alb['color'])
))

fig2020_2.add_trace(go.Scatter(x=df_2020_STY_per['lap'], y=df_2020_STY_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_STY_per['color'])
))

fig2020_2.update_layout(layout)
fig2020_2.update_layout(title = '2020 Styrian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Hungarian Grand Prix

df_2020_F_HUN = df_2020[(df_2020['name'] == 'Hungarian Grand Prix')]
df_2020_HUN = df_2020_F_HUN.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_HUN = df_2020_HUN.sort_values(by="lap")

df_2020_HUN_ver =df_2020_HUN[df_2020_HUN['code']=='VER']

df_2020_HUN_gas=df_2020_HUN[df_2020_HUN['code']=='GAS']

df_2020_HUN_alb =df_2020_HUN[df_2020_HUN['code']=='ALB']

df_2020_HUN_per =df_2020_HUN[df_2020_HUN['code']=='PER']

fig2020_3 = go.Figure()

fig2020_3.add_trace(go.Scatter(x=df_2020_HUN_ver['lap'], y=df_2020_HUN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_HUN_ver['color'],
                           marker=dict(color=df_2020_HUN_ver['color'])
))
fig2020_3.add_trace(go.Scatter(x=df_2020_HUN_gas['lap'], y=df_2020_HUN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_HUN_gas['color'],
                           marker=dict(color=df_2020_HUN_gas['color'])
))


fig2020_3.add_trace(go.Scatter(x=df_2020_HUN_alb['lap'], y=df_2020_HUN_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_HUN_alb['color'])
))

fig2020_3.add_trace(go.Scatter(x=df_2020_HUN_per['lap'], y=df_2020_HUN_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_HUN_per['color'])
))

fig2020_3.update_layout(layout)
fig2020_3.update_layout(title = '2020 Hungarian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# British Grand Prix

df_2020_F_BRIT = df_2020[(df_2020['name'] == 'British Grand Prix')]
df_2020_BRIT = df_2020_F_BRIT.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_BRIT = df_2020_BRIT.sort_values(by="lap")

df_2020_BRIT_ver =df_2020_BRIT[df_2020_BRIT['code']=='VER']

df_2020_BRIT_gas=df_2020_BRIT[df_2020_BRIT['code']=='GAS']

df_2020_BRIT_alb =df_2020_BRIT[df_2020_BRIT['code']=='ALB']

df_2020_BRIT_per =df_2020_BRIT[df_2020_BRIT['code']=='PER']

fig2020_4 = go.Figure()

fig2020_4.add_trace(go.Scatter(x=df_2020_BRIT_ver['lap'], y=df_2020_BRIT_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_BRIT_ver['color'],
                           marker=dict(color=df_2020_BRIT_ver['color'])
))
fig2020_4.add_trace(go.Scatter(x=df_2020_BRIT_gas['lap'], y=df_2020_BRIT_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_BRIT_gas['color'],
                           marker=dict(color=df_2020_BRIT_gas['color'])
))


fig2020_4.add_trace(go.Scatter(x=df_2020_BRIT_alb['lap'], y=df_2020_BRIT_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_BRIT_alb['color'])
))

fig2020_4.add_trace(go.Scatter(x=df_2020_BRIT_per['lap'], y=df_2020_BRIT_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_BRIT_per['color'])
))

fig2020_4.update_layout(layout)
fig2020_4.update_layout(title = '2020 British Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# 70th Anniversary Grand Prix

df_2020_F_70TH = df_2020[(df_2020['name'] == '70th Anniversary Grand Prix')]
df_2020_70TH = df_2020_F_70TH.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_70TH = df_2020_70TH.sort_values(by="lap")

df_2020_70TH_ver =df_2020_70TH[df_2020_70TH['code']=='VER']

df_2020_70TH_gas=df_2020_70TH[df_2020_70TH['code']=='GAS']

df_2020_70TH_alb =df_2020_70TH[df_2020_70TH['code']=='ALB']

df_2020_70TH_per =df_2020_70TH[df_2020_70TH['code']=='PER']

fig2020_5 = go.Figure()

fig2020_5.add_trace(go.Scatter(x=df_2020_70TH_ver['lap'], y=df_2020_70TH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_70TH_ver['color'],
                           marker=dict(color=df_2020_70TH_ver['color'])
))
fig2020_5.add_trace(go.Scatter(x=df_2020_70TH_gas['lap'], y=df_2020_70TH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_70TH_gas['color'],
                           marker=dict(color=df_2020_70TH_gas['color'])
))


fig2020_5.add_trace(go.Scatter(x=df_2020_70TH_alb['lap'], y=df_2020_70TH_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_70TH_alb['color'])
))

fig2020_5.add_trace(go.Scatter(x=df_2020_70TH_per['lap'], y=df_2020_70TH_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_70TH_per['color'])
))

fig2020_5.update_layout(layout)
fig2020_5.update_layout(title = '2020 70th Anniversary Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Spanish Grand Prix

df_2020_F_ESP = df_2020[(df_2020['name'] == 'Spanish Grand Prix')]
df_2020_ESP = df_2020_F_ESP.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_ESP = df_2020_ESP.sort_values(by="lap")

df_2020_ESP_ver =df_2020_ESP[df_2020_ESP['code']=='VER']

df_2020_ESP_gas=df_2020_ESP[df_2020_ESP['code']=='GAS']

df_2020_ESP_alb =df_2020_ESP[df_2020_ESP['code']=='ALB']

df_2020_ESP_per =df_2020_ESP[df_2020_ESP['code']=='PER']

fig2020_6 = go.Figure()

fig2020_6.add_trace(go.Scatter(x=df_2020_ESP_ver['lap'], y=df_2020_ESP_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_ESP_ver['color'],
                           marker=dict(color=df_2020_ESP_ver['color'])
))
fig2020_6.add_trace(go.Scatter(x=df_2020_ESP_gas['lap'], y=df_2020_ESP_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_ESP_gas['color'],
                           marker=dict(color=df_2020_ESP_gas['color'])
))


fig2020_6.add_trace(go.Scatter(x=df_2020_ESP_alb['lap'], y=df_2020_ESP_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_ESP_alb['color'])
))

fig2020_6.add_trace(go.Scatter(x=df_2020_ESP_per['lap'], y=df_2020_ESP_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_ESP_per['color'])
))

fig2020_6.update_layout(layout)
fig2020_6.update_layout(title = '2020 Spanish Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Belgian Grand Prix

df_2020_F_BEL = df_2020[(df_2020['name'] == 'Belgian Grand Prix')]
df_2020_BEL = df_2020_F_BEL.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_BEL = df_2020_BEL.sort_values(by="lap")

df_2020_BEL_ver =df_2020_BEL[df_2020_BEL['code']=='VER']

df_2020_BEL_gas=df_2020_BEL[df_2020_BEL['code']=='GAS']

df_2020_BEL_alb =df_2020_BEL[df_2020_BEL['code']=='ALB']

df_2020_BEL_per =df_2020_BEL[df_2020_BEL['code']=='PER']

fig2020_7 = go.Figure()

fig2020_7.add_trace(go.Scatter(x=df_2020_BEL_ver['lap'], y=df_2020_BEL_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_BEL_ver['color'],
                           marker=dict(color=df_2020_BEL_ver['color'])
))
fig2020_7.add_trace(go.Scatter(x=df_2020_BEL_gas['lap'], y=df_2020_BEL_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_BEL_gas['color'],
                           marker=dict(color=df_2020_BEL_gas['color'])
))


fig2020_7.add_trace(go.Scatter(x=df_2020_BEL_alb['lap'], y=df_2020_BEL_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_BEL_alb['color'])
))

fig2020_7.add_trace(go.Scatter(x=df_2020_BEL_per['lap'], y=df_2020_BEL_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_BEL_per['color'])
))

fig2020_7.update_layout(layout)
fig2020_7.update_layout(title = '2020 Belgian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Italian Grand Prix

df_2020_F_ITA = df_2020[(df_2020['name'] == 'Italian Grand Prix')]
df_2020_ITA = df_2020_F_ITA.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_ITA = df_2020_ITA.sort_values(by="lap")

df_2020_ITA_ver =df_2020_ITA[df_2020_ITA['code']=='VER']

df_2020_ITA_gas=df_2020_ITA[df_2020_ITA['code']=='GAS']

df_2020_ITA_alb =df_2020_ITA[df_2020_ITA['code']=='ALB']

df_2020_ITA_per =df_2020_ITA[df_2020_ITA['code']=='PER']

fig2020_8 = go.Figure()

fig2020_8.add_trace(go.Scatter(x=df_2020_ITA_ver['lap'], y=df_2020_ITA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_ITA_ver['color'],
                           marker=dict(color=df_2020_ITA_ver['color'])
))
fig2020_8.add_trace(go.Scatter(x=df_2020_ITA_gas['lap'], y=df_2020_ITA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_ITA_gas['color'],
                           marker=dict(color=df_2020_ITA_gas['color'])
))


fig2020_8.add_trace(go.Scatter(x=df_2020_ITA_alb['lap'], y=df_2020_ITA_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_ITA_alb['color'])
))

fig2020_8.add_trace(go.Scatter(x=df_2020_ITA_per['lap'], y=df_2020_ITA_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_ITA_per['color'])
))

fig2020_8.update_layout(layout)
fig2020_8.update_layout(title = '2020 Italian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Tuscan Grand Prix

df_2020_F_TUS = df_2020[(df_2020['name'] == 'Tuscan Grand Prix')]
df_2020_TUS = df_2020_F_TUS.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_TUS = df_2020_TUS.sort_values(by="lap")

df_2020_TUS_ver =df_2020_TUS[df_2020_TUS['code']=='VER']

df_2020_TUS_gas=df_2020_TUS[df_2020_TUS['code']=='GAS']

df_2020_TUS_alb =df_2020_TUS[df_2020_TUS['code']=='ALB']

df_2020_TUS_per =df_2020_TUS[df_2020_TUS['code']=='PER']

fig2020_9 = go.Figure()

fig2020_9.add_trace(go.Scatter(x=df_2020_TUS_ver['lap'], y=df_2020_TUS_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_TUS_ver['color'],
                           marker=dict(color=df_2020_TUS_ver['color'])
))
fig2020_9.add_trace(go.Scatter(x=df_2020_TUS_gas['lap'], y=df_2020_TUS_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_TUS_gas['color'],
                           marker=dict(color=df_2020_TUS_gas['color'])
))


fig2020_9.add_trace(go.Scatter(x=df_2020_TUS_alb['lap'], y=df_2020_TUS_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_TUS_alb['color'])
))

fig2020_9.add_trace(go.Scatter(x=df_2020_TUS_per['lap'], y=df_2020_TUS_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_TUS_per['color'])
))

fig2020_9.update_layout(layout)
fig2020_9.update_layout(title = '2020 Tuscan Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Russian Grand Prix

df_2020_F_RUS = df_2020[(df_2020['name'] == 'Russian Grand Prix')]
df_2020_RUS = df_2020_F_RUS.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_RUS = df_2020_RUS.sort_values(by="lap")


df_2020_RUS_ver =df_2020_RUS[df_2020_RUS['code']=='VER']

df_2020_RUS_gas=df_2020_RUS[df_2020_RUS['code']=='GAS']

df_2020_RUS_alb =df_2020_RUS[df_2020_RUS['code']=='ALB']

df_2020_RUS_per =df_2020_RUS[df_2020_RUS['code']=='PER']

fig2020_10 = go.Figure()

fig2020_10.add_trace(go.Scatter(x=df_2020_RUS_ver['lap'], y=df_2020_RUS_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_RUS_ver['color'],
                           marker=dict(color=df_2020_RUS_ver['color'])
))
fig2020_10.add_trace(go.Scatter(x=df_2020_RUS_gas['lap'], y=df_2020_RUS_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_RUS_gas['color'],
                           marker=dict(color=df_2020_RUS_gas['color'])
))


fig2020_10.add_trace(go.Scatter(x=df_2020_RUS_alb['lap'], y=df_2020_RUS_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_RUS_alb['color'])
))

fig2020_10.add_trace(go.Scatter(x=df_2020_RUS_per['lap'], y=df_2020_RUS_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_RUS_per['color'])
))

fig2020_10.update_layout(layout)
fig2020_10.update_layout(title = '2020 Russian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Eifel Grand Prix

df_2020_F_EIF = df_2020[(df_2020['name'] == 'Eifel Grand Prix')]
df_2020_EIF = df_2020_F_EIF.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_EIF = df_2020_EIF.sort_values(by="lap")

df_2020_EIF_ver =df_2020_EIF[df_2020_EIF['code']=='VER']

df_2020_EIF_gas=df_2020_EIF[df_2020_EIF['code']=='GAS']

df_2020_EIF_alb =df_2020_EIF[df_2020_EIF['code']=='ALB']

df_2020_EIF_per =df_2020_EIF[df_2020_EIF['code']=='PER']

fig2020_11 = go.Figure()

fig2020_11.add_trace(go.Scatter(x=df_2020_EIF_ver['lap'], y=df_2020_EIF_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_EIF_ver['color'],
                           marker=dict(color=df_2020_EIF_ver['color'])
))
fig2020_11.add_trace(go.Scatter(x=df_2020_EIF_gas['lap'], y=df_2020_EIF_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_EIF_gas['color'],
                           marker=dict(color=df_2020_EIF_gas['color'])
))


fig2020_11.add_trace(go.Scatter(x=df_2020_EIF_alb['lap'], y=df_2020_EIF_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_EIF_alb['color'])
))

fig2020_11.add_trace(go.Scatter(x=df_2020_EIF_per['lap'], y=df_2020_EIF_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_EIF_per['color'])
))

fig2020_11.update_layout(layout)
fig2020_11.update_layout(title = '2020 Eifel Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Portuguese Grand Prix

df_2020_F_POR = df_2020[(df_2020['name'] == 'Portuguese Grand Prix')]
df_2020_POR = df_2020_F_POR.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_POR = df_2020_POR.sort_values(by="lap")

df_2020_POR_ver =df_2020_POR[df_2020_POR['code']=='VER']

df_2020_POR_gas=df_2020_POR[df_2020_POR['code']=='GAS']

df_2020_POR_alb =df_2020_POR[df_2020_POR['code']=='ALB']

df_2020_POR_per =df_2020_POR[df_2020_POR['code']=='PER']

fig2020_12 = go.Figure()

fig2020_12.add_trace(go.Scatter(x=df_2020_POR_ver['lap'], y=df_2020_POR_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_POR_ver['color'],
                           marker=dict(color=df_2020_POR_ver['color'])
))
fig2020_12.add_trace(go.Scatter(x=df_2020_POR_gas['lap'], y=df_2020_POR_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_POR_gas['color'],
                           marker=dict(color=df_2020_POR_gas['color'])
))


fig2020_12.add_trace(go.Scatter(x=df_2020_POR_alb['lap'], y=df_2020_POR_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_POR_alb['color'])
))

fig2020_12.add_trace(go.Scatter(x=df_2020_POR_per['lap'], y=df_2020_POR_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_POR_per['color'])
))

fig2020_12.update_layout(layout)
fig2020_12.update_layout(title = '2020 Portuguese Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Emilia Romagna Grand Prix

df_2020_F_EMI = df_2020[(df_2020['name'] == 'Emilia Romagna Grand Prix')]
df_2020_EMI = df_2020_F_EMI.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_EMI = df_2020_EMI.sort_values(by="lap")


df_2020_EMI_ver =df_2020_EMI[df_2020_EMI['code']=='VER']

df_2020_EMI_gas=df_2020_EMI[df_2020_EMI['code']=='GAS']

df_2020_EMI_alb =df_2020_EMI[df_2020_EMI['code']=='ALB']

df_2020_EMI_per =df_2020_EMI[df_2020_EMI['code']=='PER']

fig2020_13 = go.Figure()

fig2020_13.add_trace(go.Scatter(x=df_2020_EMI_ver['lap'], y=df_2020_EMI_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_EMI_ver['color'],
                           marker=dict(color=df_2020_EMI_ver['color'])
))
fig2020_13.add_trace(go.Scatter(x=df_2020_EMI_gas['lap'], y=df_2020_EMI_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_EMI_gas['color'],
                           marker=dict(color=df_2020_EMI_gas['color'])
))


fig2020_13.add_trace(go.Scatter(x=df_2020_EMI_alb['lap'], y=df_2020_EMI_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_EMI_alb['color'])
))

fig2020_13.add_trace(go.Scatter(x=df_2020_EMI_per['lap'], y=df_2020_EMI_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_EMI_per['color'])
))

fig2020_13.update_layout(layout)
fig2020_13.update_layout(title = '2020 Emilia Romagna Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Turkish Grand Prix

df_2020_F_TUR = df_2020[(df_2020['name'] == 'Turkish Grand Prix')]
df_2020_TUR = df_2020_F_TUR.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_TUR = df_2020_TUR.sort_values(by="lap")

df_2020_TUR_ver =df_2020_TUR[df_2020_TUR['code']=='VER']

df_2020_TUR_gas=df_2020_TUR[df_2020_TUR['code']=='GAS']

df_2020_TUR_alb =df_2020_TUR[df_2020_TUR['code']=='ALB']

df_2020_TUR_per =df_2020_TUR[df_2020_TUR['code']=='PER']

fig2020_14 = go.Figure()

fig2020_14.add_trace(go.Scatter(x=df_2020_TUR_ver['lap'], y=df_2020_TUR_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_TUR_ver['color'],
                           marker=dict(color=df_2020_TUR_ver['color'])
))
fig2020_14.add_trace(go.Scatter(x=df_2020_TUR_gas['lap'], y=df_2020_TUR_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_TUR_gas['color'],
                           marker=dict(color=df_2020_TUR_gas['color'])
))


fig2020_14.add_trace(go.Scatter(x=df_2020_TUR_alb['lap'], y=df_2020_TUR_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_TUR_alb['color'])
))

fig2020_14.add_trace(go.Scatter(x=df_2020_TUR_per['lap'], y=df_2020_TUR_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_TUR_per['color'])
))

fig2020_14.update_layout(layout)
fig2020_14.update_layout(title = '2020 Turkish Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Bahrain Grand Prix

df_2020_F_BAH = df_2020[(df_2020['name'] == 'Bahrain Grand Prix')]
df_2020_BAH = df_2020_F_BAH.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_BAH = df_2020_BAH.sort_values(by="lap")

df_2020_BAH_ver =df_2020_BAH[df_2020_BAH['code']=='VER']

df_2020_BAH_gas=df_2020_BAH[df_2020_BAH['code']=='GAS']

df_2020_BAH_alb =df_2020_BAH[df_2020_BAH['code']=='ALB']

df_2020_BAH_per =df_2020_BAH[df_2020_BAH['code']=='PER']

fig2020_15 = go.Figure()

fig2020_15.add_trace(go.Scatter(x=df_2020_BAH_ver['lap'], y=df_2020_BAH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_BAH_ver['color'],
                           marker=dict(color=df_2020_BAH_ver['color'])
))
fig2020_15.add_trace(go.Scatter(x=df_2020_BAH_gas['lap'], y=df_2020_BAH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_BAH_gas['color'],
                           marker=dict(color=df_2020_BAH_gas['color'])
))


fig2020_15.add_trace(go.Scatter(x=df_2020_BAH_alb['lap'], y=df_2020_BAH_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_BAH_alb['color'])
))

fig2020_15.add_trace(go.Scatter(x=df_2020_BAH_per['lap'], y=df_2020_BAH_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_BAH_per['color'])
))

fig2020_15.update_layout(layout)
fig2020_15.update_layout(title = '2020 Bahrain Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Sakhir Grand Prix

df_2020_F_SAK = df_2020[(df_2020['name'] == 'Sakhir Grand Prix')]
df_2020_SAK = df_2020_F_SAK.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_SAK = df_2020_SAK.sort_values(by="lap")


df_2020_SAK_ver =df_2020_SAK[df_2020_SAK['code']=='VER']

df_2020_SAK_gas=df_2020_SAK[df_2020_SAK['code']=='GAS']

df_2020_SAK_alb =df_2020_SAK[df_2020_SAK['code']=='ALB']

df_2020_SAK_per =df_2020_SAK[df_2020_SAK['code']=='PER']

fig2020_16 = go.Figure()

fig2020_16.add_trace(go.Scatter(x=df_2020_SAK_ver['lap'], y=df_2020_SAK_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_SAK_ver['color'],
                           marker=dict(color=df_2020_SAK_ver['color'])
))
fig2020_16.add_trace(go.Scatter(x=df_2020_SAK_gas['lap'], y=df_2020_SAK_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_SAK_gas['color'],
                           marker=dict(color=df_2020_SAK_gas['color'])
))


fig2020_16.add_trace(go.Scatter(x=df_2020_SAK_alb['lap'], y=df_2020_SAK_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_SAK_alb['color'])
))

fig2020_16.add_trace(go.Scatter(x=df_2020_SAK_per['lap'], y=df_2020_SAK_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_SAK_per['color'])
))

fig2020_16.update_layout(layout)
fig2020_16.update_layout(title = '2020 Sakhir Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Abu Dhabi Grand Prix

df_2020_F_ABH = df_2020[(df_2020['name'] == 'Abu Dhabi Grand Prix')]
df_2020_ABH  = df_2020_F_ABH.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2020_ABH  = df_2020_ABH.sort_values(by="lap")

df_2020_ABH_ver =df_2020_ABH[df_2020_ABH['code']=='VER']

df_2020_ABH_gas=df_2020_ABH[df_2020_ABH['code']=='GAS']

df_2020_ABH_alb =df_2020_ABH[df_2020_ABH['code']=='ALB']

df_2020_ABH_per =df_2020_ABH[df_2020_ABH['code']=='PER']

fig2020_17 = go.Figure()

fig2020_17.add_trace(go.Scatter(x=df_2020_ABH_ver['lap'], y=df_2020_ABH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2020_ABH_ver['color'],
                           marker=dict(color=df_2020_ABH_ver['color'])
))
fig2020_17.add_trace(go.Scatter(x=df_2020_ABH_gas['lap'], y=df_2020_ABH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2020_ABH_gas['color'],
                           marker=dict(color=df_2020_ABH_gas['color'])
))


fig2020_17.add_trace(go.Scatter(x=df_2020_ABH_alb['lap'], y=df_2020_ABH_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2020_ABH_alb['color'])
))

fig2020_17.add_trace(go.Scatter(x=df_2020_ABH_per['lap'], y=df_2020_ABH_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2020_ABH_per['color'])
))

fig2020_17.update_layout(layout)
fig2020_17.update_layout(title = '2020 Abu Dhabi Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# RACES: GRAPH OBJECTS


# Defining Colors for each driver
indexRB_ver_21 = df_2021[(df_2021['code'] == 'VER')].index
df_2021.loc[indexRB_ver_21,'color'] = '#66c2a5'

indexRB_gasly_21 = df_2021[(df_2021['code'] == 'GAS')].index
df_2021.loc[indexRB_gasly_21,'color'] = '#fc8d62'


indexRB_perez_21 = df_2021[(df_2021['code'] == 'PER')].index
df_2021.loc[indexRB_perez_21,'color'] = '#e78ac3'


# Bahrain Grand Prix (1)

df_2021_F_BAH = df_2021[(df_2021['name'] == 'Bahrain Grand Prix')]
df_2021_BAH = df_2021_F_BAH.query("driverRef in ['gasly', 'max_verstappen','perez']")
df_2021_BAH = df_2021_BAH.sort_values(by="lap")

df_2021_BAH_ver =df_2021_BAH[df_2021_BAH['code']=='VER']

df_2021_BAH_gas=df_2021_BAH[df_2021_BAH['code']=='GAS']

df_2021_BAH_per =df_2021_BAH[df_2021_BAH['code']=='PER']

fig2021_1 = go.Figure()

fig2021_1.add_trace(go.Scatter(x=df_2021_BAH_ver['lap'], y=df_2021_BAH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_BAH_ver['color'],
                           marker=dict(color=df_2021_BAH_ver['color'])
))
fig2021_1.add_trace(go.Scatter(x=df_2021_BAH_gas['lap'], y=df_2021_BAH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_BAH_gas['color'],
                           marker=dict(color=df_2021_BAH_gas['color'])
))

fig2021_1.add_trace(go.Scatter(x=df_2021_BAH_per['lap'], y=df_2021_BAH_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_BAH_per['color'],
                           marker=dict(color=df_2021_BAH_per['color'])
))

fig2021_1.update_layout(layout)
fig2021_1.update_layout(title = '2021 Bahrain Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Emilia Romagna Grand Prix (2)

df_2021_F_EMI = df_2021[(df_2021['name'] == 'Emilia Romagna Grand Prix')]
df_2021_EMI = df_2021_F_EMI.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_EMI = df_2021_EMI.sort_values(by="lap")

df_2021_EMI_ver =df_2021_EMI[df_2021_EMI['code']=='VER']

df_2021_EMI_gas=df_2021_EMI[df_2021_EMI['code']=='GAS']

df_2021_EMI_per =df_2021_EMI[df_2021_EMI['code']=='PER']

fig2021_2 = go.Figure()

fig2021_2.add_trace(go.Scatter(x=df_2021_EMI_ver['lap'], y=df_2021_EMI_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_EMI_ver['color'],
                           marker=dict(color=df_2021_EMI_ver['color'])
))
fig2021_2.add_trace(go.Scatter(x=df_2021_EMI_gas['lap'], y=df_2021_EMI_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_EMI_gas['color'],
                           marker=dict(color=df_2021_EMI_gas['color'])
))

fig2021_2.add_trace(go.Scatter(x=df_2021_EMI_per['lap'], y=df_2021_EMI_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_EMI_per['color'],
                           marker=dict(color=df_2021_EMI_per['color'])
))

fig2021_2.update_layout(layout)
fig2021_2.update_layout(title = '2021 Emilia Romagna Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Portuguese Grand Prix (3)

df_2021_F_POR = df_2021[(df_2021['name'] == 'Portuguese Grand Prix')]
df_2021_POR = df_2021_F_POR.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_POR = df_2021_POR.sort_values(by="lap")

df_2021_POR_ver =df_2021_POR[df_2021_POR['code']=='VER']

df_2021_POR_gas=df_2021_POR[df_2021_POR['code']=='GAS']

df_2021_POR_per =df_2021_POR[df_2021_POR['code']=='PER']

fig2021_3 = go.Figure()

fig2021_3.add_trace(go.Scatter(x=df_2021_POR_ver['lap'], y=df_2021_POR_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_POR_ver['color'],
                           marker=dict(color=df_2021_POR_ver['color'])
))
fig2021_3.add_trace(go.Scatter(x=df_2021_POR_gas['lap'], y=df_2021_POR_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_POR_gas['color'],
                           marker=dict(color=df_2021_POR_gas['color'])
))

fig2021_3.add_trace(go.Scatter(x=df_2021_POR_per['lap'], y=df_2021_POR_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_POR_per['color'],
                           marker=dict(color=df_2021_POR_per['color'])
))

fig2021_3.update_layout(layout)
fig2021_3.update_layout(title = '2021 Portuguese Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))





# Spanish Grand Prix (4)

df_2021_F_ESP = df_2021[(df_2021['name'] == 'Spanish Grand Prix')]
df_2021_ESP = df_2021_F_ESP.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_ESP = df_2021_ESP.sort_values(by="lap")

df_2021_ESP_ver =df_2021_ESP[df_2021_ESP['code']=='VER']

df_2021_ESP_gas=df_2021_ESP[df_2021_ESP['code']=='GAS']

df_2021_ESP_per =df_2021_ESP[df_2021_ESP['code']=='PER']

fig2021_4 = go.Figure()

fig2021_4.add_trace(go.Scatter(x=df_2021_ESP_ver['lap'], y=df_2021_ESP_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_ESP_ver['color'],
                           marker=dict(color=df_2021_ESP_ver['color'])
))
fig2021_4.add_trace(go.Scatter(x=df_2021_ESP_gas['lap'], y=df_2021_ESP_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_ESP_gas['color'],
                           marker=dict(color=df_2021_ESP_gas['color'])
))

fig2021_4.add_trace(go.Scatter(x=df_2021_ESP_per['lap'], y=df_2021_ESP_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_ESP_per['color'],
                           marker=dict(color=df_2021_ESP_per['color'])
))

fig2021_4.update_layout(layout)
fig2021_4.update_layout(title = '2021 Spanish Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Monaco Grand Prix (5)

df_2021_F_MON = df_2021[(df_2021['name'] == 'Monaco Grand Prix')]
df_2021_MON = df_2021_F_MON.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_MON = df_2021_MON.sort_values(by="lap")

df_2021_MON_ver =df_2021_MON[df_2021_MON['code']=='VER']

df_2021_MON_gas=df_2021_MON[df_2021_MON['code']=='GAS']

df_2021_MON_per =df_2021_MON[df_2021_MON['code']=='PER']

fig2021_5 = go.Figure()

fig2021_5.add_trace(go.Scatter(x=df_2021_MON_ver['lap'], y=df_2021_MON_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_MON_ver['color'],
                           marker=dict(color=df_2021_MON_ver['color'])
))
fig2021_5.add_trace(go.Scatter(x=df_2021_MON_gas['lap'], y=df_2021_MON_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_MON_gas['color'],
                           marker=dict(color=df_2021_MON_gas['color'])
))

fig2021_5.add_trace(go.Scatter(x=df_2021_MON_per['lap'], y=df_2021_MON_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_MON_per['color'],
                           marker=dict(color=df_2021_MON_per['color'])
))

fig2021_5.update_layout(layout)
fig2021_5.update_layout(title = '2021 Monaco Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Azerbaijan Grand Prix (6)

df_2021_F_AZB = df_2021[(df_2021['name'] == 'Azerbaijan Grand Prix')]
df_2021_AZB = df_2021_F_AZB.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_AZB = df_2021_AZB.sort_values(by="lap")

df_2021_AZB_ver =df_2021_AZB[df_2021_AZB['code']=='VER']

df_2021_AZB_gas=df_2021_AZB[df_2021_AZB['code']=='GAS']

df_2021_AZB_per =df_2021_AZB[df_2021_AZB['code']=='PER']

fig2021_6 = go.Figure()

fig2021_6.add_trace(go.Scatter(x=df_2021_AZB_ver['lap'], y=df_2021_AZB_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_AZB_ver['color'],
                           marker=dict(color=df_2021_AZB_ver['color'])
))
fig2021_6.add_trace(go.Scatter(x=df_2021_AZB_gas['lap'], y=df_2021_AZB_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_AZB_gas['color'],
                           marker=dict(color=df_2021_AZB_gas['color'])
))

fig2021_6.add_trace(go.Scatter(x=df_2021_AZB_per['lap'], y=df_2021_AZB_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_AZB_per['color'],
                           marker=dict(color=df_2021_AZB_per['color'])
))

fig2021_6.update_layout(layout)
fig2021_6.update_layout(title = '2021 Azerbaijan Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# French Grand Prix (7)

df_2021_F_FRA = df_2021[(df_2021['name'] == 'French Grand Prix')]
df_2021_FRA = df_2021_F_FRA.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_FRA = df_2021_FRA.sort_values(by="lap")

df_2021_FRA_ver =df_2021_FRA[df_2021_FRA['code']=='VER']

df_2021_FRA_gas=df_2021_FRA[df_2021_FRA['code']=='GAS']

df_2021_FRA_per =df_2021_FRA[df_2021_FRA['code']=='PER']

fig2021_7 = go.Figure()

fig2021_7.add_trace(go.Scatter(x=df_2021_FRA_ver['lap'], y=df_2021_FRA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_FRA_ver['color'],
                           marker=dict(color=df_2021_FRA_ver['color'])
))
fig2021_7.add_trace(go.Scatter(x=df_2021_FRA_gas['lap'], y=df_2021_FRA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_FRA_gas['color'],
                           marker=dict(color=df_2021_FRA_gas['color'])
))

fig2021_7.add_trace(go.Scatter(x=df_2021_FRA_per['lap'], y=df_2021_FRA_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_FRA_per['color'],
                           marker=dict(color=df_2021_FRA_per['color'])
))

fig2021_7.update_layout(layout)
fig2021_7.update_layout(title = '2021 French Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Styrian Grand Prix (8)

df_2021_F_STY = df_2021[(df_2021['name'] == 'Styrian Grand Prix')]
df_2021_STY = df_2021_F_STY.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_STY = df_2021_STY.sort_values(by="lap")

df_2021_STY_ver =df_2021_STY[df_2021_STY['code']=='VER']

df_2021_STY_gas=df_2021_STY[df_2021_STY['code']=='GAS']

df_2021_STY_per =df_2021_STY[df_2021_STY['code']=='PER']

fig2021_8 = go.Figure()

fig2021_8.add_trace(go.Scatter(x=df_2021_STY_ver['lap'], y=df_2021_STY_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_STY_ver['color'],
                           marker=dict(color=df_2021_STY_ver['color'])
))
fig2021_8.add_trace(go.Scatter(x=df_2021_STY_gas['lap'], y=df_2021_STY_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_STY_gas['color'],
                           marker=dict(color=df_2021_STY_gas['color'])
))

fig2021_8.add_trace(go.Scatter(x=df_2021_STY_per['lap'], y=df_2021_STY_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_STY_per['color'],
                           marker=dict(color=df_2021_STY_per['color'])
))

fig2021_8.update_layout(layout)
fig2021_8.update_layout(title = '2021 Styrian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Austrian Grand Prix (9)

df_2021_F_AUS = df_2021[(df_2021['name'] == 'Austrian Grand Prix')]
df_2021_AUS = df_2021_F_AUS.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_AUS = df_2021_AUS.sort_values(by="lap")

df_2021_AUS_ver =df_2021_AUS[df_2021_AUS['code']=='VER']

df_2021_AUS_gas=df_2021_AUS[df_2021_AUS['code']=='GAS']

df_2021_AUS_per =df_2021_AUS[df_2021_AUS['code']=='PER']

fig2021_9 = go.Figure()

fig2021_9.add_trace(go.Scatter(x=df_2021_AUS_ver['lap'], y=df_2021_AUS_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_AUS_ver['color'],
                           marker=dict(color=df_2021_AUS_ver['color'])
))
fig2021_9.add_trace(go.Scatter(x=df_2021_AUS_gas['lap'], y=df_2021_AUS_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_AUS_gas['color'],
                           marker=dict(color=df_2021_AUS_gas['color'])
))

fig2021_9.add_trace(go.Scatter(x=df_2021_AUS_per['lap'], y=df_2021_AUS_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_AUS_per['color'],
                           marker=dict(color=df_2021_AUS_per['color'])
))

fig2021_9.update_layout(layout)
fig2021_9.update_layout(title = '2021 Austrian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))





# British Grand Prix (10)

df_2021_F_BRIT = df_2021[(df_2021['name'] == 'British Grand Prix')]
df_2021_BRIT = df_2021_F_BRIT.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_BRIT = df_2021_BRIT.sort_values(by="lap")

df_2021_BRIT_ver =df_2021_BRIT[df_2021_BRIT['code']=='VER']

df_2021_BRIT_gas=df_2021_BRIT[df_2021_BRIT['code']=='GAS']

df_2021_BRIT_per =df_2021_BRIT[df_2021_BRIT['code']=='PER']

fig2021_10 = go.Figure()

fig2021_10.add_trace(go.Scatter(x=df_2021_BRIT_ver['lap'], y=df_2021_BRIT_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_BRIT_ver['color'],
                           marker=dict(color=df_2021_BRIT_ver['color'])
))
fig2021_10.add_trace(go.Scatter(x=df_2021_BRIT_gas['lap'], y=df_2021_BRIT_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_BRIT_gas['color'],
                           marker=dict(color=df_2021_BRIT_gas['color'])
))

fig2021_10.add_trace(go.Scatter(x=df_2021_BRIT_per['lap'], y=df_2021_BRIT_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_BRIT_per['color'],
                           marker=dict(color=df_2021_BRIT_per['color'])
))

fig2021_10.update_layout(layout)
fig2021_10.update_layout(title = '2021 British Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Hungarian Grand Prix (11)

df_2021_F_HUN = df_2021[(df_2021['name'] == 'Hungarian Grand Prix')]
df_2021_HUN = df_2021_F_HUN.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_HUN = df_2021_HUN.sort_values(by="lap")

df_2021_HUN_ver =df_2021_HUN[df_2021_HUN['code']=='VER']

df_2021_HUN_gas=df_2021_HUN[df_2021_HUN['code']=='GAS']

df_2021_HUN_per =df_2021_HUN[df_2021_HUN['code']=='PER']

fig2021_11 = go.Figure()

fig2021_11.add_trace(go.Scatter(x=df_2021_HUN_ver['lap'], y=df_2021_HUN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_HUN_ver['color'],
                           marker=dict(color=df_2021_HUN_ver['color'])
))
fig2021_11.add_trace(go.Scatter(x=df_2021_HUN_gas['lap'], y=df_2021_HUN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_HUN_gas['color'],
                           marker=dict(color=df_2021_HUN_gas['color'])
))

fig2021_11.add_trace(go.Scatter(x=df_2021_HUN_per['lap'], y=df_2021_HUN_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_HUN_per['color'],
                           marker=dict(color=df_2021_HUN_per['color'])
))

fig2021_11.update_layout(layout)
fig2021_11.update_layout(title = '2021 Hungarian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Belgian Grand Prix (12)

df_2021_F_BEL = df_2021[(df_2021['name'] == 'Belgian Grand Prix')]
df_2021_BEL = df_2021_F_BEL.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_BEL = df_2021_BEL.sort_values(by="lap")

df_2021_BEL_ver =df_2021_BEL[df_2021_BEL['code']=='VER']

df_2021_BEL_gas=df_2021_BEL[df_2021_BEL['code']=='GAS']

df_2021_BEL_per =df_2021_BEL[df_2021_BEL['code']=='PER']

fig2021_12 = go.Figure()

fig2021_12.add_trace(go.Scatter(x=df_2021_BEL_ver['lap'], y=df_2021_BEL_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_BEL_ver['color'],
                           marker=dict(color=df_2021_BEL_ver['color'])
))
fig2021_12.add_trace(go.Scatter(x=df_2021_BEL_gas['lap'], y=df_2021_BEL_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_BEL_gas['color'],
                           marker=dict(color=df_2021_BEL_gas['color'])
))

fig2021_12.add_trace(go.Scatter(x=df_2021_BEL_per['lap'], y=df_2021_BEL_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_BEL_per['color'],
                           marker=dict(color=df_2021_BEL_per['color'])
))

fig2021_12.update_layout(layout)
fig2021_12.update_layout(title = '2021 Belgian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))





# Dutch Grand Prix (13)

df_2021_F_NED = df_2021[(df_2021['name'] == 'Dutch Grand Prix')]
df_2021_NED = df_2021_F_NED.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_NED = df_2021_NED.sort_values(by="lap")


df_2021_NED_ver =df_2021_NED[df_2021_NED['code']=='VER']

df_2021_NED_gas=df_2021_NED[df_2021_NED['code']=='GAS']

df_2021_NED_per =df_2021_NED[df_2021_NED['code']=='PER']

fig2021_13 = go.Figure()

fig2021_13.add_trace(go.Scatter(x=df_2021_NED_ver['lap'], y=df_2021_NED_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_NED_ver['color'],
                           marker=dict(color=df_2021_NED_ver['color'])
))
fig2021_13.add_trace(go.Scatter(x=df_2021_NED_gas['lap'], y=df_2021_NED_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_NED_gas['color'],
                           marker=dict(color=df_2021_NED_gas['color'])
))

fig2021_13.add_trace(go.Scatter(x=df_2021_NED_per['lap'], y=df_2021_NED_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_NED_per['color'],
                           marker=dict(color=df_2021_NED_per['color'])
))

fig2021_13.update_layout(layout)
fig2021_13.update_layout(title = '2021 Dutch Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))





# Italian Grand Prix (14)

df_2021_F_ITA = df_2021[(df_2021['name'] == 'Italian Grand Prix')]
df_2021_ITA = df_2021_F_ITA.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_ITA = df_2021_ITA.sort_values(by="lap")

df_2021_ITA_ver =df_2021_ITA[df_2021_ITA['code']=='VER']

df_2021_ITA_gas=df_2021_ITA[df_2021_ITA['code']=='GAS']

df_2021_ITA_per =df_2021_ITA[df_2021_ITA['code']=='PER']

fig2021_14 = go.Figure()

fig2021_14.add_trace(go.Scatter(x=df_2021_ITA_ver['lap'], y=df_2021_ITA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_ITA_ver['color'],
                           marker=dict(color=df_2021_ITA_ver['color'])
))
fig2021_14.add_trace(go.Scatter(x=df_2021_ITA_gas['lap'], y=df_2021_ITA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_ITA_gas['color'],
                           marker=dict(color=df_2021_ITA_gas['color'])
))

fig2021_14.add_trace(go.Scatter(x=df_2021_ITA_per['lap'], y=df_2021_ITA_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_ITA_per['color'],
                           marker=dict(color=df_2021_ITA_per['color'])
))

fig2021_14.update_layout(layout)
fig2021_14.update_layout(title = '2021 Italian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Russian Grand Prix (15)

df_2021_F_RUS = df_2021[(df_2021['name'] == 'Russian Grand Prix')]
df_2021_RUS = df_2021_F_RUS.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_RUS = df_2021_RUS.sort_values(by="lap")

df_2021_RUS_ver =df_2021_RUS[df_2021_RUS['code']=='VER']

df_2021_RUS_gas=df_2021_RUS[df_2021_RUS['code']=='GAS']

df_2021_RUS_per =df_2021_RUS[df_2021_RUS['code']=='PER']

fig2021_15 = go.Figure()

fig2021_15.add_trace(go.Scatter(x=df_2021_RUS_ver['lap'], y=df_2021_RUS_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_RUS_ver['color'],
                           marker=dict(color=df_2021_RUS_ver['color'])
))
fig2021_15.add_trace(go.Scatter(x=df_2021_RUS_gas['lap'], y=df_2021_RUS_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_RUS_gas['color'],
                           marker=dict(color=df_2021_RUS_gas['color'])
))

fig2021_15.add_trace(go.Scatter(x=df_2021_RUS_per['lap'], y=df_2021_RUS_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_RUS_per['color'],
                           marker=dict(color=df_2021_RUS_per['color'])
))

fig2021_15.update_layout(layout)
fig2021_15.update_layout(title = '2021 Russian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Turkish Grand Prix (16)

df_2021_F_TUR = df_2021[(df_2021['name'] == 'Turkish Grand Prix')]
df_2021_TUR = df_2021_F_TUR.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_TUR = df_2021_TUR.sort_values(by="lap")

df_2021_TUR_ver =df_2021_TUR[df_2021_TUR['code']=='VER']

df_2021_TUR_gas=df_2021_TUR[df_2021_TUR['code']=='GAS']

df_2021_TUR_per =df_2021_TUR[df_2021_TUR['code']=='PER']

fig2021_16 = go.Figure()

fig2021_16.add_trace(go.Scatter(x=df_2021_TUR_ver['lap'], y=df_2021_TUR_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_TUR_ver['color'],
                           marker=dict(color=df_2021_TUR_ver['color'])
))
fig2021_16.add_trace(go.Scatter(x=df_2021_TUR_gas['lap'], y=df_2021_TUR_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_TUR_gas['color'],
                           marker=dict(color=df_2021_TUR_gas['color'])
))

fig2021_16.add_trace(go.Scatter(x=df_2021_TUR_per['lap'], y=df_2021_TUR_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_TUR_per['color'],
                           marker=dict(color=df_2021_TUR_per['color'])
))

fig2021_16.update_layout(layout)
fig2021_16.update_layout(title = '2021 Turkish Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# United States Grand Prix (17)

df_2021_F_USA = df_2021[(df_2021['name'] == 'United States Grand Prix')]
df_2021_USA = df_2021_F_USA.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_USA = df_2021_USA.sort_values(by="lap")

df_2021_USA_ver =df_2021_USA[df_2021_USA['code']=='VER']

df_2021_USA_gas=df_2021_USA[df_2021_USA['code']=='GAS']

df_2021_USA_per =df_2021_USA[df_2021_USA['code']=='PER']

fig2021_17 = go.Figure()

fig2021_17.add_trace(go.Scatter(x=df_2021_USA_ver['lap'], y=df_2021_USA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_USA_ver['color'],
                           marker=dict(color=df_2021_USA_ver['color'])
))
fig2021_17.add_trace(go.Scatter(x=df_2021_USA_gas['lap'], y=df_2021_USA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_USA_gas['color'],
                           marker=dict(color=df_2021_USA_gas['color'])
))

fig2021_17.add_trace(go.Scatter(x=df_2021_USA_per['lap'], y=df_2021_USA_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_USA_per['color'],
                           marker=dict(color=df_2021_USA_per['color'])
))

fig2021_17.update_layout(layout)
fig2021_17.update_layout(title = '2021 United States Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Mexico City Grand Prix (18)
df_2021_F_MEX = df_2021[(df_2021['name'] == 'Mexico City Grand Prix')]
df_2021_MEX = df_2021_F_MEX.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_MEX = df_2021_MEX.sort_values(by="lap")

df_2021_MEX_ver =df_2021_MEX[df_2021_MEX['code']=='VER']

df_2021_MEX_gas=df_2021_MEX[df_2021_MEX['code']=='GAS']

df_2021_MEX_per =df_2021_MEX[df_2021_MEX['code']=='PER']

fig2021_18 = go.Figure()

fig2021_18.add_trace(go.Scatter(x=df_2021_MEX_ver['lap'], y=df_2021_MEX_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_MEX_ver['color'],
                           marker=dict(color=df_2021_MEX_ver['color'])
))
fig2021_18.add_trace(go.Scatter(x=df_2021_MEX_gas['lap'], y=df_2021_MEX_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_MEX_gas['color'],
                           marker=dict(color=df_2021_MEX_gas['color'])
))

fig2021_18.add_trace(go.Scatter(x=df_2021_MEX_per['lap'], y=df_2021_MEX_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_MEX_per['color'],
                           marker=dict(color=df_2021_MEX_per['color'])
))

fig2021_18.update_layout(layout)
fig2021_18.update_layout(title = '2021 Mexico City Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Qatar Grand Prix (19)

df_2021_F_QAT = df_2021[(df_2021['name'] == 'Qatar Grand Prix')]
df_2021_QAT = df_2021_F_QAT.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_QAT = df_2021_QAT.sort_values(by="lap")

df_2021_QAT_ver =df_2021_QAT[df_2021_QAT['code']=='VER']

df_2021_QAT_gas=df_2021_QAT[df_2021_QAT['code']=='GAS']

df_2021_QAT_per =df_2021_QAT[df_2021_QAT['code']=='PER']

fig2021_19 = go.Figure()

fig2021_19.add_trace(go.Scatter(x=df_2021_QAT_ver['lap'], y=df_2021_QAT_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_QAT_ver['color'],
                           marker=dict(color=df_2021_QAT_ver['color'])
))
fig2021_19.add_trace(go.Scatter(x=df_2021_QAT_gas['lap'], y=df_2021_QAT_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_QAT_gas['color'],
                           marker=dict(color=df_2021_QAT_gas['color'])
))

fig2021_19.add_trace(go.Scatter(x=df_2021_QAT_per['lap'], y=df_2021_QAT_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_QAT_per['color'],
                           marker=dict(color=df_2021_QAT_per['color'])
))

fig2021_19.update_layout(layout)
fig2021_19.update_layout(title = '2021 Qatar Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))

# São Paulo Grand Prix (20)

df_2021_F_BRZ = df_2021[(df_2021['name'] == 'São Paulo Grand Prix')]
df_2021_BRZ = df_2021_F_BRZ.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_BRZ = df_2021_BRZ.sort_values(by="lap")

df_2021_BRZ_ver =df_2021_BRZ[df_2021_BRZ['code']=='VER']

df_2021_BRZ_gas =df_2021_BRZ[df_2021_BRZ['code']=='GAS']

df_2021_BRZ_per =df_2021_BRZ[df_2021_BRZ['code']=='PER']

fig2021_20 = go.Figure()

fig2021_20.add_trace(go.Scatter(x=df_2021_BRZ_ver['lap'], y=df_2021_BRZ_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_BRZ_ver['color'],
                           marker=dict(color=df_2021_BRZ_ver['color'])
))
fig2021_20.add_trace(go.Scatter(x=df_2021_BRZ_gas['lap'], y=df_2021_BRZ_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_BRZ_gas['color'],
                           marker=dict(color=df_2021_BRZ_gas['color'])
))

fig2021_20.add_trace(go.Scatter(x=df_2021_BRZ_per['lap'], y=df_2021_BRZ_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_BRZ_per['color'],
                           marker=dict(color=df_2021_BRZ_per['color'])
))

fig2021_20.update_layout(layout)
fig2021_20.update_layout(title = '2021 São Paulo Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Saudi Arabian Grand Prix (21)

df_2021_F_SAU = df_2021[(df_2021['name'] == 'Saudi Arabian Grand Prix')]
df_2021_SAU = df_2021_F_SAU.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_SAU = df_2021_SAU.sort_values(by="lap")

df_2021_SAU_ver =df_2021_SAU[df_2021_SAU['code']=='VER']

df_2021_SAU_gas =df_2021_SAU[df_2021_SAU['code']=='GAS']

df_2021_SAU_per =df_2021_SAU[df_2021_SAU['code']=='PER']

fig2021_21 = go.Figure()

fig2021_21.add_trace(go.Scatter(x=df_2021_SAU_ver['lap'], y=df_2021_SAU_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_SAU_ver['color'],
                           marker=dict(color=df_2021_SAU_ver['color'])
))
fig2021_21.add_trace(go.Scatter(x=df_2021_SAU_gas['lap'], y=df_2021_SAU_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_SAU_gas['color'],
                           marker=dict(color=df_2021_SAU_gas['color'])
))

fig2021_21.add_trace(go.Scatter(x=df_2021_SAU_per['lap'], y=df_2021_SAU_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_SAU_per['color'],
                           marker=dict(color=df_2021_SAU_per['color'])
))

fig2021_21.update_layout(layout)
fig2021_21.update_layout(title = '2021 Saudi Arabian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Abu Dhabi Grand Prix (22)

df_2021_F_ABH = df_2021[(df_2021['name'] == 'Abu Dhabi Grand Prix')]
df_2021_ABH  = df_2021_F_ABH.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2021_ABH  = df_2021_ABH.sort_values(by="lap")

df_2021_ABH_ver =df_2021_ABH[df_2021_ABH['code']=='VER']

df_2021_ABH_gas =df_2021_ABH[df_2021_ABH['code']=='GAS']

df_2021_ABH_per =df_2021_ABH[df_2021_ABH['code']=='PER']

fig2021_22 = go.Figure()

fig2021_22.add_trace(go.Scatter(x=df_2021_ABH_ver['lap'], y=df_2021_ABH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2021_ABH_ver['color'],
                           marker=dict(color=df_2021_ABH_ver['color'])
))
fig2021_22.add_trace(go.Scatter(x=df_2021_ABH_gas['lap'], y=df_2021_ABH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2021_ABH_gas['color'],
                           marker=dict(color=df_2021_ABH_gas['color'])
))

fig2021_22.add_trace(go.Scatter(x=df_2021_ABH_per['lap'], y=df_2021_ABH_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',marker_color = df_2021_ABH_per['color'],
                           marker=dict(color=df_2021_ABH_per['color'])
))

fig2021_22.update_layout(layout)
fig2021_22.update_layout(title = '2021 Abu Dhabi Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# RACES: GRAPH OBJECTS
# Defining color of every driver

indexRB_ver_22 = df_2022[(df_2022['code'] == 'VER')].index
df_2022.loc[indexRB_ver_22,'color'] = '#66c2a5'

indexRB_gasly_22 = df_2022[(df_2022['code'] == 'GAS')].index
df_2022.loc[indexRB_gasly_22,'color'] = '#fc8d62'

indexRB_albon_22 = df_2022[(df_2022['code'] == 'ALB')].index
df_2022.loc[indexRB_albon_22,'color'] = '#8da0cb'

indexRB_perez_22 = df_2022[(df_2022['code'] == 'PER')].index
df_2022.loc[indexRB_perez_22,'color'] = '#e78ac3'



# Bahrain Grand Prix (1)

df_2022_F_BAH = df_2022[(df_2022['name'] == 'Bahrain Grand Prix')]
df_2022_BAH = df_2022_F_BAH.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_BAH = df_2022_BAH.sort_values(by="lap")

df_2022_BAH_ver =df_2022_BAH[df_2022_BAH['code']=='VER']

df_2022_BAH_gas =df_2022_BAH[df_2022_BAH['code']=='GAS']

df_2022_BAH_alb =df_2022_BAH[df_2022_BAH['code']=='ALB']

df_2022_BAH_per =df_2022_BAH[df_2022_BAH['code']=='PER']

fig2022_1 = go.Figure()

fig2022_1.add_trace(go.Scatter(x=df_2022_BAH_ver['lap'], y=df_2022_BAH_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_BAH_ver['color'],
                           marker=dict(color=df_2022_BAH_ver['color'])
))
fig2022_1.add_trace(go.Scatter(x=df_2022_BAH_gas['lap'], y=df_2022_BAH_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_BAH_gas['color'],
                           marker=dict(color=df_2022_BAH_gas['color'])
))


fig2022_1.add_trace(go.Scatter(x=df_2022_BAH_alb['lap'], y=df_2022_BAH_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_BAH_alb['color'])
))

fig2022_1.add_trace(go.Scatter(x=df_2022_BAH_per['lap'], y=df_2022_BAH_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_BAH_per['color'])
))

fig2022_1.update_layout(layout)
fig2022_1.update_layout(title = '2022 Bahrain Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))

# Saudi Arabian Grand Prix (2)

df_2022_F_SAU = df_2022[(df_2022['name'] == 'Saudi Arabian Grand Prix')]
df_2022_SAU = df_2022_F_SAU.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_SAU = df_2022_SAU.sort_values(by="lap")

df_2022_SAU_ver =df_2022_SAU[df_2022_SAU['code']=='VER']

df_2022_SAU_gas =df_2022_SAU[df_2022_SAU['code']=='GAS']

df_2022_SAU_alb =df_2022_SAU[df_2022_SAU['code']=='ALB']

df_2022_SAU_per =df_2022_SAU[df_2022_SAU['code']=='PER']

fig2022_2 = go.Figure()

fig2022_2.add_trace(go.Scatter(x=df_2022_SAU_ver['lap'], y=df_2022_SAU_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_SAU_ver['color'],
                           marker=dict(color=df_2022_SAU_ver['color'])
))
fig2022_2.add_trace(go.Scatter(x=df_2022_SAU_gas['lap'], y=df_2022_SAU_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_SAU_gas['color'],
                           marker=dict(color=df_2022_SAU_gas['color'])
))


fig2022_2.add_trace(go.Scatter(x=df_2022_SAU_alb['lap'], y=df_2022_SAU_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_SAU_alb['color'])
))

fig2022_2.add_trace(go.Scatter(x=df_2022_SAU_per['lap'], y=df_2022_SAU_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_SAU_per['color'])
))

fig2022_2.update_layout(layout)
fig2022_2.update_layout(title = '2022 Saudi Arabian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Australian Grand Prix (3)

df_2022_F_AUST = df_2022[(df_2022['name'] == 'Australian Grand Prix')]
df_2022_AUST = df_2022_F_AUST.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_AUST = df_2022_AUST.sort_values(by="lap")

df_2022_AUST_ver =df_2022_AUST[df_2022_AUST['code']=='VER']

df_2022_AUST_gas =df_2022_AUST[df_2022_AUST['code']=='GAS']

df_2022_AUST_alb =df_2022_AUST[df_2022_AUST['code']=='ALB']

df_2022_AUST_per =df_2022_AUST[df_2022_AUST['code']=='PER']

fig2022_3 = go.Figure()

fig2022_3.add_trace(go.Scatter(x=df_2022_AUST_ver['lap'], y=df_2022_AUST_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_AUST_ver['color'],
                           marker=dict(color=df_2022_AUST_ver['color'])
))
fig2022_3.add_trace(go.Scatter(x=df_2022_AUST_gas['lap'], y=df_2022_AUST_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_AUST_gas['color'],
                           marker=dict(color=df_2022_AUST_gas['color'])
))


fig2022_3.add_trace(go.Scatter(x=df_2022_AUST_alb['lap'], y=df_2022_AUST_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_AUST_alb['color'])
))

fig2022_3.add_trace(go.Scatter(x=df_2022_AUST_per['lap'], y=df_2022_AUST_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_AUST_per['color'])
))

fig2022_3.update_layout(layout)
fig2022_3.update_layout(title = '2022 Australian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Emilia Romagna Grand Prix (4)

df_2022_F_EMI = df_2022[(df_2022['name'] == 'Emilia Romagna Grand Prix')]
df_2022_EMI = df_2022_F_EMI.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_EMI = df_2022_EMI.sort_values(by="lap")

df_2022_EMI_ver =df_2022_EMI[df_2022_EMI['code']=='VER']

df_2022_EMI_gas =df_2022_EMI[df_2022_EMI['code']=='GAS']

df_2022_EMI_alb =df_2022_EMI[df_2022_EMI['code']=='ALB']

df_2022_EMI_per =df_2022_EMI[df_2022_EMI['code']=='PER']

fig2022_4 = go.Figure()

fig2022_4.add_trace(go.Scatter(x=df_2022_EMI_ver['lap'], y=df_2022_EMI_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_EMI_ver['color'],
                           marker=dict(color=df_2022_EMI_ver['color'])
))
fig2022_4.add_trace(go.Scatter(x=df_2022_EMI_gas['lap'], y=df_2022_EMI_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_EMI_gas['color'],
                           marker=dict(color=df_2022_EMI_gas['color'])
))


fig2022_4.add_trace(go.Scatter(x=df_2022_EMI_alb['lap'], y=df_2022_EMI_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_EMI_alb['color'])
))

fig2022_4.add_trace(go.Scatter(x=df_2022_EMI_per['lap'], y=df_2022_EMI_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_EMI_per['color'])
))

fig2022_4.update_layout(layout)
fig2022_4.update_layout(title = '2022 Emilia Romagna Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Miami Grand Prix (5)

df_2022_F_MIA = df_2022[(df_2022['name'] == 'Miami Grand Prix')]
df_2022_MIA = df_2022_F_MIA.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_MIA = df_2022_MIA.sort_values(by="lap")

df_2022_MIA_ver =df_2022_MIA[df_2022_MIA['code']=='VER']

df_2022_MIA_gas =df_2022_MIA[df_2022_MIA['code']=='GAS']

df_2022_MIA_alb =df_2022_MIA[df_2022_MIA['code']=='ALB']

df_2022_MIA_per =df_2022_MIA[df_2022_MIA['code']=='PER']

fig2022_5 = go.Figure()

fig2022_5.add_trace(go.Scatter(x=df_2022_MIA_ver['lap'], y=df_2022_MIA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_MIA_ver['color'],
                           marker=dict(color=df_2022_MIA_ver['color'])
))
fig2022_5.add_trace(go.Scatter(x=df_2022_MIA_gas['lap'], y=df_2022_MIA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_MIA_gas['color'],
                           marker=dict(color=df_2022_MIA_gas['color'])
))


fig2022_5.add_trace(go.Scatter(x=df_2022_MIA_alb['lap'], y=df_2022_MIA_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_MIA_alb['color'])
))

fig2022_5.add_trace(go.Scatter(x=df_2022_MIA_per['lap'], y=df_2022_MIA_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_MIA_per['color'])
))

fig2022_5.update_layout(layout)
fig2022_5.update_layout(title = '2022 Miami Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Spanish Grand Prix (6)

df_2022_F_ESP = df_2022[(df_2022['name'] == 'Spanish Grand Prix')]
df_2022_ESP = df_2022_F_ESP.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_ESP = df_2022_ESP.sort_values(by="lap")

df_2022_ESP_ver =df_2022_ESP[df_2022_ESP['code']=='VER']

df_2022_ESP_gas =df_2022_ESP[df_2022_ESP['code']=='GAS']

df_2022_ESP_alb =df_2022_ESP[df_2022_ESP['code']=='ALB']

df_2022_ESP_per =df_2022_ESP[df_2022_ESP['code']=='PER']

fig2022_6 = go.Figure()

fig2022_6.add_trace(go.Scatter(x=df_2022_ESP_ver['lap'], y=df_2022_ESP_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_ESP_ver['color'],
                           marker=dict(color=df_2022_ESP_ver['color'])
))
fig2022_6.add_trace(go.Scatter(x=df_2022_ESP_gas['lap'], y=df_2022_ESP_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_ESP_gas['color'],
                           marker=dict(color=df_2022_ESP_gas['color'])
))


fig2022_6.add_trace(go.Scatter(x=df_2022_ESP_alb['lap'], y=df_2022_ESP_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_ESP_alb['color'])
))

fig2022_6.add_trace(go.Scatter(x=df_2022_ESP_per['lap'], y=df_2022_ESP_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_ESP_per['color'])
))

fig2022_6.update_layout(layout)
fig2022_6.update_layout(title = '2022 Spanish Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Monaco Grand Prix (7)

df_2022_F_MON = df_2022[(df_2022['name'] == 'Monaco Grand Prix')]
df_2022_MON = df_2022_F_MON.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_MON = df_2022_MON.sort_values(by="lap")

df_2022_MON_ver =df_2022_MON[df_2022_MON['code']=='VER']

df_2022_MON_gas =df_2022_MON[df_2022_MON['code']=='GAS']

df_2022_MON_alb =df_2022_MON[df_2022_MON['code']=='ALB']

df_2022_MON_per =df_2022_MON[df_2022_MON['code']=='PER']

fig2022_7 = go.Figure()

fig2022_7.add_trace(go.Scatter(x=df_2022_MON_ver['lap'], y=df_2022_MON_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_MON_ver['color'],
                           marker=dict(color=df_2022_MON_ver['color'])
))
fig2022_7.add_trace(go.Scatter(x=df_2022_MON_gas['lap'], y=df_2022_MON_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_MON_gas['color'],
                           marker=dict(color=df_2022_MON_gas['color'])
))


fig2022_7.add_trace(go.Scatter(x=df_2022_MON_alb['lap'], y=df_2022_MON_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_MON_alb['color'])
))

fig2022_7.add_trace(go.Scatter(x=df_2022_MON_per['lap'], y=df_2022_MON_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_MON_per['color'])
))

fig2022_7.update_layout(layout)
fig2022_7.update_layout(title = '2022 Monaco Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Azerbaijan Grand Prix (8)

df_2022_F_AZB = df_2022[(df_2022['name'] == 'Azerbaijan Grand Prix')]
df_2022_AZB = df_2022_F_AZB.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_AZB = df_2022_AZB.sort_values(by="lap")

df_2022_AZB_ver =df_2022_AZB[df_2022_AZB['code']=='VER']

df_2022_AZB_gas =df_2022_AZB[df_2022_AZB['code']=='GAS']

df_2022_AZB_alb =df_2022_AZB[df_2022_AZB['code']=='ALB']

df_2022_AZB_per =df_2022_AZB[df_2022_AZB['code']=='PER']

fig2022_8 = go.Figure()

fig2022_8.add_trace(go.Scatter(x=df_2022_AZB_ver['lap'], y=df_2022_AZB_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_AZB_ver['color'],
                           marker=dict(color=df_2022_AZB_ver['color'])
))
fig2022_8.add_trace(go.Scatter(x=df_2022_AZB_gas['lap'], y=df_2022_AZB_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_AZB_gas['color'],
                           marker=dict(color=df_2022_AZB_gas['color'])
))


fig2022_8.add_trace(go.Scatter(x=df_2022_AZB_alb['lap'], y=df_2022_AZB_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_AZB_alb['color'])
))

fig2022_8.add_trace(go.Scatter(x=df_2022_AZB_per['lap'], y=df_2022_AZB_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_AZB_per['color'])
))

fig2022_8.update_layout(layout)
fig2022_8.update_layout(title = '2022 Azerbaijan Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Canadian Grand Prix (9)

df_2022_F_CAN = df_2022[(df_2022['name'] == 'Canadian Grand Prix')]
df_2022_CAN = df_2022_F_CAN.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_CAN = df_2022_CAN.sort_values(by="lap")

df_2022_CAN_ver =df_2022_CAN[df_2022_CAN['code']=='VER']

df_2022_CAN_gas =df_2022_CAN[df_2022_CAN['code']=='GAS']

df_2022_CAN_alb =df_2022_CAN[df_2022_CAN['code']=='ALB']

df_2022_CAN_per =df_2022_CAN[df_2022_CAN['code']=='PER']

fig2022_9 = go.Figure()

fig2022_9.add_trace(go.Scatter(x=df_2022_CAN_ver['lap'], y=df_2022_CAN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_CAN_ver['color'],
                           marker=dict(color=df_2022_CAN_ver['color'])
))
fig2022_9.add_trace(go.Scatter(x=df_2022_CAN_gas['lap'], y=df_2022_CAN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_CAN_gas['color'],
                           marker=dict(color=df_2022_CAN_gas['color'])
))


fig2022_9.add_trace(go.Scatter(x=df_2022_CAN_alb['lap'], y=df_2022_CAN_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_CAN_alb['color'])
))

fig2022_9.add_trace(go.Scatter(x=df_2022_CAN_per['lap'], y=df_2022_CAN_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_CAN_per['color'])
))

fig2022_9.update_layout(layout)
fig2022_9.update_layout(title = '2022 Canadian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# British Grand Prix (10)

df_2022_F_BRIT = df_2022[(df_2022['name'] == 'British Grand Prix')]
df_2022_BRIT = df_2022_F_BRIT.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_BRIT = df_2022_BRIT.sort_values(by="lap")

df_2022_BRIT_ver =df_2022_BRIT[df_2022_BRIT['code']=='VER']

df_2022_BRIT_gas =df_2022_BRIT[df_2022_BRIT['code']=='GAS']

df_2022_BRIT_alb =df_2022_BRIT[df_2022_BRIT['code']=='ALB']

df_2022_BRIT_per =df_2022_BRIT[df_2022_BRIT['code']=='PER']

fig2022_10 = go.Figure()

fig2022_10.add_trace(go.Scatter(x=df_2022_BRIT_ver['lap'], y=df_2022_BRIT_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_BRIT_ver['color'],
                           marker=dict(color=df_2022_BRIT_ver['color'])
))
fig2022_10.add_trace(go.Scatter(x=df_2022_BRIT_gas['lap'], y=df_2022_BRIT_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_BRIT_gas['color'],
                           marker=dict(color=df_2022_BRIT_gas['color'])
))


fig2022_10.add_trace(go.Scatter(x=df_2022_BRIT_alb['lap'], y=df_2022_BRIT_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_BRIT_alb['color'])
))

fig2022_10.add_trace(go.Scatter(x=df_2022_BRIT_per['lap'], y=df_2022_BRIT_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_BRIT_per['color'])
))

fig2022_10.update_layout(layout)
fig2022_10.update_layout(title = '2022 British Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Austrian Grand Prix (11)

df_2022_F_AUS = df_2022[(df_2022['name'] == 'Austrian Grand Prix')]
df_2022_AUS = df_2022_F_AUS.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_AUS = df_2022_AUS.sort_values(by="lap")

df_2022_AUS_ver =df_2022_AUS[df_2022_AUS['code']=='VER']

df_2022_AUS_gas =df_2022_AUS[df_2022_AUS['code']=='GAS']

df_2022_AUS_alb =df_2022_AUS[df_2022_AUS['code']=='ALB']

df_2022_AUS_per =df_2022_AUS[df_2022_AUS['code']=='PER']

fig2022_11 = go.Figure()

fig2022_11.add_trace(go.Scatter(x=df_2022_AUS_ver['lap'], y=df_2022_AUS_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_AUS_ver['color'],
                           marker=dict(color=df_2022_AUS_ver['color'])
))
fig2022_11.add_trace(go.Scatter(x=df_2022_AUS_gas['lap'], y=df_2022_AUS_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_AUS_gas['color'],
                           marker=dict(color=df_2022_AUS_gas['color'])
))


fig2022_11.add_trace(go.Scatter(x=df_2022_AUS_alb['lap'], y=df_2022_AUS_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_AUS_alb['color'])
))

fig2022_10.add_trace(go.Scatter(x=df_2022_AUS_per['lap'], y=df_2022_AUS_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_AUS_per['color'])
))

fig2022_11.update_layout(layout)
fig2022_11.update_layout(title = '2022 Austrian Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# French Grand Prix (12)

df_2022_F_FRA = df_2022[(df_2022['name'] == 'French Grand Prix')]
df_2022_FRA = df_2022_F_FRA.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_FRA = df_2022_FRA.sort_values(by="lap")

df_2022_FRA_ver =df_2022_FRA[df_2022_FRA['code']=='VER']

df_2022_FRA_gas =df_2022_FRA[df_2022_FRA['code']=='GAS']

df_2022_FRA_alb =df_2022_FRA[df_2022_FRA['code']=='ALB']

df_2022_FRA_per =df_2022_FRA[df_2022_FRA['code']=='PER']

fig2022_12 = go.Figure()

fig2022_12.add_trace(go.Scatter(x=df_2022_FRA_ver['lap'], y=df_2022_FRA_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_FRA_ver['color'],
                           marker=dict(color=df_2022_FRA_ver['color'])
))
fig2022_12.add_trace(go.Scatter(x=df_2022_FRA_gas['lap'], y=df_2022_FRA_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_FRA_gas['color'],
                           marker=dict(color=df_2022_FRA_gas['color'])
))


fig2022_12.add_trace(go.Scatter(x=df_2022_FRA_alb['lap'], y=df_2022_FRA_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_FRA_alb['color'])
))

fig2022_12.add_trace(go.Scatter(x=df_2022_FRA_per['lap'], y=df_2022_FRA_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_FRA_per['color'])
))

fig2022_12.update_layout(layout)
fig2022_12.update_layout(title = '2022 Frech Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))




# Hungarian Grand Prix (13)

df_2022_F_HUN = df_2022[(df_2022['name'] == 'Hungarian Grand Prix')]
df_2022_HUN = df_2022_F_HUN.query("driverRef in ['gasly', 'max_verstappen','albon','perez']")
df_2022_HUN = df_2022_HUN.sort_values(by="lap")

df_2022_HUN_ver =df_2022_HUN[df_2022_HUN['code']=='VER']

df_2022_HUN_gas =df_2022_HUN[df_2022_HUN['code']=='GAS']

df_2022_HUN_alb =df_2022_HUN[df_2022_HUN['code']=='ALB']

df_2022_HUN_per =df_2022_HUN[df_2022_HUN['code']=='PER']

fig2022_13 = go.Figure()

fig2022_13.add_trace(go.Scatter(x=df_2022_HUN_ver['lap'], y=df_2022_HUN_ver['seconds'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = df_2022_HUN_ver['color'],
                           marker=dict(color=df_2022_HUN_ver['color'])
))
fig2022_13.add_trace(go.Scatter(x=df_2022_HUN_gas['lap'], y=df_2022_HUN_gas['seconds'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = df_2022_HUN_gas['color'],
                           marker=dict(color=df_2022_HUN_gas['color'])
))


fig2022_13.add_trace(go.Scatter(x=df_2022_HUN_alb['lap'], y=df_2022_HUN_alb['seconds'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=df_2022_HUN_alb['color'])
))

fig2022_13.add_trace(go.Scatter(x=df_2022_HUN_per['lap'], y=df_2022_HUN_per['seconds'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=df_2022_HUN_per['color'])
))

fig2022_13.update_layout(layout)
fig2022_13.update_layout(title = '2022 Frech Grand Prix',xaxis_title ="lap",yaxis_title ="time",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))

suppress_callback_exceptions=True

layout = html.Div(children=[
    html.P(),
    html.Div(className='service-box', children=[
        html.Div(className='row', children=[
            dcc.RadioItems(id='radio1',
                           options=[dict(label='2019', value=1), dict(label='2020', value=2),
                                    dict(label='2021', value=3), dict(label='2022', value=4)],
                           value=1, inline=True,
                           labelStyle={'margin-right': '10px', 'font-weight': 300}
                           )
        ]),
        html.Div(id='races',children=[
            html.P(),
            html.Span('Races: ', style={'font-size': '20px', 'font-weight': 'bold'}),
            dcc.Dropdown(id='dp1', clearable=False)]),
        dcc.Graph(id='race-graph'),
    ])
])


@callback([Output('dp1', 'options'), Output('dp1', 'value')], Input('radio1', 'value'))
def dropdown(value):
    if value == 1:
        d = [{'label': x, 'value': x} for x in [
                                                'Australian Grand Prix',
                                                'Bahrain Grand Prix',
                                                'Chinese Grand Prix',
                                                'Azerbaijan Grand Prix',
                                                'Spanish Grand Prix',
                                                'Monaco Grand Prix',
                                                'Canadian Grand Prix',
                                                'French Grand Prix',
                                                'Austrian Grand Prix',
                                                'British Grand Prix',
                                                'German Grand Prix',
                                                'Hungarian Grand Prix',
                                                'Belgian Grand Prix',
                                                'Italian Grand Prix',
                                                'Singapore Grand Prix',
                                                'Russian Grand Prix',
                                                'Japanese Grand Prix',
                                                'Mexican Grand Prix',
                                                'United States Grand Prix',
                                                'Brazilian Grand Prix',
                                                'Abu Dhabi Grand Prix']]
        v ='Australian Grand Prix'
        return d,v
    elif value == 2:
        d = [{'label': x, 'value': x} for x in [
                                                'Austrian Grand Prix',
                                                'Styrian Grand Prix',
                                                'Hungarian Grand Prix',
                                                'British Grand Prix',
                                                '70th Anniversary Grand Prix',
                                                'Spanish Grand Prix',
                                                'Belgian Grand Prix',
                                                'Italian Grand Prix',
                                                'Tuscan Grand Prix',
                                                'Russian Grand Prix',
                                                'Eifel Grand Prix',
                                                'Portuguese Grand Prix',
                                                'Emilia Romagna Grand Prix',
                                                'Turkish Grand Prix',
                                                'Bahrain Grand Prix',
                                                'Sakhir Grand Prix',
                                                'Abu Dhabi Grand Prix']]
        v = 'Austrian Grand Prix'
        return d,v
    elif value == 3:
        d = [{'label': x, 'value': x} for x in [
                                                'Bahrain Grand Prix',
                                                'Emilia Romagna Grand Prix',
                                                'Portuguese Grand Prix',
                                                'Spanish Grand Prix',
                                                'Monaco Grand Prix',
                                                'Azerbaijan Grand Prix',
                                                'French Grand Prix',
                                                'Styrian Grand Prix',
                                                'Austrian Grand Prix',
                                                'British Grand Prix',
                                                'Hungarian Grand Prix',
                                                'Belgian Grand Prix',
                                                'Dutch Grand Prix',
                                                'Italian Grand Prix',
                                                'Russian Grand Prix',
                                                'Turkish Grand Prix',
                                                'United States Grand Prix',
                                                'Mexico City Grand Prix',
                                                'São Paulo Grand Prix',
                                                'Qatar Grand Prix',
                                                'Saudi Arabian Grand Prix',
                                                'Abu Dhabi Grand Prix']]
        v = 'Bahrain Grand Prix'
        return d,v
    elif value == 4:
        d = [{'label': x, 'value': x} for x in [
                                                'Bahrain Grand Prix',
                                                'Saudi Arabian Grand Prix',
                                                'Australian Grand Prix',
                                                'Emilia Romagna Grand Prix',
                                                'Miami Grand Prix',
                                                'Spanish Grand Prix',
                                                'Monaco Grand Prix',
                                                'Azerbaijan Grand Prix',
                                                'Canadian Grand Prix',
                                                'British Grand Prix',
                                                'Austrian Grand Prix',
                                                'French Grand Prix',
                                                'Hungarian Grand Prix']]
        v = 'Bahrain Grand Prix'
        return d,v

@callback(Output('race-graph','figure'),[Input('radio1','value'),Input('dp1','value')])
def graphs(value,d):
    print(d)
    if value == 1:
       if d == 'Australian Grand Prix':
          return fig2019_1
       elif d == 'Bahrain Grand Prix':
          return fig2019_2
       elif d == 'Chinese Grand Prix':
          return fig2019_3
       elif d == 'Azerbaijan Grand Prix':
          return fig2019_4
       elif d == 'Spanish Grand Prix':
          return fig2019_5
       elif d == 'Monaco Grand Prix':
          return fig2019_6
       elif d == 'Canadian Grand Prix':
          return fig2019_7
       elif d == 'French Grand Prix':
          return fig2019_8
       elif d == 'Austrian Grand Prix':
          return fig2019_9
       elif d == 'British Grand Prix':
          return fig2019_10
       elif d == 'German Grand Prix':
          return fig2019_11
       elif d == 'Hungarian Grand Prix':
          return fig2019_12
       elif d == 'Belgian Grand Prix':
          return fig2019_13
       elif d == 'Italian Grand Prix':
          return fig2019_14
       elif d == 'Singapore Grand Prix':
          return fig2019_15
       elif d == 'Russian Grand Prix':
          return fig2019_16
       elif d == 'Japanese Grand Prix':
          return fig2019_17
       elif d == 'Mexican Grand Prix':
          return fig2019_18
       elif d == 'United States Grand Prix':
          return fig2019_19
       elif d == 'Brazilian Grand Prix':
          return fig2019_20
       elif d == 'Abu Dhabi Grand Prix':
          return fig2019_21


    elif value == 2:
       if d == 'Austrian Grand Prix':
          return fig2020_1
       elif d == 'Styrian Grand Prix':
          return fig2020_2
       elif d == 'Hungarian Grand Prix':
          return fig2020_3
       elif d == 'British Grand Prix':
          return fig2020_4
       elif d == '70th Anniversary Grand Prix':
          return fig2020_5
       elif d == 'Spanish Grand Prix':
          return fig2020_6
       elif d == 'Belgian Grand Prix':
          return fig2020_7
       elif d == 'Italian Grand Prix':
          return fig2020_8
       elif d == 'Tuscan Grand Prix':
          return fig2020_9
       elif d == 'Russian Grand Prix':
          return fig2020_10
       elif d == 'Eifel Grand Prix':
          return fig2020_11
       elif d == 'Portuguese Grand Prix':
          return fig2020_12
       elif d == 'Emilia Romagna Grand Prix':
          return fig2020_13
       elif d == 'Turkish Grand Prix':
          return fig2020_14
       elif d == 'Bahrain Grand Prix':
          return fig2020_15
       elif d == 'Sakhir Grand Prix':
          return fig2020_16
       elif d == 'Abu Dhabi Grand Prix':
          return fig2020_17

    elif value == 3:
       if d == 'Bahrain Grand Prix':
          return fig2021_1
       elif d == 'Emilia Romagna Grand Prix':
          return fig2021_2
       elif d == 'Portuguese Grand Prix':
          return fig2021_3
       elif d == 'Spanish Grand Prix':
          return fig2021_4
       elif d == 'Monaco Grand Prix':
          return fig2021_5
       elif d == 'Azerbaijan Grand Prix':
          return fig2021_6
       elif d == 'French Grand Prix':
          return fig2021_7
       elif d == 'Styrian Grand Prix':
          return fig2021_8
       elif d == 'Austrian Grand Prix':
          return fig2021_9
       elif d == 'British Grand Prix':
          return fig2021_10
       elif d == 'Hungarian Grand Prix':
          return fig2021_11
       elif d == 'Belgian Grand Prix':
          return fig2021_12
       elif d == 'Dutch Grand Prix':
          return fig2021_13
       elif d == 'Italian Grand Prix':
          return fig2021_14
       elif d == 'Russian Grand Prix':
          return fig2021_15
       elif d == 'Turkish Grand Prix':
          return fig2021_16
       elif d == 'United States Grand Prix':
          return fig2021_17
       elif d == 'Mexico City Grand Prix':
          return fig2021_18
       elif d == 'São Paulo Grand Prix':
          return fig2021_19
       elif d == 'Qatar Grand Prix':
          return fig2021_20
       elif d == 'Saudi Arabian Grand Prix':
          return fig2021_21
       elif d == 'Abu Dhabi Grand Prix':
          return fig2021_22

    elif value == 4:
       if d == 'Bahrain Grand Prix':
          return fig2022_1
       elif d == 'Saudi Arabia Grand Prix':
          return fig2022_2
       elif d == 'Australian Grand Prix':
          return fig2022_3
       elif d == 'Emilia Romagna Grand Prix':
          return fig2022_4
       elif d == 'Miami Grand Prix':
          return fig2022_5
       elif d == 'Spanish Grand Prix':
          return fig2022_6
       elif d == 'Monaco Grand Prix':
          return fig2022_7
       elif d == 'Azerbaijan Grand Prix':
          return fig2022_8
       elif d == 'Canadian Grand Prix':
          return fig2022_9
       elif d == 'British Grand Prix':
          return fig2022_10
       elif d == 'Austrian Grand Prix':
          return fig2022_11
       elif d == 'French Grand Prix':
          return fig2022_12
       elif d == 'Hungarian Grand Prix':
          return fig2022_13
       
