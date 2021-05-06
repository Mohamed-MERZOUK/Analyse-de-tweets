# from app import LDA_model
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS
from nltk.probability import FreqDist
import pandas as pd
import plotly.express as px
from functions.NLP import preprocess
from app import geolocator
import dash_leaflet as dl
import dash_leaflet.express as dlx
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

# def LDA_plot():
#     vis = gensimvis.prepare(lda_model_tfidf, bow_corpus, dictionary=lda_model_tfidf.id2word)
#     return vis


def timeseriesCount(df_tweet):
    df = df_tweet.copy()
    df_time = df.groupby(pd.Grouper(key="created_at",
                                    freq="1D")).count().reset_index()
    df_time = df_time.rename(columns={'favorite_count': 'sum'})

    fig = px.line(df_time, x='created_at', y="sum")
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


def wordCloud(df):

    df_t = df['full_text'].copy()

    df_t = df_t.apply(preprocess)
    all_words = [
        word for tokens in df_t for word in tokens if word != "coronavirus"]

    text = " ".join(all_words)

    wc = WordCloud(stopwords=set(STOPWORDS),
                   max_words=30,
                   max_font_size=100)
    wc.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x = []
    y = []
    for i in position_list:
        x.append(i[0])
        y.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list

    trace = go.Scatter(x=x,
                       y=y,
                       textfont=dict(size=new_freq_list,
                                     color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(
                           w, f) for w, f in zip(word_list, freq_list)],
                       mode="text",
                       text=word_list
                       )

    layout = go.Layout(
        xaxis=dict(showgrid=False,
                   showticklabels=False,
                   zeroline=False,
                   automargin=True),
        yaxis=dict(showgrid=False,
                   showticklabels=False,
                   zeroline=False,
                   automargin=True)
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def treeMap(df_input):
    df = df_input.copy()
    df['full_text'] = df.full_text.apply(preprocess)

    all_words = [word for tokens in df['full_text'] for word in tokens]

    word_freq = FreqDist(all_words)

    most_common_count = [x[1] for x in word_freq.most_common(30)]
    most_common_word = [x[0] for x in word_freq.most_common(30)]

    most_common_word.pop(0)
    most_common_count.pop(0)

    dict_word_count = {'word': most_common_word, 'count': most_common_count}

    new_df = pd.DataFrame(dict_word_count)

    fig = px.treemap(new_df, path=['word'], values='count',
                     hover_data=['count'], color="count",
                     color_continuous_scale='tempo'
                     )
    fig.layout.paper_bgcolor = '#fafafa'
    return fig


def word_freq_tweet(df):
    my_df = df.copy()
    my_df['full_text'] = my_df.full_text.apply(preprocess)
    all_words = [word for tokens in my_df['full_text'] for word in tokens]

    tweet_lengths = [len(tokens) for tokens in my_df['full_text']]

    df = pd.DataFrame(tweet_lengths, columns=["length"])
    df["count"] = 1
    df_count = df.groupby(['length'], as_index=False).count()

    fig = px.bar(df_count, x='length', y='count', labels={
                 'count': 'Number of Tweets', 'length': 'Words per Tweet'})

    fig.update_layout(
        xaxis=dict(
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
            showgrid=True,
            linecolor='black',
            zeroline=False,
            showline=False,
            gridcolor="rgb(82,82,82)",
        ),
        showlegend=False,
        plot_bgcolor='#fafafa'
    )
    fig.layout.paper_bgcolor = '#fafafa'
    fig.update_traces(marker_color='#456987')

    return fig


def simple_map(df, nb_makers):
    postions = []
    for tweet in df.iloc[0:nb_makers, :].iterrows():
        try:
            if tweet[1]['user']['location']:
                coordinate = geolocator.geocode(tweet[1]['user']['location'])
                if(not coordinate):
                    continue

                postions.append(dl.Marker(position=(
                    coordinate.latitude, coordinate.longitude), children=dl.Tooltip("{}".format(tweet[1]['full_text']))))

        except Exception as e:
            print("Http error : " + e)
            continue

    return postions


def cluster_map(df, nb_makers):
    postions = []
    for tweet in df.iloc[0:nb_makers, :].iterrows():
        try:
            if tweet[1]['user']['location']:
                coordinate = geolocator.geocode(tweet[1]['user']['location'])
                if(not coordinate):
                    continue

                postions.append(dict(lat=coordinate.latitude,
                                lon=coordinate.longitude))

        except Exception as e:
            print("Http error")
            continue

    return postions
