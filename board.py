from dash import Dash, dcc, html
from dash.dependencies import Input, Output 
import plotly.graph_objects as go
app = Dash(__name__)
app.layout = html.Div([
    html.P("Color:"),
    dcc.Dropdown(
        id="dropdown",
        options=[
            {'label': x, 'value': x}
for x in ['#37bbe7', '#5e90aa', '#feb3c7', '#2e5189']
],
value='#37bbe7', clearable=False,
),
    dcc.Graph(id="graph"),
])
@app.callback(
    Output("graph", "figure"),
    [Input("dropdown", "value")])
def display_color(color): 
    print(color)
    fig = go.Figure(
    data=go.Bar(y=[2, 3, 1], marker_color=color))
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)