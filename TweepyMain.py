import tweepy
import random
import time

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

# Function that finds a random tweet that contains a certain word
def findRandomTweetByWord(str):
    """
    Function that finds a certain tweet that contains a certain word
    :param str: String with the that the tweet must contain
    :return: Integer with the tweet ID or -1 if not found
    """
    catched=True
    MAX_REQUESTS=15
    requests=0
    while(catched and requests<MAX_REQUESTS):
        next_status=random.randint(0,api.search("\S").since_id)
        requests+=1
        try:
            text=api.get_status(next_status).text
            if(str in text):
                catched=False
                return next_status
        except tweepy.TweepError:
            print("ID: ",next_status," unavailable")

# Finds the latest tweet that contains a certain word or a sequence of words
def findLatestTweetByWord(str):
    """
    Finds the latest tweet that contains a certain word or sequence of words
    :param str: String with the word/sequence of words being found
    :return: Integer with the tweet ID that contains the word/sequence of words or -1 if not found
    """
    return api.search(str).since_id;

# Posts a tweet
def post(str):
    """
    Posts a tweet with a certain content
    :param str: String with the tweet content
    :return: Boolean true if the tweet was successful, false if not
    """
    try:
        api.update_status(str)
        return True
    except tweepy.TweepError:
        return False

# Retweets a certain tweet with a certain ID
def retweet(status_id):
    """
    Retweets a certain tweet with a certain ID
    :param status_id: Integer with the tweet ID being retweeted
    :return: Boolean true if the retweet was successful, false if not
    """
    try:
        api.retweet(status_id)
        return True
    except tweepy.TweepError:
        return False

def happy_new_year(str):
    try:
        HNW=" Happy New Year "
        AT="@"
        EXCLAMATION=" !"
        request=0
        REQUEST_LIMIT=20
        user=api.get_user(str)
        user_followers= get_all_followers(str)
        post(AT+user.screen_name+HNW+user.name+EXCLAMATION)
        for follower in user_followers:
            if request==REQUEST_LIMIT:
                request=0
                time.sleep(60)
            if not follower.protected:
                request+=1
                post(AT+follower.screen_name+HNW+follower.name+EXCLAMATION)
    except tweepy.TweepError:
        print("No Happy New Year :(")

# Gets all followers of a user
def get_all_followers(user):
    """
    Gets all followers of a certain user
    :param user: User @ that is going to get all followers
    :return: Array with all followers of the user, or None if a problem happened
    """
    try:
        followers=[]
        for page in tweepy.Cursor(api.followers,screen_name=user).pages():
            followers.extend(page)
            time.sleep(60)
        return followers
    except tweepy.TweepError:
        return None
