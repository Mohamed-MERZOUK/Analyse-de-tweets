import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from functions.Utils import get_tags, get_random_element
from app import app
from dash.dependencies import Input, Output, State
from base64 import urlsafe_b64encode
import grasia_dash_components as gdc
import dash_defer_js_import as dji
from functions.Components import card
import pandas as pd
import plotly.express as px

layout = dbc.Container(
    [

        dbc.Row(
            [
                dbc.Col(card()),
                dbc.Col(card()),
                dbc.Col(card()),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Controleur")),
                    dbc.CardBody([
                        dbc.FormGroup(
                            [
                                dbc.Label("algorithme"),
                                dcc.Dropdown(
                                    id='algo-1',
                                    options=[{'label': i[0], 'value': i[1]}
                                             for i in [('Days', '1D'), ('Weeks', '1W'), ('Months', '1M')]],
                                    value="1D",
                                    searchable=False,
                                    clearable=False,

                                ),
                            ]
                        )
                    ])]), width=3),
                dbc.Col(dcc.Graph(id="dist-graph-11"), width=9)

            ]
        )
    ],
)


@app.callback(
    Output('dist-graph-11', 'figure'),
    [Input('algo-1', 'value')])
def update_graph_dist(dist_var):

    print(dist_var)
    df = pd.DataFrame(
        {
            "Publish date": [
                pd.Timestamp("2000-01-02"),
                pd.Timestamp("2000-01-02"),
                pd.Timestamp("2000-01-09"),
                pd.Timestamp("2000-01-16")
            ],
            "ID": [0, 1, 2, 3],
            "Price": [10, 20, 30, 40]
        }
    )
    df_time = df.groupby(pd.Grouper(key="Publish date",
                                    freq="1D")).count().reset_index()
    df_time = df_time.rename(columns={'Price': 'count'})

    # df = df_tweet.groupby(pd.Grouper(
    #     key="created_at", freq=dist_var)).count().reset_index()
    # df = df.rename(columns={'truncated': 'count'})
    fig = px.line(df_time, x='Publish date', y="count")
    return fig
