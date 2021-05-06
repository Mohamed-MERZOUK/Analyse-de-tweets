from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import Home, Analyse_by_keyword
import grasia_dash_components as gdc
from app import df_tweet
from functions.Plots import wordCloud

globalActiveSideBar = ""

sideBar = html.Nav(
    id='sidebar',
    children=[
        html.Div(
            children=html.H3('Covid-19'),
            className='sidebar-header'
        ),
        html.Hr(),
        html.Ul(
            className='list-unstyled components',

            children=[

                html.Li(
                    className='active',
                    children=[
                        html.Li(
                            dbc.NavLink(
                                'Home',
                                href="/",
                            )
                        ),
                        html.Li(
                            dbc.NavLink(
                                'Analyse by keyword',
                                href="/analysebykeyword",
                            )
                        ),
                        html.Li(
                            dbc.NavLink(
                                'Analyse du Topic modeling',
                                href="/analysetopicmodeling",
                            )
                        ),
                    ]
                ),

            ]
        )
    ]

)

navBar = html.Div(
    children=[
        html.Nav(
            className='navbar navbar-expand-lg navbar-light bg-light',
            children=[
                html.Div(
                    id="buttonNavcontainer",
                    className='container-fluid',
                    children=[
                        html.Button(
                            type='button',
                            id='sidebarCollapse',
                            className='btn btn-info',
                            children=[
                                html.I(className='fas fa-align-left'),

                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
app.layout = html.Div(
    [
        dcc.Location(id="url"), sideBar,
        html.Div([navBar, html.Div([], id="content-page")],
                 id='content', style={"font-size": "12px"})
    ],
    className="wrapper")


@app.callback(
    [Output('sidebar', 'className'), Output('content', 'className')],
    [Input('sidebarCollapse', 'n_clicks')])
def clicks(n_clicks):
    global globalActiveSideBar
    if (globalActiveSideBar == ""):
        globalActiveSideBar = "active"
        return ['active', 'active']
    else:
        globalActiveSideBar = ""
        return ['', '']


@app.callback(Output("content-page", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return Home.layout
    if pathname == "/analysebykeyword":
        return Analyse_by_keyword.layout
    if pathname == "/analysetopicmodeling":
        return Home.layout
    elif pathname == "/exec":
        return html.Div(html.H1("bbbbbb"))

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
