import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from functions.Utils import get_tags,get_random_element
from app import app
from dash.dependencies import Input, Output, State
from base64 import urlsafe_b64encode
import dash_defer_js_import as dji





layout = dbc.Container(
    [

    dbc.Row(
        html.H1("Advenced Twitter Analyzer", style={ "margin-bottom":"30px" }, className="mx-auto")
    ),
    dbc.Row(
        dbc.Col(
            [
            dbc.Input(id="input_keyword", type="text", placeholder="", className="mb-10")
            ],
            width=12, 
        )
    ),
    dbc.Row(
        dbc.Col(
            [
            dbc.Button("Submitt",id="input_key_button",n_clicks=0, style={ "margin-top":"30px" }, className="btn btn-secondary btn-lg btn-block"),
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

    dbc.Row(
        html.H3("Latest tweets", className="mx-auto", style={"margin-top":"40px"})
    ),

    

    html.Div(id="output_tweets"),
     
   
    ],
    
)



@app.callback(
    [Output('output_keywords', 'children')],
    [Input('input_key_button', 'n_clicks')],
    [State('input_keyword', 'value')]
)
def submit(n_clicks, input_value):
    if(n_clicks==0):
        return [""]
    tags = get_tags(input_value)
    #print(tags)
    return  [[(html.Span(tag,className="badge badge-"+get_random_element(), style={"font-size":"15pt", "margin":"10px 5px 0 0"})) for tag in tags]]
        
    

    

@app.callback(
    [Output('output_tweets', 'children')],
    [Input('input_key_button', 'n_clicks')],
    
)
def submit(n_clicks):
    
    #print(tags)
    return  [dbc.Row(
        [
        dbc.Col(
            html.Div(
                html.Div(
                    html.Blockquote(
                    ["Recapping some of the 💯 Tweets from the past week.</p>&mdash; Twitter (@Twitter)",
                    html.A("16 décembre 2017",href="https://twitter.com/yogitabhayana/status/1385241049505812481")],

                    className="twitter-tweet"
                    )
                ),
            ),
        ),
        dbc.Col(
            html.Div(
                html.Div(
                    html.Blockquote(
                    ["Recapping some of the 💯 Tweets from the past week.</p>&mdash; Twitter (@Twitter)",
                    html.A("16 décembre 2017",href="https://twitter.com/yogitabhayana/status/1385241049505812481")],

                    className="twitter-tweet"
                    )
                ),
            ),
        ),
        dbc.Col(
            html.Div(
                html.Div(
                    html.Blockquote(
                    ["Recapping some of the 💯 Tweets from the past week.</p>&mdash; Twitter (@Twitter)",
                    html.A("16 décembre 2017",href="https://twitter.com/yogitabhayana/status/1385241049505812481")],

                    className="twitter-tweet"
                    )
                )
            ),
        ),
          dji.Import(src="https://platform.twitter.com/widgets.js")
        ],
        style={
            "height" : "500px",
            "overflow-y" : "scroll"
        }
    ),
   
    
    ]
        
    

    
