import os
import shutil
import tweepy

def readSettings():

    import yaml

    with open('settings.yaml', 'r') as stream:
        all_settings = yaml.safe_load(stream)

    api_key = all_settings['api_key']
    api_secret_key = all_settings['api_secret_key']
    bearer_token = all_settings['bearer_token']
    user_id = all_settings['user_id']
    save_results = all_settings['save_results']

    full_parameters = (api_key,
                        api_secret_key,
                        bearer_token,
                        user_id,
                        save_results)

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

def fetchRecentTweets(api, user_id, nitems = 100):

    tweets = tweepy.Cursor(api.user_timeline, id = user_id).items(nitems)

    return tweets

def saveTweets(tweets, user_id, save_over = False):

    out_dir = os.path.join('tweets', user_id)

    if save_over and os.path.exists(out_dir):
            shutil.rmtree(out_dir)

    makeResultsDirectories(user_id)

    for tweet in tweets:
        with open(os.path.join(out_dir, tweet.id_str + '.tweet'), 'w') as filewrite:
            filewrite.write(tweet.text)

    return None

# ------------------------------------------------------------------------------

def main():

    (api_key,
    api_secret_key,
    bearer_token,
    user_id,
    save_results) = readSettings()

    auth, api = establishAuthAPI(api_key, api_secret_key)

    tweets = fetchRecentTweets(api, user_id, 50)

    if save_results:
        saveTweets(tweets, user_id, save_over = True)


if __name__ == '__main__':
    main()
