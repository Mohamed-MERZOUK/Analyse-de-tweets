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

# def LDA_plot():
#     vis = gensimvis.prepare(lda_model_tfidf, bow_corpus, dictionary=lda_model_tfidf.id2word)
#     return vis


def wordCloud(df):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    all_words = [word for tokens in df['full_text'] for word in tokens]
    print(len(all_words))
    # word_freq = FreqDist(all_words)

    # most_common_count = [x[1] for x in word_freq.most_common(30)]
    # most_common_word = [x[0] for x in word_freq.most_common(30)]

    # #create dictionary mapping of word count
    # top_30_dictionary = dict(zip(most_common_word, most_common_count))

    alice_mask = np.array(Image.open(
        path.join(d, ".\\assets\\alice_mask.png")))

    stopwords = set(STOPWORDS)

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
                   stopwords=stopwords, contour_width=3, contour_color='steelblue')

    # generate word cloud
    wc.generate(" ".join(["all word", "zzzz", "aaa", "bbbbbb"]))

    # store to file
    wc.to_file(path.join(d, ".\\assets\\alice.png"))

    # show
    # plt.imshow(wc, interpolation='bilinear')
    # plt.axis("off")
    # plt.figure()
    # plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()

    return ".\\assets\\alice.png"


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

    return fig


def simple_map(df, nb_makers):
    postions = []
    for tweet in df.iloc[0:, :nb_makers].iterrows():
        try:
            if tweet[1]['user']['location']:
                coordinate = geolocator.geocode(tweet[1]['user']['location'])
                if(not coordinate):
                    continue

                postions.append(dl.Marker(position=(
                    coordinate.latitude, coordinate.longitude), title=tweet[1]['full_text']))
        except KeyError:
            continue
    return postions
