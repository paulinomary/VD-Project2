import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, callback
import pandas as pd

dash.register_page(__name__, name='Races')

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page smth and much more!')
    ]
)