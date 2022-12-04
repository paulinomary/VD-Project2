import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.YETI])
dash.register_page(__name__, name='Home', href="/")

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    dbc.Col(dbc.NavbarBrand("Formula 1 - Red Bull Analysis 🏎️", className="ms-2")),
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                [
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [   dbc.NavItem(dbc.NavLink("Races", href = "/races", style= {'color': '#9e9e9e'})),
                                dbc.NavItem(dbc.NavLink("Standings Race by Race", href = "/standingsrace", style= {'color': '#9e9e9e'})),
                                dbc.NavItem(dbc.NavLink("Standings Season", href = "/standingsseason", style= {'color': '#9e9e9e'}),className="me-auto"),
                                dbc.NavItem(dbc.Button("More About Formula 1", active=True, outline = True, href = "https://www.formula1.com/", style= {'color': '#ff0303', 'background-color':'#ffffff'})),
                            ],
                            className="w-100",
                        ),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
                className="flex-grow-1",
            ),
        ],
        fluid=True,
    ),
    dark=True,
    color="dark",
)

app.layout = dbc.Container([

    dbc.Row(
        [navbar, dash.page_container]
    ),

], fluid=True)



if __name__ == "__main__":
    app.run(debug=False)


