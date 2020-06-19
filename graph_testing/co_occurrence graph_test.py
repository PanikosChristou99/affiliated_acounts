import networkx as nx
import tweepy
from Twitter_crawler import twitter_credentials
import re
import matplotlib.pyplot as plt

regex_mention = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)')

# # /^             //start of the string
# # (?!.*\bRT\b)   //Verify that rt is not in the string.
# # (?:.*\s)?      //Find optional chars and whitespace the
# #                   //Note: (?: ) makes the group non-capturing.
# # @\w+           //Find @ followed by one or more word chars.
# # /i             //Make it case insensitive.
G = nx.Graph()

auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)
name_of_original_target = "@HillaryClinton"

query = ['@HillaryClinton OR Hillary Clinton']
max_tweets = 50
search_results = api.search(q=query, count=max_tweets)
for tweet in search_results:
    if (not tweet.retweeted) and ('RT @' not in tweet.text):
        print("---------------------------------")
        print(f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}")
        print("tweet text:")
        print(tweet.text)
        print("found:")
        for match in re.finditer(regex_mention, tweet.text):
            s = match.start()
            e = match.end()
            found = tweet.text[s:e]
            print(found)
            if G.has_edge(name_of_original_target, tweet.text[s:e]):
                G.add_edge(name_of_original_target, tweet.text[s:e],
                           weight=G[name_of_original_target][tweet.text[s:e]]['weight'] + 1)
            else:
                G.add_edge(name_of_original_target, tweet.text[s:e], weight=1)
        print("---------------------------------")
#
# # labels
#
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw(G,pos)
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
# plt.axis('off')
# plt.savefig("weighted_graph.png") # save as png
# plt.show() # display
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw_networkx_labels(G, pos, font_size=9, font_family='sans-serif')
nx.draw(G, pos)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
