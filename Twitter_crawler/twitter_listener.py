import time
from Twitter_crawler import twitter_credentials
import tweepy
import dataset

db = dataset.connect("sqlite:///tweets.db")
# override tweepy.StreamListener to add logic to on_status


# Attributes
# description = status.user.description
# loc = status.user.location
# text = status.text
# coords = status.coordinates
# name = status.user.screen_name
# user_created = status.user.created_at
# followers = status.user.followers_count
# id_str = status.id_str
# created = status.created_at
# retweets = status.retweet_count
# bg_color = status.user.profile_background_color
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open('data.json', 'a')
        super(MyStreamListener, self).__init__()

    def on_status(self, data):
        if (time.time() - self.start_time) < self.limit:
            self.saveFile.write(data)
            self.saveFile.write('\n')
            return True
        else:
            self.saveFile.close()
            return False

    def on_error(self, status_code):
        print("error")
        return False


with tweepy.Stream(auth=auth, listener=MyStreamListener(time_limit=5)) as myStream:
    # In this example we will use filter to stream all tweets containing the word python. The track parameter is an
    # array of search terms to stream.
    myStream.filter(track=['python'])
    # filter to stream tweets by a specific user.
    # This example shows how to use filter to stream tweets by a specific user. The follow parameter is an array of IDs.
    myStream.filter(follow=["2211149702"], is_async=True)

# Streams do not terminate unless the connection is closed, blocking the thread.
# Tweepy offers a convenient is_async parameter on filter so the stream will run on a new thread. For example
