import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from functions.Utils import get_tags, get_random_element
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
from functions.Plots import wordCloud

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(card(title="tweets without hachtags", value=str(hachtags_numbers(df_tweet.values.tolist())[0][0]), progress=str(hachtags_numbers(df_tweet.values.tolist())[0][1]))),
                dbc.Col(card(title="tweets with hachtags", value=str(hachtags_numbers(df_tweet.values.tolist())[1][0]), progress=str(hachtags_numbers(df_tweet.values.tolist())[1][1]))),
                dbc.Col(card(title="tweets without mentions", value=str(mentions_numbers(df_tweet.values.tolist())[0][0]), progress=str(mentions_numbers(df_tweet.values.tolist())[0][1]))),
                dbc.Col(card(title="tweets with mentions", value=str(mentions_numbers(df_tweet.values.tolist())[1][0]), progress=str(mentions_numbers(df_tweet.values.tolist())[1][1]))),
            ]
        ),
        dbc.Row(
            html.H3("Variation of tweets count over time", className="mx-auto"),
            style={"margin" : "20px 0"}
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card([
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
                        )
                    ])]), width=3),
                dbc.Col(dcc.Graph(id="graph-timeseries"), width=9)

            ]
        ),
        dbc.Row(
            html.H3("Proportion of users gender", className="mx-auto"),
            style={"margin" : "20px 0"}
        ),
        dbc.Row(
            [
                dbc.Col(cardMultiProgress(title1="Hommes", title2="Femmes", value1=str(getGenderCounts(df_tweet)["male"]), value2=str(getGenderCounts(df_tweet)["female"]), 
                                            progress1=str( int(int(getGenderCounts(df_tweet)["male"])*100/300)), progress2=str( int(int(getGenderCounts(df_tweet)["male"]))*100/300))),
            ]
        ),
        dbc.Row(
            html.H3("Sentiment Analysis", className="mx-auto"),
            style={"margin" : "20px 0"}
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
            dbc.Col(
                [
                    html.Button(id='invisible_button', style={'display':'none'}),
                    html.Img(id="graph-wordcloud", src=".\\assets\\alice.png")
                ]
            )
        )
    ],
)


@app.callback(
    Output('graph-timeseries', 'figure'),
    [Input('algo-1', 'value')])
def update_graph_dist(dist_var):

    df = df_tweet.copy()
    df_time = df.groupby(pd.Grouper(key="created_at",
                                    freq=dist_var)).count().reset_index()
    df_time = df_time.rename(columns={'favorite_count': 'sum'})

    # df = df_tweet.groupby(pd.Grouper(
    #     key="created_at", freq=dist_var)).count().reset_index()
    # df = df.rename(columns={'truncated': 'count'})
    fig = px.line(df_time, x='created_at', y="sum")
    fig.layout.paper_bgcolor = '#fafafa'
    #fig.layout.plot_bgcolor = "#fff"
    return fig


@app.callback(
    Output('graph-sentiment', 'figure'),
    [Input('period', 'value')])
def update_graph_sent(dist_var):

    df = df_tweet.copy()

    labels = ['Positive','Negative']
    values = ['1000','500']
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


@app.callback(
    Output('graph-wordcloud', 'src'),
    [Input('url','pathname')])
def update_graph_wordcloud(dist_var):
    #print("aaaa\n\n")
    df = df_tweet.copy()
    return wordCloud(df)