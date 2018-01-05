import tweepy
import random
import time
from multiprocessing import Process
import threading
import queue
from builtins import str
from tweepy import TweepError

# Function that gets all available Twitter API accounts under a certain file name
def get_available_accounts(file_name):
    """
    Function that gets all available Twitter API accounts under a certain file name
    <br>File must follow the same structure as the file that has the OATH keys and tokens for the login
    :param file_name: String with the file name that contains all OAUTH keys and tokens of the accounts
    :return: Array with all the Tweepy API of the accounts
    """
    accounts=[]
    keys=['null']*4
    fileInfo=open(file_name, 'r')
    tokens=0
    for line in fileInfo:
        keys[tokens]=line[0:-1]
        tokens+=1
        if tokens==4:
            tokens=0
            authX=tweepy.OAuthHandler(keys[0],keys[1])
            authX.set_access_token(keys[2],keys[3])
            accounts.append(tweepy.API(authX))
    fileInfo.close()
    return accounts


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
def findLatestTweetByWord(str,api):
    """
    Finds the latest tweet that contains a certain word or sequence of words
    :param str: String with the word/sequence of words being found
    :return: Integer with the tweet ID that contains the word/sequence of words or -1 if not found
    """
    return api.search(str).since_id;

# Posts a tweet
def post(str,api):
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
def retweet(status_id,api):
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

# Gets an array with all trends occurring on a certain WOEID
def get_trends_woeid(id):
    """
    Gets an array with all trends occurring on a certain WOEID (Yahoo GEO ID)
    :param id: Integer with the WOEID (Yahoo GEO ID) of the place
    :return: Array with all trends occurring on the place or None if an error occurred or no trends found
    """
    try:
        trends_json=api.trends_place(id)
        trends=(trends_json[0])['trends']
        return [trend['name'] for trend in trends]
    except tweepy.TweepError:
        return None

# Gets the location and woeid from a certain Twitter Trends JSON
def get_location_and_woeid_json(json):
    """
    Gets the location and woeid from a certain Twitter Trends JSON
    :param json: JSON with the Twitter trend JSON object
    :return: Array with the location and woeid of the trend location
    """
    array=[]
    replaced_splitted_json=replace_string(json.get('locations').__str__(),{'{','}','[',']',':','\'',','}).split(" ")
    array.append(replaced_splitted_json[1])
    array.append(replaced_splitted_json[3])
    return array


# Replaces all characters/Strings in a certain String
def replace_string(str, array):
    """
    Replaces all characters/Strings in a certain String
    :param str: String being replaced
    :param array: Array with all characters/Strings being replaced
    :return: String with all replaced characters/Strings by an empty String ("")
    """
    new_str=str.__str__()
    EMPTY_STRING=""
    for sequence in array:
        new_str=new_str.replace(sequence,EMPTY_STRING)
    return new_str

def get_tweets_text(low,high,api):
    """
    Gets tweets in order from low to high or "low" ammount of random tweets
    :param low: defines the starting number
    :param top: if False will give random tweets
    :param api: The tweepy api
    :return:
    """
    if high:
        tweets_ids=range(low,high)
    else:
        tweets_ids=[]
        for i in range(0,low):
            tweets_ids.append(random.randint(0,10**10))

    tweets_text=[]
    for i in tweets_ids:
        while True:
            try:
                tweets_text.append(api.get_status(i).text)
                break
            except:
                tweets_text.append("ERROR GUETING TWEET")
                break
    return tweets_text


users = get_available_accounts("KEYS_TEMPLATE.txt")

#print(users[0].get_status(findLatestTweetByWord("sup",users[0])).text)# searches for tweets withs the word
n_tweets=10
n_threads=10
tempo=time.time()
memory=[]
# memory=get_tweets_text(n_tweets,False,users[0])
que= queue.Queue()
n_tweets_multi=int(n_tweets/n_threads)
threads=[]
for i in range(n_threads):
    #thread = threading.Thread(target=get_tweets_text,args=(n_tweets_multi,False,users[0]))

    thread = threading.Thread( target = lambda q, arg1,arg2,arg3: q.put(get_tweets_text(arg1,arg2,arg3)), args=(que,n_tweets_multi, False, users[0]))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

while not que.empty():
    memory.append(que.get())

print("It took {}s to get {} tweets".format(time.time()-tempo,n_tweets))
for i in range(len(memory)):
    print(memory[i][0])