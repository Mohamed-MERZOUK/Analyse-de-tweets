import dash
import pandas as pd
import numpy as np
import os
import sys
import inspect
import pickle
import gzip
import nltk
from geopy.geocoders import Nominatim
# import pyLDAvis
# import pyLDAvis.gensim_models as gensimvis

tweetsIdsByTopic = pickle.load(open('./data/tweetsIdsByTopic.npy', 'rb'))
dictionnary = pickle.load(open('./data/lda_dictionary.sav', 'rb'))
lda_model = pickle.load(open('./models/lda_model.sav', 'rb'))


# TODO remove comment
# nltk.download('movie_reviews')
# nltk.download('punkt')


geolocator = Nominatim(user_agent='http://127.0.0.1:8888/')

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4',
        'crossorigin': 'anonymous'
    },
    {
        'href': 'https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/fonts/simple-line-icons/style.min.css',
        'rel': 'stylesheet',
        'type': 'text/css',

    },
    {
        'href': 'https://fonts.gstatic.com',
        'rel': 'preconnect'
    },
    {
        'href': 'https://fonts.googleapis.com/css2?family=Noto+Serif:wght@700&display=swap',
        'rel': 'stylesheet'
    }

]

external_scripts = [

    {
        'src': 'https://platform.twitter.com/widgets.js',

        'charset': 'utf-8'
    },
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/solid.js',
        'integrity': 'sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js',
        'integrity': 'sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
        'integrity': 'sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js',
        'integrity': 'sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm',
        'crossorigin': 'anonymous'
    },
    {
        "src": "https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.concat.min.js"
    }

]

df_tweet = pd.read_json("./data/covid-tweets-sample.jsonl",
                        orient='records', lines=True)

if(os.path.isfile('./data/working_data.jsonl')):
    print("hello word")
    df_tweet_working = pd.read_json("./data/working_data.jsonl",
                                    orient='records', lines=True)
else:
    df_tweet_working = df_tweet.copy()

# df_tweet = df_tweet[df_tweet['id'].isin(tweetsIdsByTopic[0])]
# print(df_tweet.shape)
app = dash.Dash(__name__, external_scripts=external_scripts,
                external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
