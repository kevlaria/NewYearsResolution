from twitter import *
from twitter import TwitterStream
import csv

"""
Helper module to connect to Twitter
"""


def get_twitter_stream():
    """
    None -> TwitterStream
    Get a TwitterStream object (for real time search)
    """
    credentials = get_credentials()
    OAUTH_TOKEN = credentials[0]
    OAUTH_SECRET = credentials[1]
    CONSUMER_KEY = credentials[2]
    CONSUMER_SECRET = credentials[3]
    twitter_stream = TwitterStream(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    return twitter_stream

def get_twitter():
    """
    Get a Twitter object (for historical searches etc)
    """
    credentials = get_credentials()
    OAUTH_TOKEN = credentials[0]
    OAUTH_SECRET = credentials[1]
    CONSUMER_KEY = credentials[2]
    CONSUMER_SECRET = credentials[3]
    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    return t


def get_credentials():
    """
    Extracts Twitter credenitals from a TSV credentials file. Credentials file must be in the format: 
    oauth_token\t<token>
    oauth_secret\t<secret>
    consumer_key\t<key>
    consuemr_secret\t<consumer_secret>
    """
    credentials_file = open('credentials.properties', 'r')
    csv_reader = csv.reader(credentials_file, delimiter='\t')
    contents = []
    for item in csv_reader:
        contents.append(item)
    OAUTH_TOKEN = contents[0][1]
    OAUTH_SECRET = contents[1][1]
    CONSUMER_KEY = contents[2][1]
    CONSUMER_SECRET = contents[3][1]
    credentials_file.close()
    return (OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)



