from collections import Counter, defaultdict
import re
import numpy as np 
import requests
import json


def get_hashtags(tweet):
    entities = tweet[4]
    hashtags = entities.get('hashtags', [])
    return [tag['text'].lower() for tag in hashtags]


def get_mentions(tweet):
    entities = tweet[4]
    hashtags = entities.get('user_mentions', [])
    return [tag['screen_name'] for tag in hashtags]


def hachtags_numbers(tweets):

    hashtag_count = defaultdict(int)
    for tweet in tweets:
        hashtags_in_tweet = get_hashtags(tweet)
        n_of_hashtags = len(hashtags_in_tweet)
        hashtag_count[n_of_hashtags] += 1

    tweets_with_hashtags = sum([count for n_of_tags, count in hashtag_count.items() if n_of_tags > 0])
    tweets_no_hashtags = hashtag_count[0]
    tweets_total = tweets_no_hashtags + tweets_with_hashtags
    tweets_with_hashtags_percent = "%d" % (tweets_with_hashtags / tweets_total * 100)
    tweets_no_hashtags_percent = "%d" % (tweets_no_hashtags / tweets_total * 100)

    for tag_count, tweet_count in hashtag_count.items():
        if tag_count > 0:
            percent_total = "%.2f" % (tweet_count / tweets_total * 100)
            percent_elite = "%.2f" % (tweet_count / tweets_with_hashtags * 100)

    return [(tweets_no_hashtags, tweets_no_hashtags_percent),(tweets_with_hashtags, tweets_with_hashtags_percent)]


def mentions_numbers(tweets):

    mention_count = defaultdict(int)
    for tweet in tweets:
        hashtags_in_tweet = get_mentions(tweet)
        n_of_hashtags = len(hashtags_in_tweet)
        mention_count[n_of_hashtags] += 1

    tweets_with_mentions = sum([count for n_of_tags, count in mention_count.items() if n_of_tags > 0])
    tweets_no_mentions = mention_count[0]
    tweets_total = tweets_no_mentions + tweets_with_mentions
    tweets_with_mentions_percent = "%d" % (tweets_with_mentions / tweets_total * 100)
    tweets_no_mentions_percent = "%d" % (tweets_no_mentions / tweets_total * 100)


    return [(tweets_no_mentions, tweets_no_mentions_percent),(tweets_with_mentions, tweets_with_mentions_percent)]





def getGenderCounts(df):
  gender = []
  for i in range(20):
    firstName = df.iloc[i,:]['user']['name'].split(" ")[0]
    firstName = re.sub('[^a-zA-Z]+', '', firstName)
    if firstName==" " or firstName==None or len(firstName)<=1 :
      gender.append(np.nan)
      continue
 
    # url = "https://api.genderize.io/?name=" + firstName;
    # x = requests.get(url)
    
    # res = json.loads(x.content.decode("ascii"))
    # gender.append(np.nan if res.get('gender') == None else res.get('gender'))
  
  #return { "male":gender.count("male"), "female":gender.count("female"), "nan":gender.count(np.nan) }
  return { "male":100, "female":200, "nan":30 }