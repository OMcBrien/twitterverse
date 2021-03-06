import os
import shutil
import tweepy
import json
import pandas as pd

def readSettings():

    import yaml

    with open('settings.yaml', 'r') as stream:
        all_settings = yaml.safe_load(stream)

    api_key = all_settings['api_key']
    api_secret_key = all_settings['api_secret_key']
    bearer_token = all_settings['bearer_token']
    fetch_properties = all_settings['fetch_properties']
    save_results = all_settings['save_results']

    user_id = fetch_properties['user_id']

    full_parameters = (api_key,
                        api_secret_key,
                        bearer_token,
                        fetch_properties,
                        save_results,
                        user_id)

    return full_parameters

def establishAuthAPI(api_key, api_secret_key):

    auth = tweepy.AppAuthHandler(api_key, api_secret_key)
    api = tweepy.API(auth)

    return auth, api

def makeMainOutputDirectory():

    if not os.path.exists('output'):
        os.mkdir('output')

def makeResultsDirectories(sub_dir):

    if not os.path.exists('output'):
        makeMainOutputDirectory()

    user_output_directory = os.path.join('output', sub_dir)

    if not os.path.exists(user_output_directory):
        os.mkdir(user_output_directory)
        os.mkdir(os.path.join(user_output_directory, 'tweets'))
    elif os.path.exists(user_output_directory):
        shutil.rmtree(user_output_directory)
        os.mkdir(user_output_directory)
        os.mkdir(os.path.join(user_output_directory, 'tweets'))

def fetchRecentTweets(api, fetch_properties):

    tweets = tweepy.Cursor(api.user_timeline, id = fetch_properties['user_id'], trim_user = fetch_properties['trim_user'], exclude_replies = fetch_properties['exclude_replies'], include_rts = fetch_properties['include_rts'], tweet_mode = 'extended').items(fetch_properties['nitems'])

    return tweets

def saveTweets(tweets, user_id, save_over = False):

    tweet_out_dir = os.path.join('output/' + user_id, 'tweets')

    for tweet in tweets:

        tweet = json.loads( json.dumps(tweet._json) )

        with open(os.path.join(tweet_out_dir, tweet['id_str'] + '.tweet'), 'w') as filewrite:
            json.dump(tweet, filewrite, indent = 4)

# ------------------------------------------------------------------------------

def main():

    (api_key,
    api_secret_key,
    bearer_token,
    fetch_properties,
    save_results,
    user_id) = readSettings()

    auth, api = establishAuthAPI(api_key, api_secret_key)

    tweets = fetchRecentTweets(api, fetch_properties)

    if save_results:
        makeMainOutputDirectory()
        makeResultsDirectories(user_id)
        saveTweets(tweets, user_id, save_over = True)


if __name__ == '__main__':
    main()
