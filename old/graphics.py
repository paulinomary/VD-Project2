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

marker = dict(
    color='black'
)

# 2019 ALL Drivers Standings Season Standings
h2019 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2019.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2019 = h2019.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2019.dropna(inplace = True)

viz2019.points = viz2019.points.astype('int64')
viz2019.wins = viz2019.wins.astype('int64')
viz2019.date = pd.to_datetime(viz2019.date)
    
top2019 = viz2019[viz2019.loc[:,'year'] == 2019]
top2019 = top2019.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

# fig shows the bar graph of 2019 season points for all drivers
fig2019 = px.bar(top2019, x='surname', y='points',hover_data=['wins'], color='points',color_continuous_scale='greys',height=400, text_auto=True)
fig2019.update_traces(textfont_size=20,marker=dict(line=dict(color='#000000', width=2)),textposition="outside", cliponaxis=False)
fig2019.update_xaxes(showgrid=False)
fig2019.update_yaxes(showgrid=False)
fig2019.update_layout(layout)
fig2019.show()

#df 2020
df_2020_2 = df2[df2['year'] == 2020]

# 2020 Season Gran Prixs info
df_laps_2020 = df[(df['year']==2020)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2020.rename(columns={'position':'lap position'},inplace=True)
df_laps_2020 = df_laps_2020.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2020 = df_laps_2020.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2020['stop'].fillna(0,inplace=True)
df_laps_2020['stop']=df_laps_2020['stop'].astype(int)
df_laps_2020['stop'][df_laps_2020['stop']==0] = ''
df_laps_2020

# 2020 Season Drivers Standings
h2020 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2020.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2020 = h2020.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2020.dropna(inplace = True)

viz2020.points = viz2020.points.astype('int64')
viz2020.wins = viz2020.wins.astype('int64')
viz2020.date = pd.to_datetime(viz2020.date)
    
top2020 = viz2020[viz2020.loc[:,'year'] == 2020]
top2020 = top2020.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

fig2020 = px.bar(top2020, x='surname', y='points',hover_data=['wins'], color='points',height=400,color_continuous_scale= 'greys',text_auto=True)
fig2020.update_traces(textfont_size=20,marker=dict(line=dict(color='#000000', width=2)),textposition="outside", cliponaxis=False)
fig2020.update_xaxes(showgrid=False)
fig2020.update_yaxes(showgrid=False)
fig2020.update_layout(layout)

fig2020.show()

# 2021 Season races info

df_laps_2021 = df[(df['year']==2021)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2021.rename(columns={'position':'lap position'},inplace=True)
df_laps_2021 = df_laps_2021.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2021 = df_laps_2021.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2021['stop'].fillna(0,inplace=True)
df_laps_2021['stop']=df_laps_2021['stop'].astype(int)
df_laps_2021['stop'][df_laps_2021['stop']==0] = ''
df_laps_2021

# 2021 Season
df_2021 = df_laps_2021[df_laps_2021['year'] == 2021]
df_2021

# 2021 Season - Driver Standings

h2021 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2021.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2021 = h2021.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2021.dropna(inplace = True)

viz2021.points = viz2021.points.astype('int64')
viz2021.wins = viz2021.wins.astype('int64')
viz2021.date = pd.to_datetime(viz2021.date)
    
top2021 = viz2021[viz2021.loc[:,'year'] == 2021]
top2021 = top2021.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

fig2021 = px.bar(top2021, x='surname', y='points',hover_data=['wins'], color='points',height=400,color_continuous_scale= 'greys',text_auto = True)
fig2021.update_traces(textfont_size=20,marker=dict(line=dict(color='#000000', width=2)),textposition="outside", cliponaxis=False)
fig2021.update_xaxes(showgrid=False)
fig2021.update_yaxes(showgrid=False)
fig2021.update_layout(layout)

fig2021.show()

# 2022 Season races info

df_laps_2022 = df[(df['year']==2022)&((df['code']=='VER')|(df['code']=='GAS'))|(df['driverRef']=='albon')|(df['driverRef']=='perez')].copy()
df_laps_2022.rename(columns={'position':'lap position'},inplace=True)
df_laps_2022 = df_laps_2022.merge(results[['raceId','driverId','position']],how='left',on=['raceId','driverId'])
df_laps_2022 = df_laps_2022.merge(pit_stops[['raceId','driverId','lap','stop']],how='left',on=['raceId','driverId','lap'])
df_laps_2022['stop'].fillna(0,inplace=True)
df_laps_2022['stop']=df_laps_2022['stop'].astype(int)
df_laps_2022['stop'][df_laps_2022['stop']==0] = ''
df_laps_2022

# 2022 Season
df_2022 = df_laps_2022[df_laps_2022['year'] == 2022]
df_2022

# 2022 Drivers Standings 

h2022 = driver_position.merge(circuits,left_on='circuitId',right_on='circuitId',how = 'left')
h2022.rename(columns={'name_y':'circuit_name'},inplace=True)
viz2022 = h2022.loc[:,['date','year','circuit_name','surname','points','wins']]

viz2022.dropna(inplace = True)

viz2022.points = viz2022.points.astype('int64')
viz2022.wins = viz2022.wins.astype('int64')
viz2022.date = pd.to_datetime(viz2022.date)
    
top2022 = viz2022[viz2022.loc[:,'year'] == 2022]
top2022 = top2022.groupby(['surname'])[['points','wins']].max().sort_values('points',ascending = False).head(20).reset_index()

fig2022 = px.bar(top2022, x='surname', y='points',hover_data=['wins'], color='points',height=400,color_continuous_scale= 'greys', text_auto=True)
fig2022.update_traces(textfont_size=20,marker=dict(line=dict(color='#000000', width=2)),textposition="outside", cliponaxis=False)
fig2022.update_xaxes(showgrid=False)
fig2022.update_yaxes(showgrid=False)
fig2022.update_layout(layout)

fig2022.show()