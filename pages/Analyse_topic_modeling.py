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
from functions.Plots import simple_map, treeMap, wordCloud, word_freq_tweet, cluster_map, timeseriesCount
import dash_leaflet as dl
import dash_leaflet.express as dlx
from app import app


layout = dbc.Container([
    dbc.Row(
        html.H3("LDA  advanced topic visualization", className="mx-auto"),
        style={"margin": "40px 0 0 0"}
    ),
    dbc.Row(
        dbc.Col(
            html.Iframe(src=app.get_asset_url('../assets/lda_topic_vis.html'),
                        style={"width": "100%", "height": "100vh", "position": "flex", "align-items": "center", "justify-content": "center", "flex-direction": "column", "border": "none"})
        )
    )



])
