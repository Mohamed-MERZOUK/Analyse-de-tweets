import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from functions.Utils import get_tags, get_random_element
from app import app, df_tweet, tweetsIdsByTopic
from dash.dependencies import Input, Output, State
from base64 import urlsafe_b64encode
import dash_defer_js_import as dji
from functions.NLP import predictTopic
import time
import os
import pandas as pd

df_tweet_home = df_tweet.copy()

layout = dbc.Container(
    [

        html.H5(
            "Home",
            style={
                "position": "absolute", "top": "0", "right": "0",
                "padding": "0.5em 1em", "background-color": "#456987",
                "color": "#fafafa", "z-index": "99999"
            }
        ),

        dbc.Row(
            html.H2("Advenced Tweets Analyzer for Covid-19", style={
                    "margin-bottom": "30px"}, className="mx-auto")
        ),
        dbc.Row([
            dbc.Col(
                [
                    dbc.Input(id="input_keyword", type="text",
                              placeholder="keywords", className="mb-10")
                ],
                width=10,
            ),
            dbc.Col(
                [
                    dcc.Dropdown(id="select_algo",
                                 className="mb-10",
                                 options=[{'label': i, 'value': i}
                                          for i in ["NMF", "LDA"]],
                                 value="LDA",
                                 searchable=False,
                                 clearable=False,)
                ],
                width=2,
            )
        ]

        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Button("Submit", id="input_key_button", n_clicks=0, style={
                               "margin-top": "30px"}, className="btn btn-secondary btn-lg btn-block"),
                ],
                width=12,
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Div(id="output_keywords"),
                ],
                width=12,
            ),
        ),

        dcc.Loading(
            id="loading-2",
            children=[html.Div(id="output_tweets")],
            type="default",
        )



    ],

)


@app.callback(
    [Output('output_keywords', 'children')],
    [Input('input_key_button', 'n_clicks')],
    [State('input_keyword', 'value')]
)
def submit(n_clicks, input_value):

    if(n_clicks == 0):
        return [""]
    tags = get_tags(input_value)
    # print("home")
    # print(df_tweet_working.shape)

    global df_tweet_home

    df_tweet_working = df_tweet[df_tweet['id'].isin(
        tweetsIdsByTopic[predictTopic(input_value)])]

    df_tweet_home = df_tweet_working.copy()

    with open('./data/working_data.jsonl', 'w') as f:
        pass
    df_tweet_working.to_json('./data/working_data.jsonl',
                             orient="records", lines=True)

    return [[(html.Span(tag, className="badge badge-"+get_random_element(), style={"font-size": "13pt", "margin": "10px 5px 0 0"})) for tag in tags]]


@app.callback(
    [Output('output_tweets', 'children')],
    [Input('input_key_button', 'n_clicks')],

)
def submit(n_clicks):
    if(n_clicks == 0):
        return [""]

    nb_tweets = 6

    # if not os.path.exists("./data/working_data.jsonl"):
    #     return ['']

    # df_tweet_working = pd.read_json("./data/working_data.jsonl",
    #                                 orient='records', lines=True)

    sample_tweets = df_tweet_home.sort_values(
        by=['created_at'], ascending=False).iloc[0:nb_tweets, :]
    sample_tweets.reset_index(inplace=True)
    index = 0
    all_tweets = []
    all_tweets.append(dbc.Row(
        html.H4("Latest tweets", className="mx-auto",
                style={"margin-top": "40px"})
    ))
    for i in range(int(nb_tweets/3)):
        row_tweet = []
        for j in range(3):
            col = dbc.Col(
                html.Div(
                    html.Div(
                        html.Blockquote(
                            [
                                html.A(href="https://twitter.com/"+sample_tweets.iloc[index, :]['user']['screen_name']+"/status/"+str(sample_tweets.iloc[index, :]['id']))],

                            className="twitter-tweet"
                        )
                    ),
                ),
            )
            row_tweet.append(col)

            index += 1

        all_tweets.append(dbc.Row(row_tweet))
        all_tweets.append(dji.Import(
            src="https://platform.twitter.com/widgets.js")
        )
    time.sleep(5)
    return [dbc.Container(all_tweets)]
    # print(tags)
    # return [dbc.Row(
    #     [
    #         dbc.Col(
    #             html.Div(
    #                 html.Div(
    #                     html.Blockquote(
    #                         ["Recapping some of the 💯 Tweets from the past week.</p>&mdash; Twitter (@Twitter)",
    #                          html.A("16 décembre 2017", href="https://twitter.com/yogitabhayana/status/1385241049505812481")],

    #                         className="twitter-tweet"
    #                     )
    #                 ),
    #             ),
    #         ),
    #         dbc.Col(
    #             html.Div(
    #                 html.Div(
    #                     html.Blockquote(
    #                         ["Recapping some of the 💯 Tweets from the past week.</p>&mdash; Twitter (@Twitter)",
    #                          html.A("16 décembre 2017", href="https://twitter.com/yogitabhayana/status/1385241049505812481")],

    #                         className="twitter-tweet"
    #                     )
    #                 ),
    #             ),
    #         ),
    #         dbc.Col(
    #             html.Div(
    #                 html.Div(
    #                     html.Blockquote(
    #                         ["Recapping some of the 💯 Tweets from the past week.</p>&mdash; Twitter (@Twitter)",
    #                          html.A("16 décembre 2017", href="https://twitter.com/yogitabhayana/status/1385241049505812481")],

    #                         className="twitter-tweet"
    #                     )
    #                 )
    #             ),
    #         ),
    #         dji.Import(src="https://platform.twitter.com/widgets.js")
    #     ],
    #     style={
    #         "height": "500px",
    #         "overflow-y": "scroll"
    #     }
    # ),

    # ]
