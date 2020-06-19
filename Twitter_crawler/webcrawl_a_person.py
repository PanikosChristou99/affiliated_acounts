import tweepy
import codecs
from Twitter_crawler import twitter_credentials

import pandas as pd

# Authenticate to Twitter
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)


def webcrawl_person(name, depth, num_of_tweets):  # depth not implemente dyet
    with codecs.open(name + "_tweet_texts.txt", 'w', encoding='utf8') as f:
        # this webcrawls a user  and all its mentions in the depth specified and maps user mentions
        for tweet in tweepy.Cursor(api.user_timeline, id=name).items(num_of_tweets):
            f.write(tweet.text + "\n")


webcrawl_person("HillaryClinton", 1, 3)
