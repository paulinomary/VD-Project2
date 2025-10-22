import dash
from dash import dcc, html
from dash import callback, Input, Output
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import math
import plotly.graph_objs as go

dash.register_page(__name__, name='Race Standings')

circuits = pd.read_csv("circuits.csv")
constructor_results = pd.read_csv("constructor_results.csv")
constructor_standings = pd.read_csv("constructor_standings.csv")
constructors = pd.read_csv("constructors.csv")
driver_standings = pd.read_csv("driver_standings.csv")
drivers = pd.read_csv("drivers.csv")
lap_times = pd.read_csv("lap_times.csv")
pit_stops = pd.read_csv("pit_stops.csv")
qualifying = pd.read_csv("qualifying.csv")
races = pd.read_csv("races.csv")
results = pd.read_csv("results.csv")
seasons = pd.read_csv("seasons.csv")
sprint_results = pd.read_csv("sprint_results.csv")
status = pd.read_csv("status.csv")

df = pd.merge(lap_times,drivers[['driverId','code','driverRef']],how='left',on='driverId')
df = pd.merge(df,races[['raceId','name','date','year']],how='left',on='raceId')

df2 = df
#df2 = pd.merge(lap_times,drivers[['driverId','code','driverRef']],how='left',on='driverId')
df2 = pd.merge(df2,driver_standings[['driverStandingsId','raceId','points']],how='left',on='raceId')
#df2
df_2019_2 = df2[df2['year'] == 2019]
# For Final Position Per Race

df_results = results
df_results = df_results.merge(drivers[['driverId','code','driverRef']],how='left',on='driverId')
df_results = df_results.merge(races[['raceId','name','date','year']],how='left',on='raceId')

df_results.drop_duplicates(inplace=True)

df_results[df_results['position']==r'\N']=0
df_results['position'] = df_results['position'].astype(int)
## For Season points per race
#driver_standings
season_Points =driver_standings

#a.info()

season_Points = season_Points.merge(drivers[['driverId','code','driverRef']],how='left',on='driverId')
season_Points1 = season_Points
season_Points1 = season_Points1.merge(races[['raceId','name','date','year']],how='left',on='raceId')
#a1.info()
season_Points_2019 = season_Points1
season_Points_2020 = season_Points1
season_Points_2021 = season_Points1
season_Points_2022 = season_Points1

season_Points_2019 = season_Points_2019[(season_Points_2019['year']==2019)&((season_Points_2019['code']=='VER')|(season_Points_2019['code']=='GAS')|
                                                             (season_Points_2019['code']=='ALB')|(season_Points_2019['code']=='PER'))]
season_Points_2020 = season_Points_2020[(season_Points_2020['year']==2020)&((season_Points_2020['code']=='VER')|(season_Points_2020['code']=='GAS')|
                                            (season_Points_2020['code']=='ALB')|(season_Points_2020['code']=='PER'))]
season_Points_2021 = season_Points_2021[(season_Points_2021['year']==2021)&((season_Points_2021['code']=='VER')|
                                (season_Points_2021['code']=='GAS')|(season_Points_2021['code']=='ALB')|(season_Points_2021['code']=='PER'))]
season_Points_2022 = season_Points_2022[(season_Points_2022['year']==2022)&((season_Points_2022['code']=='VER')|
                                                                            (season_Points_2022['code']=='GAS')|(season_Points_2022['code']=='ALB')|(season_Points_2022['code']=='PER'))]
#season_Points_2019.info()

# Position 2019 per Race
df_results_2019 = df_results[(df_results['year']==2019)&((df_results['code']=='VER')|(df_results['code']=='GAS')|(df_results['code']=='ALB')|(df_results['code']=='PER'))]


indexRB_ver_19 = df_results_2019[(df_results_2019['code'] == 'VER')].index
df_results_2019.loc[indexRB_ver_19,'color'] = '#66c2a5'

indexRB_gasly_19 = df_results_2019[(df_results_2019['code'] == 'GAS')].index
df_results_2019.loc[indexRB_gasly_19,'color'] = '#fc8d62'

