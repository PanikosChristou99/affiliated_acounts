import tweepy
import codecs
from Twitter_crawler import twitter_credentials

import pandas as pd

# Authenticate to Twitter
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

query = ['@HillaryClinton', "HillaryClinton"]
max_tweets = 4
for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
    print(f"https://twitter.com/{status.user.screen_name}/status/{status.id}")
