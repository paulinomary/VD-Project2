## Standings Race by Race
import dash
from dash import html, dcc

dash.register_page(__name__, name='Standigns Race by Race')

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 3 and much more!')
    ]
)