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

def makeResultsDirectories(sub_dir):

    if not os.path.exists('tweets'):
        os.mkdir('tweets')
        os.mkdir(os.path.join('tweets', sub_dir))
    elif os.path.exists('tweets'):
        os.mkdir(os.path.join('tweets', sub_dir))

    return None

def fetchRecentTweets(api, fetch_properties):

    tweets = tweepy.Cursor(api.user_timeline, id = fetch_properties['user_id'], trim_user = fetch_properties['trim_user'], exclude_replies = fetch_properties['exclude_replies'], include_rts = fetch_properties['include_rts'], tweet_mode = 'extended').items(fetch_properties['nitems'])

    return tweets

def saveTweets(tweets, user_id, save_over = False):

    out_dir = os.path.join('tweets', user_id)

    if save_over and os.path.exists(out_dir):
            shutil.rmtree(out_dir)

    makeResultsDirectories(user_id)

    for tweet in tweets:

        tweet = json.loads( json.dumps(tweet._json) )

        with open(os.path.join(out_dir, tweet['id_str'] + '.tweet'), 'w') as filewrite:
            json.dump(tweet, filewrite, indent = 4)

    return None

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
        saveTweets(tweets, user_id, save_over = True)


if __name__ == '__main__':
    main()
