import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output
import pandas as pd


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.YETI])

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    dbc.Col(dbc.NavbarBrand("Formula 1 - Red Bull Analysis 🏎️", className="ms-2")),
                    align="center",
                    className="g-0",
                ),
                href="/home",
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                [
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [   dbc.NavItem(dbc.NavLink("Home", href="/home", className='nav-link'), className="me-auto"),
                                #dbc.NavItem(dbc.NavLink("Meet the Drivers", href = "/drivers",className='nav-link'), className="me-auto"),
                                dbc.NavItem(dbc.NavLink("Races", href="/races", className='nav-link'), className="me-auto"),
                                dbc.NavItem(dbc.NavLink("Standings Race by Race", href="/racestandings",className='nav-link'), className="me-auto"),
                                dbc.NavItem(dbc.NavLink("Standings Season", href="/seasonstandings",
                                                        className='nav-link'), className="me-auto"),
                                dbc.NavItem(dbc.Button("More About Formula 1", active=True, outline=True,
                                                       href="https://www.formula1.com/",
                                                       style={'color': '#ff0303', 'background-color': '#ffffff', 'border-radius': '0.2rem', 'font-weight': '600'})),
                            ],
                            className="w-100",
                        ),
                        id="navbar-collapse",
                        is_open=True,
                        navbar=True,
                    ),
                ],
                className="flex-grow-1",
            )
        ],
        fluid=True,
    ), style={'border-radius': '0.5rem'},
    dark=True,
    color="dark",
)

app.layout = dbc.Card(
        [
            dbc.CardImg(src='./assets/starting.jpeg',
                        style={'background-size': 'cover', 'background-attachment': 'fixed',
                               'background-position': 'center center', 'background-repeat': 'no-repeat'}),
            dbc.CardImgOverlay([navbar, dash.page_container])
        ], style={"maxWidth": 5000})

if __name__ == "__main__":
    port = 8050
    app.run_server(debug=True, port=port)