indexRB_albon_19 = df_results_2019[(df_results_2019['code'] == 'ALB')].index
df_results_2019.loc[indexRB_albon_19,'color'] = '#8da0cb'

indexRB_perez_19 = df_results_2019[(df_results_2019['code'] == 'PER')].index
df_results_2019.loc[indexRB_perez_19,'color'] = '#e78ac3'



df_results_2019_ver =df_results_2019[df_results_2019['code']=='VER']
df_results_2019_ver= df_results_2019_ver.sort_values(by="date")
df_results_2019_ver['corrida']=df_results_2019_ver['name']+' ('+df_results_2019_ver['date']+')'

df_results_2019_gas =df_results_2019[df_results_2019['code']=='GAS']
df_results_2019_gas= df_results_2019_gas.sort_values(by="date")
df_results_2019_gas['corrida']=df_results_2019_gas['name']+' ('+df_results_2019_gas['date']+')'

df_results_2019_per =df_results_2019[df_results_2019['code']=='PER']
df_results_2019_per= df_results_2019_per.sort_values(by="date")
df_results_2019_per['corrida']=df_results_2019_per['name']+' ('+df_results_2019_per['date']+')'

df_results_2019_alb =df_results_2019[df_results_2019['code']=='ALB']
df_results_2019_alb= df_results_2019_alb.sort_values(by="date")
df_results_2019_alb['corrida']=df_results_2019_alb['name']+' ('+df_results_2019_alb['date']+')'

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

fig_results_2019 = go.Figure()

fig_results_2019 = go.Figure(data=[
    go.Bar(name ='Max Verstappen',x=df_results_2019_ver['corrida'], y=df_results_2019_ver['position'],marker_color=df_results_2019_ver['color']),
    go.Bar(name='Pierre Gasly',x=df_results_2019_gas['corrida'], y=df_results_2019_gas['position'],marker_color=df_results_2019_gas['color']),
    go.Bar(name='Sergio Perez',x=df_results_2019_per['corrida'], y=df_results_2019_per['position'],marker_color=df_results_2019_per['color']),
    go.Bar(name='Alexander Albon',x=df_results_2019_alb['corrida'], y=df_results_2019_alb['position'],marker_color=df_results_2019_alb['color']),

])

