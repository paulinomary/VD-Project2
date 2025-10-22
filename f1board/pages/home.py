import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Home', href='/home')

layout=(
    html.P(),
    html.Div(className='box-shadow-full', children=[
        html.P('''Dashboard'''),
        html.P('''Descrição'''),
        html.P('Us')
    ]))
