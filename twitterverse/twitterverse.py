import os
import shutil
import tweepy
import json
import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def readSettings():

    import yaml

    with open('settings.yaml', 'r') as stream:
        all_settings = yaml.safe_load(stream)

    connection_settings = all_settings['Connection Settings']
    program_settings = all_settings['Program Settings']
    twitter_settings = all_settings['Twitter Settings']
    output_settings = all_settings['Output Settings']

    full_parameters = (connection_settings,
                        program_settings,
                        twitter_settings,
                        output_settings)

    return full_parameters

def establishAuthAPI(connection_settings):

    auth = tweepy.AppAuthHandler(connection_settings['api key'], connection_settings['api secret key'])
    api = tweepy.API(auth)

    return auth, api

def makeResultsDirectory():

    if not os.path.exists('tweets'):
        os.mkdir('tweets')

def fetchRecentTweets(api, twitter_settings):

    tweets = tweepy.Cursor(api.user_timeline,
                            id = twitter_settings['user id'],
                            trim_user = twitter_settings['trim user'],
                            exclude_replies = twitter_settings['exclude replies'],
                            include_rts = twitter_settings['include rts'],
                            tweet_mode = 'extended').items(twitter_settings['nitems'])

    return tweets

def giveTweetsAsDictionary(the_tweets, user_id, save_tweets = False):

    tweets_dict = {'tweet_{}'.format(str(index)): the_tweet._json for index, the_tweet in enumerate(the_tweets)}

    if save_tweets:

        with open('tweets/' + user_id + '.json', 'w') as f:
            json.dump(tweets_dict, f, indent = 4)

    return tweets_dict

# ------------------------------------------------------------------------------

def main():

    (connection_settings,
    program_settings,
    twitter_settings,
    output_settings) = readSettings()

    user_id = twitter_settings['user id']

    if program_settings['fetch tweets']:

        auth, api = establishAuthAPI(connection_settings)
        tweets = fetchRecentTweets(api, twitter_settings)

        makeResultsDirectory()
        tweets = giveTweetsAsDictionary(tweets, user_id, save_tweets = True)

    else:

        with open('tweets/' + user_id + '.json', 'r') as f:
            tweets = json.load(f)

    

if __name__ == '__main__':
    main()
