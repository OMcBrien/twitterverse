import tweepy

def readSettings():

    import yaml

    with open('settings.yaml', 'r') as stream:
        all_settings = yaml.safe_load(stream)

    api_key = all_settings['api_key']
    api_secret_key = all_settings['api_secret_key']
    bearer_token = all_settings['bearer_token']
    user_id = all_settings['user_id']

    full_parameters = (api_key,
                        api_secret_key,
                        bearer_token,
                        user_id)

    return full_parameters

def establishAuthAPI(api_key, api_secret_key):

    auth = tweepy.AppAuthHandler(api_key, api_secret_key)
    api = tweepy.API(auth)

    return auth, api

# ------------------------------------------------------------------------------

def main():

    (api_key,
    api_secret_key,
    bearer_token,
    user_id) = readSettings()

    auth, api = establishAuthAPI(api_key, api_secret_key)

    for tweet in tweepy.Cursor(api.user_timeline, id = 'ormcbrien').items(20):
        print(tweet.id)
        print(tweet.text)
        print('')

if __name__ == '__main__':
    main()
