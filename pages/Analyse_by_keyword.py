import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from functions.Utils import get_tags, get_random_element, read_workingDf
from app import app
from dash.dependencies import Input, Output, State
from base64 import urlsafe_b64encode
import grasia_dash_components as gdc
import dash_defer_js_import as dji
from functions.Components import card, cardMultiProgress
import pandas as pd
import plotly.express as px
from app import df_tweet
from functions.Stats import hachtags_numbers, mentions_numbers, getGenderCounts
import plotly.graph_objects as go
from functions.Plots import simple_map, treeMap, wordCloud, word_freq_tweet, cluster_map, timeseriesCount
import dash_leaflet as dl
import dash_leaflet.express as dlx


layout = dbc.Container(
    [
        html.H5(
            "Analyse by keywords",
            style={
                "position": "absolute", "top": "0", "right": "0",
                "padding": "0.5em 1em", "background-color": "#456987",
                "color": "#fafafa", "z-index": "99999"
            }
        ),
        dbc.Row(
            html.H3("Number of tweets posted over time", className="mx-auto"),
            style={"margin": "40px 0 0 0"}
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph-timeseriesCount",
                        figure=timeseriesCount(read_workingDf())), width=12)
            ]
        ),
        dbc.Row(
            html.H3("Hachtags and Mentions", className="mx-auto"),
            style={"margin": "40px 0 20px 0"}
        ),
        dbc.Row(
            [
                dbc.Col(card(title="tweets without hachtags", value=str(hachtags_numbers(df_tweet.values.tolist())[
                        0][0]), progress=str(hachtags_numbers(df_tweet.values.tolist())[0][1]))),
                dbc.Col(card(title="tweets with hachtags", value=str(hachtags_numbers(df_tweet.values.tolist())[
                        1][0]), progress=str(hachtags_numbers(df_tweet.values.tolist())[1][1]))),
                dbc.Col(card(title="tweets without mentions", value=str(mentions_numbers(df_tweet.values.tolist())[
                        0][0]), progress=str(mentions_numbers(df_tweet.values.tolist())[0][1]))),
                dbc.Col(card(title="tweets with mentions", value=str(mentions_numbers(df_tweet.values.tolist())[
                        1][0]), progress=str(mentions_numbers(df_tweet.values.tolist())[1][1]))),
            ]
        ),
        dbc.Row(
            html.H3("Variation of tweets count over time", className="mx-auto"),
            style={"margin": "60px 0 0 0"}
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Controleur")),
                        dbc.CardBody([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Frequence per :"),
                                    dcc.Dropdown(
                                        id='algo-1',
                                        options=[{'label': i[0], 'value': i[1]}
                                                 for i in [('Days', '1D'), ('Weeks', '1W'), ('Months', '1M')]],
                                        value="1D",
                                        searchable=False,
                                        clearable=False,

                                    ),
                                ]
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Frequence per :"),
                                    dcc.Dropdown(
                                        id='algo-2',
                                        options=[{'label': i[0], 'value': i[1]}
                                                 for i in [('Favorite', 'favorite_count'), ('Retweets', 'retweet_count')]],
                                        value="favorite_count",
                                        searchable=False,
                                        clearable=False,

                                    ),
                                ]
                            )
                        ]
                        )],
                    ),
                    style={"padding-top": "100px"},
                    width=3
                ),

                dbc.Col(dcc.Graph(id="graph-timeseries"), width=9)

            ],
        ),
        dbc.Row(
            html.H3("Proportion of users gender", className="mx-auto"),
            style={"margin": "40px 0 20px 0"}
        ),
        dbc.Row(
            [
                dbc.Col(cardMultiProgress(title1="Hommes", title2="Femmes", value1=str(getGenderCounts(df_tweet)["male"]), value2=str(getGenderCounts(df_tweet)["female"]),
                                          progress1=str(int(int(getGenderCounts(df_tweet)["male"])*100/300)), progress2=str(int(int(getGenderCounts(df_tweet)["male"]))*100/300))),
            ]
        ),
        dbc.Row(
            html.H3("Sentiment Analysis", className="mx-auto"),
            style={"margin": "60px 0 20px 0"}
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Controleur")),
                    dbc.CardBody([
                        dbc.FormGroup(
                            [
                                dbc.Label("Last :"),
                                dcc.Dropdown(
                                    id='period',
                                    options=[{'label': i[0], 'value': i[1]}
                                             for i in [('Month', '1'), ('3 Months', '3'), ('6 Months', '6'), ('Year', '12')]],
                                    value="1",
                                    searchable=False,
                                    clearable=False,

                                ),
                            ]
                        )
                    ])]), width=3),
                dbc.Col(
                    dcc.Graph(id="graph-sentiment"),
                    width=9
                )

            ]
        ),
        dbc.Row(
            html.H3("Words Analysis", className="mx-auto"),
            style={"margin": "40px 0 20px 0"}
        ),
        dbc.Row(
            dbc.Col(
                [
                    # html.Img(id="graph-wordcloud", src=".\\assets\\alice.png")
                ]
            )
        ),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Tabs(id='tabs-example', children=[
                        dcc.Tab(label='TreeMap', children=[
                            dcc.Graph(figure=treeMap(df_tweet))
                        ]),
                        dcc.Tab(label='WordCloud', children=[
                            dcc.Graph(figure=wordCloud(df_tweet))
                        ]),
                    ]),

                ]
            )

        ]
        ),
        dbc.Row(
            html.H3("Tweets length destribution", className="mx-auto"),
            style={"margin": "40px 0 0 0"}
        ),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(figure=word_freq_tweet(df_tweet))
                ]
            )

        ]
        ),
        dbc.Row(
            html.H3("Tweets geographic destribution", className="mx-auto"),
            style={"margin": "40px 0 20px 0"}
        ),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Tabs(id='tabs-example2', children=[
                        dcc.Tab(label='Simple map', children=[
                             dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer")], id="map", style={
                                'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
                             ]),
                        dcc.Tab(label='Cluster map', children=[
                            dl.Map([dl.TileLayer(), dl.GeoJSON(id="cluster-data", cluster=True, zoomToBoundsOnClick=True)], id="map-cluster", style={
                                'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
                        ]),
                    ]),

                ]
            )
        ]
        ),
    ],
)