fig_results_2019.update_layout(layout_results)
fig_results_2019.update_layout(title = '2019 Grand Prixs Positions per Race',xaxis_title ="Grand Prixs",yaxis_title ="Final Position",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# 2019 Season Points per Race
season_Points_2019_ = season_Points_2019.query("code in ['GAS', 'VER','ALB','PER']")
season_Points_2019_ = season_Points_2019.sort_values(by="date")


indexRB_ver_19 = season_Points_2019[(season_Points_2019['code'] == 'VER')].index
season_Points_2019.loc[indexRB_ver_19,'color'] = '#66c2a5'

indexRB_gasly_19 = season_Points_2019[(season_Points_2019['code'] == 'GAS')].index
season_Points_2019.loc[indexRB_gasly_19,'color'] = '#fc8d62'

indexRB_albon_19 = season_Points_2019[(season_Points_2019['code'] == 'ALB')].index
season_Points_2019.loc[indexRB_albon_19,'color'] = '#8da0cb'

#indexRB_perez_19 = season_Points_2019[(season_Points_2019['code'] == 'PER')].index
#season_Points_2019.loc[indexRB_perez_19,'color'] = '#e78ac3'

season_Points_2019_ver =season_Points_2019[season_Points_2019['code']=='VER']
season_Points_2019_ver['corrida']=season_Points_2019_ver['name']+' ('+season_Points_2019_ver['date']+')'

season_Points_2019_gas =season_Points_2019[season_Points_2019['code']=='GAS']
season_Points_2019_gas['corrida']=season_Points_2019_gas['name']+' ('+season_Points_2019_gas['date']+')'

season_Points_2019_alb =season_Points_2019[season_Points_2019['code']=='ALB']
season_Points_2019_alb['corrida']=season_Points_2019_alb['name']+' ('+season_Points_2019_alb['date']+')'

#season_Points_2019_per =season_Points_2019[season_Points_2019['code']=='PER']

fig2019_season_points = go.Figure()

fig2019_season_points.add_trace(go.Scatter(x=season_Points_2019_ver['corrida'], y=season_Points_2019_ver['points'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = season_Points_2019_ver['color'],
                           marker=dict(color=season_Points_2019_ver['color'])
))
fig2019_season_points.add_trace(go.Scatter(x=season_Points_2019_gas['corrida'], y=season_Points_2019_gas['points'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = season_Points_2019_gas['color'],
                           marker=dict(color=season_Points_2019_gas['color'])
))


fig2019_season_points.add_trace(go.Scatter(x=season_Points_2019_alb['corrida'], y=season_Points_2019_alb['points'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=season_Points_2019_alb['color'])
))


fig2019_season_points.update_layout(layout_results)
fig2019_season_points.update_layout(title = '2019 Season Championship Points per Race ',xaxis_title ="lap",yaxis_title ="points",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# Positions 2020 per Race
df_results_2020 = df_results[(df_results['year']==2020)&((df_results['code']=='VER')|(df_results['code']=='GAS')|(df_results['code']=='ALB')|(df_results['code']=='PER'))]
df_results_2020= df_results_2020.sort_values(by="date")



indexRB_ver_20 = df_results_2020[(df_results_2020['code'] == 'VER')].index
df_results_2020.loc[indexRB_ver_20,'color'] = '#66c2a5'

indexRB_gasly_20 = df_results_2020[(df_results_2020['code'] == 'GAS')].index
df_results_2020.loc[indexRB_gasly_20,'color'] = '#fc8d62'

indexRB_albon_20 = df_results_2020[(df_results_2020['code'] == 'ALB')].index
df_results_2020.loc[indexRB_albon_20,'color'] = '#8da0cb'

indexRB_perez_20 = df_results_2020[(df_results_2020['code'] == 'PER')].index
df_results_2020.loc[indexRB_perez_20,'color'] = '#e78ac3'



df_results_2020_ver =df_results_2020[df_results_2020['code']=='VER']
df_results_2020_ver= df_results_2020_ver.sort_values(by="date")
df_results_2020_ver['corrida']=df_results_2020_ver['name']+' ('+df_results_2020_ver['date']+')'

df_results_2020_gas =df_results_2020[df_results_2020['code']=='GAS']
df_results_2020_gas= df_results_2020_gas.sort_values(by="date")
df_results_2020_gas['corrida']=df_results_2020_gas['name']+' ('+df_results_2020_gas['date']+')'

df_results_2020_per =df_results_2020[df_results_2020['code']=='PER']
df_results_2020_per= df_results_2020_per.sort_values(by="date")
df_results_2020_per['corrida']=df_results_2020_per['name']+' ('+df_results_2020_per['date']+')'

df_results_2020_alb =df_results_2020[df_results_2020['code']=='ALB']
df_results_2020_alb= df_results_2020_alb.sort_values(by="date")
df_results_2020_alb['corrida']=df_results_2020_alb['name']+' ('+df_results_2020_alb['date']+')'

fig_results_2020 = go.Figure()

fig_results_2020 = go.Figure(data=[
    go.Bar(name ='Max Verstappen',x=df_results_2020_ver['corrida'], y=df_results_2020_ver['position'],marker_color=df_results_2020_ver['color']),
    go.Bar(name='Pierre Gasly',x=df_results_2020_gas['corrida'], y=df_results_2020_gas['position'],marker_color=df_results_2020_gas['color']),
    go.Bar(name='Sergio Perez',x=df_results_2020_per['corrida'], y=df_results_2020_per['position'],marker_color=df_results_2020_per['color']),
    go.Bar(name='Alexander Albon',x=df_results_2020_alb['corrida'], y=df_results_2020_alb['position'],marker_color=df_results_2020_alb['color']),

])

fig_results_2020.update_layout(layout_results)
fig_results_2020.update_layout(title = '2020 Grand Prixs Positions per Race',xaxis_title ="Grand Prixs",yaxis_title ="Final Position",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



# 2020 Season Points per Race


season_Points_2020 = season_Points_2020.query("code in ['GAS', 'VER','ALB','PER']")
season_Points_2020 = season_Points_2020.sort_values(by="date")

indexRB_ver_20 = season_Points_2020[(season_Points_2020['code'] == 'VER')].index
season_Points_2020.loc[indexRB_ver_20,'color'] = '#66c2a5'

indexRB_gasly_20 = season_Points_2020[(season_Points_2020['code'] == 'GAS')].index
season_Points_2020.loc[indexRB_gasly_20,'color'] = '#fc8d62'

indexRB_albon_20 = season_Points_2020[(season_Points_2020['code'] == 'ALB')].index
season_Points_2020.loc[indexRB_albon_20,'color'] = '#8da0cb'

indexRB_perez_20 = season_Points_2020[(season_Points_2020['code'] == 'PER')].index
season_Points_2020.loc[indexRB_perez_20,'color'] = '#e78ac3'

season_Points_2020_ver =season_Points_2020[season_Points_2020['code']=='VER']
season_Points_2020_ver['corrida']=season_Points_2020_ver['name']+' ('+season_Points_2020_ver['date']+')'

season_Points_2020_gas =season_Points_2020[season_Points_2020['code']=='GAS']
season_Points_2020_gas['corrida']=season_Points_2020_gas['name']+' ('+season_Points_2019_gas['date']+')'

season_Points_2020_alb =season_Points_2020[season_Points_2020['code']=='ALB']
season_Points_2020_alb['corrida']=season_Points_2020_alb['name']+' ('+season_Points_2020_alb['date']+')'

season_Points_2020_per =season_Points_2020[season_Points_2020['code']=='PER']
season_Points_2020_per['corrida']=season_Points_2020_per['name']+' ('+season_Points_2020_per['date']+')'

fig2020_season_points = go.Figure()

fig2020_season_points.add_trace(go.Scatter(x=season_Points_2020_ver['corrida'], y=season_Points_2020_ver['points'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = season_Points_2020_ver['color'],
                           marker=dict(color=season_Points_2020_ver['color'])
))
fig2020_season_points.add_trace(go.Scatter(x=season_Points_2020_gas['corrida'], y=season_Points_2020_gas['points'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = season_Points_2020_gas['color'],
                           marker=dict(color=season_Points_2020_gas['color'])
))


fig2020_season_points.add_trace(go.Scatter(x=season_Points_2020_alb['corrida'], y=season_Points_2020_alb['points'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=season_Points_2020_alb['color'])
))

fig2020_season_points.add_trace(go.Scatter(x=season_Points_2020_per['corrida'], y=season_Points_2020_per['points'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=season_Points_2020_per['color'])
))

fig2020_season_points.update_layout(layout_results)
fig2020_season_points.update_layout(title = '2020 Season Championship Points per Race ',xaxis_title ="lap",yaxis_title ="points",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


# Positions 2021 per Race

df_results_2021 = df_results[(df_results['year']==2021)&((df_results['code']=='VER')|(df_results['code']=='GAS')|(df_results['code']=='ALB')|(df_results['code']=='PER'))]
df_results_2021r= df_results_2021.sort_values(by="date")

indexRB_ver_21 = df_results_2021[(df_results_2021['code'] == 'VER')].index
df_results_2021.loc[indexRB_ver_21,'color'] = '#66c2a5'

indexRB_gasly_21 = df_results_2021[(df_results_2021['code'] == 'GAS')].index
df_results_2021.loc[indexRB_gasly_21,'color'] = '#fc8d62'


indexRB_perez_21 = df_results_2021[(df_results_2021['code'] == 'PER')].index
df_results_2021.loc[indexRB_perez_21,'color'] = '#e78ac3'


df_results_2021_ver =df_results_2021[df_results_2021['code']=='VER']
df_results_2021_ver= df_results_2021_ver.sort_values(by="date")
df_results_2021_ver['corrida']=df_results_2021_ver['name']+' ('+df_results_2021_ver['date']+')'

df_results_2021_gas =df_results_2021[df_results_2021['code']=='GAS']
df_results_2021_gas= df_results_2021_gas.sort_values(by="date")
df_results_2021_gas['corrida']=df_results_2021_gas['name']+' ('+df_results_2021_gas['date']+')'

df_results_2021_per =df_results_2021[df_results_2021['code']=='PER']
df_results_2021_per= df_results_2021_per.sort_values(by="date")
df_results_2021_per['corrida']=df_results_2021_per['name']+' ('+df_results_2021_per['date']+')'

fig_results_2021 = go.Figure()

fig_results_2021 = go.Figure(data=[
    go.Bar(name ='Max Verstappen',x=df_results_2021_ver['corrida'], y=df_results_2021_ver['position'],marker_color=df_results_2021_ver['color']),
    go.Bar(name='Pierre Gasly',x=df_results_2021_gas['corrida'], y=df_results_2021_gas['position'],marker_color=df_results_2021_gas['color']),
    go.Bar(name='Sergio Perez',x=df_results_2021_per['corrida'], y=df_results_2021_per['position'],marker_color=df_results_2021_per['color']),

])

fig_results_2021.update_layout(layout_results)
fig_results_2021.update_layout(title = '2021 Grand Prixs Positions per Race',xaxis_title ="Grand Prixs",yaxis_title ="Final Position",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))


season_Points_2021_ = season_Points_2021.query("code in ['GAS', 'VER','ALB','PER']")
season_Points_2021_ = season_Points_2021.sort_values(by="date")

indexRB_ver_21 = season_Points_2021[(season_Points_2021['code'] == 'VER')].index
season_Points_2021.loc[indexRB_ver_21,'color'] = '#66c2a5'

indexRB_gasly_21 = season_Points_2021[(season_Points_2021['code'] == 'GAS')].index
season_Points_2021.loc[indexRB_gasly_21,'color'] = '#fc8d62'

indexRB_albon_21 = season_Points_2021[(season_Points_2021['code'] == 'ALB')].index
season_Points_2021.loc[indexRB_albon_21,'color'] = '#8da0cb'

indexRB_perez_21 = season_Points_2021[(season_Points_2021['code'] == 'PER')].index
season_Points_2021.loc[indexRB_perez_21,'color'] = '#e78ac3'

season_Points_2021_ver =season_Points_2021[season_Points_2021['code']=='VER']
season_Points_2021_ver = season_Points_2021_ver.sort_values(by="date")
season_Points_2021_ver['corrida']=season_Points_2021_ver['name']+' ('+season_Points_2021_ver['date']+')'

season_Points_2021_gas =season_Points_2021[season_Points_2021['code']=='GAS']
season_Points_2021_gas = season_Points_2021_gas.sort_values(by="date")
season_Points_2021_gas['corrida']=season_Points_2021_gas['name']+' ('+season_Points_2021_gas['date']+')'

season_Points_2021_alb =season_Points_2021[season_Points_2021['code']=='ALB']
season_Points_2021_alb = season_Points_2021_alb.sort_values(by="date")
season_Points_2021_alb['corrida']=season_Points_2021_alb['name']+' ('+season_Points_2021_alb['date']+')'

season_Points_2021_per =season_Points_2021[season_Points_2021['code']=='PER']
season_Points_2021_per = season_Points_2021_per.sort_values(by="date")
season_Points_2021_per['corrida']=season_Points_2021_per['name']+' ('+season_Points_2021_per['date']+')'

fig2021_season_points = go.Figure()

fig2021_season_points.add_trace(go.Scatter(x=season_Points_2021_ver['corrida'], y=season_Points_2021_ver['points'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = season_Points_2021_ver['color'],
                           marker=dict(color=season_Points_2021_ver['color'])
))
fig2021_season_points.add_trace(go.Scatter(x=season_Points_2021_gas['corrida'], y=season_Points_2021_gas['points'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = season_Points_2021_gas['color'],
                           marker=dict(color=season_Points_2021_gas['color'])
))


fig2021_season_points.add_trace(go.Scatter(x=season_Points_2021_alb['corrida'], y=season_Points_2021_alb['points'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=season_Points_2021_alb['color'])
))

fig2021_season_points.add_trace(go.Scatter(x=season_Points_2021_per['corrida'], y=season_Points_2021_per['points'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=season_Points_2021_per['color'])
))

fig2021_season_points.update_layout(layout_results)
fig2021_season_points.update_layout(title = '2021 Season Championship Points per Race ',xaxis_title ="lap",yaxis_title ="points",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))

df_results_2022 = df_results[(df_results['year'] == 2022) & (
            (df_results['code'] == 'VER') | (df_results['code'] == 'GAS') | (df_results['code'] == 'ALB') | (
                df_results['code'] == 'PER'))]
df_results_2022 = df_results_2022.sort_values(by="date")

indexRB_ver_22 = df_results_2022[(df_results_2022['code'] == 'VER')].index
df_results_2022.loc[indexRB_ver_22, 'color'] = '#66c2a5'

indexRB_gasly_22 = df_results_2022[(df_results_2022['code'] == 'GAS')].index
df_results_2022.loc[indexRB_gasly_22, 'color'] = '#fc8d62'

indexRB_albon_22 = df_results_2022[(df_results_2022['code'] == 'ALB')].index
df_results_2022.loc[indexRB_albon_22, 'color'] = '#8da0cb'

indexRB_perez_22 = df_results_2022[(df_results_2022['code'] == 'PER')].index
df_results_2022.loc[indexRB_perez_22, 'color'] = '#e78ac3'

df_results_2022_ver = df_results_2022[df_results_2022['code'] == 'VER']
df_results_2022_ver = df_results_2022_ver.sort_values(by="date")
df_results_2022_ver['corrida'] = df_results_2022_ver['name'] + ' (' + df_results_2022_ver['date'] + ')'

df_results_2022_gas = df_results_2022[df_results_2022['code'] == 'GAS']
df_results_2022_gas = df_results_2022_gas.sort_values(by="date")
df_results_2022_gas['corrida'] = df_results_2022_gas['name'] + ' (' + df_results_2022_gas['date'] + ')'

df_results_2022_per = df_results_2022[df_results_2022['code'] == 'PER']
df_results_2022_per = df_results_2022_per.sort_values(by="date")
df_results_2022_per['corrida'] = df_results_2022_per['name'] + ' (' + df_results_2022_per['date'] + ')'

df_results_2022_alb = df_results_2022[df_results_2022['code'] == 'ALB']
df_results_2022_alb = df_results_2022_alb.sort_values(by="date")
df_results_2022_alb['corrida'] = df_results_2022_alb['name'] + ' (' + df_results_2022_alb['date'] + ')'

fig_results_2022 = go.Figure()

fig_results_2022 = go.Figure(data=[
    go.Bar(name='Max Verstappen', x=df_results_2022_ver['corrida'], y=df_results_2022_ver['position'],
           marker_color=df_results_2022_ver['color']),
    go.Bar(name='Pierre Gasly', x=df_results_2022_gas['corrida'], y=df_results_2022_gas['position'],
           marker_color=df_results_2022_gas['color']),
    go.Bar(name='Sergio Perez', x=df_results_2022_per['corrida'], y=df_results_2022_per['position'],
           marker_color=df_results_2022_per['color']),
    go.Bar(name='Alexander Albon', x=df_results_2022_alb['corrida'], y=df_results_2022_alb['position'],
           marker_color=df_results_2022_alb['color']),

])

fig_results_2022.update_layout(layout_results)
fig_results_2022.update_layout(title='2022 Grand Prixs Positions per Race', xaxis_title="Grand Prixs",
                               yaxis_title="Final Position",
                               legend_title="Drivers",
                               font=dict(family="Courier New, monospace", size=12, color="Black"))

season_Points_2022 = season_Points_2022.query("code in ['GAS', 'VER','ALB','PER']")
season_Points_2022 = season_Points_2022.sort_values(by="date")

indexRB_ver_22 = season_Points_2022[(season_Points_2022['code'] == 'VER')].index
season_Points_2022.loc[indexRB_ver_22,'color'] = '#66c2a5'

indexRB_gasly_22 = season_Points_2022[(season_Points_2022['code'] == 'GAS')].index
season_Points_2022.loc[indexRB_gasly_22,'color'] = '#fc8d62'

indexRB_albon_22 = season_Points_2022[(season_Points_2022['code'] == 'ALB')].index
season_Points_2022.loc[indexRB_albon_22,'color'] = '#8da0cb'

indexRB_perez_22 = season_Points_2022[(season_Points_2022['code'] == 'PER')].index
season_Points_2022.loc[indexRB_perez_22,'color'] = '#e78ac3'

season_Points_2022_ver =season_Points_2022[season_Points_2022['code']=='VER']
season_Points_2022_ver['corrida']=season_Points_2022_ver['name']+' ('+season_Points_2022_ver['date']+')'

season_Points_2022_gas =season_Points_2022[season_Points_2022['code']=='GAS']
season_Points_2022_gas['corrida']=season_Points_2022_gas['name']+' ('+season_Points_2022_gas['date']+')'

season_Points_2022_alb =season_Points_2022[season_Points_2022['code']=='ALB']
season_Points_2022_alb['corrida']=season_Points_2022_alb['name']+' ('+season_Points_2022_alb['date']+')'

season_Points_2022_per =season_Points_2022[season_Points_2022['code']=='PER']
season_Points_2022_per['corrida']=season_Points_2022_per['name']+' ('+season_Points_2022_per['date']+')'

fig2022_season_points = go.Figure()

fig2022_season_points.add_trace(go.Scatter(x=season_Points_2022_ver['corrida'], y=season_Points_2022_ver['points'],
                    mode='lines+markers',
                    name='Max Verstappen',marker_color = season_Points_2022_ver['color'],
                           marker=dict(color=season_Points_2022_ver['color'])
))
fig2022_season_points.add_trace(go.Scatter(x=season_Points_2022_gas['corrida'], y=season_Points_2022_gas['points'],
                    mode='lines+markers',
                    name='Pierre Gasly',
                           marker_color = season_Points_2022_gas['color'],
                           marker=dict(color=season_Points_2022_gas['color'])
))


fig2022_season_points.add_trace(go.Scatter(x=season_Points_2022_alb['corrida'], y=season_Points_2022_alb['points'],
                    mode='lines+markers',
                    name='Alexander Albon',
                           marker=dict(color=season_Points_2022_alb['color'])
))

fig2022_season_points.add_trace(go.Scatter(x=season_Points_2022_per['corrida'], y=season_Points_2022_per['points'],
                    mode='lines+markers',
                    name='Sergio Perez',
                           marker=dict(color=season_Points_2022_per['color'])
))

fig2022_season_points.update_layout(layout_results)
fig2022_season_points.update_layout(title = '2022 Season Championship Points per Race ',xaxis_title ="lap",yaxis_title ="points",
                        legend_title="Drivers",font=dict(family="Courier New, monospace",size=12,color="Black"))



layout = html.Div([

    html.Div(className='service-box', children=[
        html.Div(children=[html.P("Choose the Season: ", style={'font-size': '20px', 'font-weight': 'bold'}),

                           dcc.Dropdown(id="dropdown",
                                        options=[
                                            {'label': x, 'value': x}
                                            for x in ['2019', '2020', '2021', '2022']
                                        ],
                                        value='2019', clearable=False),
                           ]),
        dcc.Graph(id='season1', figure=fig2019_season_points),
        dcc.Graph(id='race1', figure=fig_results_2019)
    ])
    
])


@callback(Output('season1', 'figure'), Output('race1', 'figure'), Input('dropdown', 'value'))
def display_figure(value):

    if value == '2019':
        return fig2019_season_points, fig_results_2019

    elif value == '2020':
        return fig2020_season_points, fig_results_2020

    elif value == '2021':
        return fig2021_season_points, fig_results_2021

    elif value == '2022':
        return fig2022_season_points, fig_results_2022
