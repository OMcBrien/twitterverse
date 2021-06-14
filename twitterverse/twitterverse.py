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
    twitter_settings = all_settings['Twitter Settings']
    output_settings = all_settings['Output Settings']

    full_parameters = (connection_settings,
                        twitter_settings,
                        output_settings)

    return full_parameters

def establishAuthAPI(connection_settings):

    auth = tweepy.AppAuthHandler(connection_settings['api key'], connection_settings['api secret key'])
    api = tweepy.API(auth)

    return auth, api

def makeResultsDirectories(sub_dir):

    if not os.path.exists('output'):
        os.mkdir('output')

    user_output_directory = os.path.join('output', sub_dir)

    if not os.path.exists(user_output_directory):
        os.mkdir(user_output_directory)
    elif os.path.exists(user_output_directory):
        shutil.rmtree(user_output_directory)
        os.mkdir(user_output_directory)

def fetchRecentTweets(api, twitter_settings):

    tweets = tweepy.Cursor(api.user_timeline,
                            id = twitter_settings['user id'],
                            trim_user = twitter_settings['trim user'],
                            exclude_replies = twitter_settings['exclude replies'],
                            include_rts = twitter_settings['include rts'],
                            tweet_mode = 'extended').items(twitter_settings['nitems'])

    return tweets

def saveTweets(the_tweets, user_id, save_over = False):

    tweet_out_dir = os.path.join('output/' + user_id)

    for the_tweet in the_tweets:

        the_tweet = json.loads( json.dumps(the_tweet._json) )

        with open(os.path.join(tweet_out_dir, the_tweet['id_str'] + '.tweet'), 'w') as filewrite:
            json.dump(the_tweet, filewrite, indent = 4)

# ------------------------------------------------------------------------------

def main():

    (connection_settings,
     twitter_settings,
     output_settings) = readSettings()

    auth, api = establishAuthAPI(connection_settings)

    tweets = fetchRecentTweets(api, twitter_settings)

    if output_settings['save results']:
        makeResultsDirectories(twitter_settings['user id'])
        saveTweets(tweets, twitter_settings['user id'], save_over = True)




if __name__ == '__main__':
    main()
