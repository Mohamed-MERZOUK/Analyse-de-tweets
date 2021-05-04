# from app import LDA_model
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS


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

    alice_mask = np.array(Image.open(path.join(d, ".\\assets\\alice_mask.png")))

    stopwords = set(STOPWORDS)

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
                stopwords=stopwords, contour_width=3, contour_color='steelblue')

    # generate word cloud
    wc.generate(" ".join(["all word","zzzz","aaa"]))

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