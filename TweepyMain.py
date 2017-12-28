import tweepy
import random

# Constants with the auth and consumer keys
CONSUMER_KEY=''
CONSUMER_SECRET=''
OAUTH_TOKEN=''
OAUTH_TOKEN_SECRET=''

#Creates a new Auth to Twitter API
auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

#Sets the tokens for the api access
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

#Creates a new API with the auth
api=tweepy.API(auth)

# Gets all the tweets from the user
#public_tweets=api.home_timeline()

#for tweet in public tweets:
 #   tweet.destroy()
   # print(tweet.text)

#api.retweet(666)