@app.callback(
    Output('graph-timeseries', 'figure'),
    [Input('algo-1', 'value'),
     Input('algo-2', 'value')])
def update_graph_dist(dist_var1, dist_var2):

    df = df_tweet.copy()
    df_time = df[['created_at', 'retweet_count', 'favorite_count']].groupby(pd.Grouper(key="created_at",
                                                                                       freq=dist_var1)).sum().reset_index()

    fig = px.line(df_time, x='created_at', y=dist_var2)
    fig.layout.paper_bgcolor = '#fafafa'

    fig.update_layout(
        xaxis=dict(
            title="Date",
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='black',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            title="Number of tweets",
            showgrid=True,
            linecolor='black',
            zeroline=False,
            showline=False,
            gridcolor="rgb(82,82,82)",
        ),
        showlegend=False,
        plot_bgcolor='#fafafa'
    )
    fig.update_traces(line_color='#456987')
    return fig


@app.callback(
    Output('graph-sentiment', 'figure'),
    [Input('period', 'value')])
def update_graph_sent(dist_var):

    df = df_tweet.copy()

    labels = ['Positive', 'Negative']
    values = ['1000', '500']
    colors = ['#EF553B', 'rgb(102,194,165)']

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_layout(
        autosize=False,
        # width=500,
        # height=500,
        margin=dict(
            l=100,
            r=10,
            b=100,
            t=10,
            pad=10
        ),
        paper_bgcolor="#fafafa",
    )

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors))

    return fig


# @app.callback(Output("layer", "children"), [Input("map", "click_lat_lng")])
# def map_click(click_lat_lng):
#     pos = simple_map(df_tweet, nb_makers=100)
#     return pos


@app.callback(Output("cluster-data", "data"), [Input("map-cluster", "click_lat_lng")])
def map_click_2(click_lat_lng):
    pos = cluster_map(df_tweet, nb_makers=20)
    return dlx.dicts_to_geojson(pos)
