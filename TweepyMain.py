import tweepy
import random

from tweepy import TweepError

print(sys.version)
print(" ")
# file must contain keys by order and finish with a \n(enter)
file = open("chave.txt","r")

key=['null']*4
i=0
for line in file:
    key[i]=line[0:-1]
    i+=1
file.close()

#Creates a new Auth to Twitter API
auth = tweepy.OAuthHandler(key[0], key[1])

#Sets the tokens for the api access
auth.set_access_token(key[2], key[3])

#Creates a new API with the auth
api = tweepy.API(auth)


# Gets all the tweets from the user
#public_tweets=api.home_timeline()

#for tweet in public tweets:
 #   tweet.destroy()
   # print(tweet.text)

#api.retweet(666)

#escreve os tweets dentro da range e da skip aos que nao exitem ou sao privados
#tb procura pela palavra have !
word='have'
contador=0
for i in range (2000,2005):
    while True:
        try:
            var=api.get_status(i).text
            print(var)
            if word in var:
                contador += 1
            break
        except:
            print("----------Oops!------------ ")
            break



print("\nforam encontados {} {}".format(contador,word))

# Function that finds a certain tweet that contains a certain word
def findTweetByWord(str):
    """
    Function that finds a certain tweet that contains a certain word
    :param str: String with the that the tweet must contain
    :return: Integer with the tweet ID
    """
    catched=True
    while(catched):
        next_status=random.randint(0,9999999999)
        try:
            text=api.get_status(next_status).text
            if(str in text):
                catched=False
                return next_status
        except tweepy.TweepError:
            print("ID: ",next_status," unavailable")