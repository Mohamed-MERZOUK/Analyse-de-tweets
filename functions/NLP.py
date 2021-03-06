
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import pandas as pd
from textblob.sentiments import NaiveBayesAnalyzer
import string
from app import dictionnary, lda_model


def remove_urls(text):
    result = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', ' ', text)
    return result


stop_words = stopwords.words('english')
# add punctuation char's to stopwords list
# <-- contains !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
stop_words += list(string.punctuation)
# add integers
stop_words += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def tokenize_lowercase(text):
    tokens = nltk.word_tokenize(text)
    stopwords_removed = [token.lower()
                         for token in tokens if token.lower() not in stop_words]
    return stopwords_removed


def remove_nums(text_object):
    no_nums = list(filter(lambda x: x.isalpha(), text_object))
    return no_nums


lemmatizer = WordNetLemmatizer()


def lemmatize_text(df_text):
    lemmatized = []
    for w in df_text:
        if(len(w) > 3):
            lemmatized.append(lemmatizer.lemmatize(w))

    return lemmatized


def list_to_sentence(list_words):
    return " ".join(list_words)


def preprocess(text):
    return lemmatize_text(remove_nums(tokenize_lowercase(remove_urls(text))))


def sentimentAnalyser(text):
    blob_object = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    analysis = blob_object.sentiment
    return analysis.classification


def sentimentStats(df):
    df.full_text.map(sentimentAnalyser)


def predictTopic(text):
    bow_vector = dictionnary.doc2bow(preprocess(text))
    topics = sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1])
    return topics[0][0]
