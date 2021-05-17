from functions.NLP import preprocess, tokenize_lowercase
import pandas as pd
import secrets
import os
from app import df_tweet


def get_tags(text):
    return preprocess(text)


def get_random_element(liste_element=["primary", "secondary", "success", 'danger', "info", "warning", 'dark']):
    return secrets.choice(liste_element)


def read_workingDf():
    if not os.path.exists("../data/working_data.jsonl"):
        return df_tweet

    df_tweet_working = pd.read_json("../data/working_data.jsonl",
                                    orient='records', lines=True)
    return df_tweet_working
