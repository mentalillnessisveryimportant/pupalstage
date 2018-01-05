import tweepy
import random
import time

from builtins import str
from tweepy import TweepError

FILE_KEYS="keys.txt"
TWEEPY_NO_STATUS_ERROR_CODE=144
TWEEPY_PRIVATE_STATUS_ERROR_CODE=179
TWEEPY_TOO_MANY_REQUESTS_ERROR_CODE=420
# file must contain keys by order and finish with a \n(enter)
file = open(FILE_KEYS,"r")

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


# Replies to a certain tweet with a certain status ID with a certain content message
def reply(status_id,current_api,content):
    """
    Replies to a certain tweet with a certain statud ID with a certain content message
    :param status_id: Integer with the status ID
    :param current_api: API being used
    :param content: String with the content being replied
    :return: boolean true if reply was successful, false if not
    """
    try:
        current_api.update_status(content,in_reply_to_status_id=status_id)
        return True
    except tweepy.TweepError as e:
        return False


# Replies to a certain tweet with a certain status ID with a certain content message
def reply_integer(status_id,current_api,content):
    """
    Replies to a certain tweet with a certain statud ID with a certain content message
    :param status_id: Integer with the status ID
    :param current_api: API being used
    :param content: String with the content being replied
    :return: Integer 5 if reply was succesful, or Twitter error code with the error code
    """
    try:
        current_api.update_status(content,in_reply_to_status_id=status_id)
        return 5
    except tweepy.TweepError as e:
        return e.api_code


# Checks if a certain status ID is valid or not
def is_status_id_valid(status_id, current_api):
        """
        Checks if a certain status ID is valid or not
        :param status_id: Integer with the status_id
        :param current_api: API being used
        :return: boolean true if valid, false if not
        """
        try:
            current_api.get_status(status_id)
            return True
        except tweepy.TweepError as e:
            return False


# Checks if a certain status ID is valid or not
def is_status_id_valid_integer(status_id,current_api):
    """
    Checks if a certain status ID is valid or not
    :param status_id: Integer with the status_id
    :param current_api: API being used
    :return: Integer 5 if valid, else Error code with the Twitter Error
    """
    try:
        current_api.get_status(status_id)
        return 5
    except tweepy.TweepError as e:
        return e.api_code


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

#https://www.youtube.com/watch?v=6tlDSVCaWcc
#def spamTweetsInRegion(accounts,content,used_ids,low_region,high_region):
    #while(True):
     #   MAX_ACCOUNTS=accounts.__sizeof__()
    #    used_accounts=0
    #    for i in range(0,MAX_ACCOUNTS):
       #     while(low_region<=high_region):
         #       if not used_ids.__contains__(low_region):
         #           valid_status=is_status_id_valid_integer(low_region,accounts[i])
           #         if valid_status == 5:
            #            used_accounts=0
           #             reply=reply_integer(low_region,accounts[i],content)
         #               if reply == 5:
        #                    used_accounts=0
         #                   used_ids.add(low_region)
        #                    low_region+=1
        #                else:
        #                    if reply==TWEEPY_TOO_MANY_REQUESTS_ERROR_CODE:
        #                        used_accounts+=1
         #                       i+=1
#
          #                  used_ids.add(low_region)
          #                  low_region+=1
          #          else:
          #              if valid_status==TWEEPY_TOO_MANY_REQUESTS_ERROR_CODE:
          #                  used_accounts+=1
          #                  i+=1
          #              used_ids.add(low_region)
         #               low_region+=1
      #          else:
     #               used_ids.add(low_region)
     #               low_region+=1
     #           if(used_accounts==MAX_ACCOUNTS):
      #              time.sleep(5)
