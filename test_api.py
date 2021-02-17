import tweepy

def establishAuthAPI(consumer_key, consumer_secret):

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    return auth, api

def main():

    consumer_key = 'SE9GwvVCgOj2pBFsSlLYoZmTf'
    consumer_secret = 'JNaLFvySvRbwLAczIvkb9QIAXuDCamixeIaNqxrOkNfCrFduNB'

    auth, api = establishAuthAPI(consumer_key, consumer_secret)

    print(type(auth))
    print(type(api))

    for tweet in tweepy.Cursor(api.user_timeline, id = 'ormcbrien').items(20):
        print(tweet.id)
        print(tweet.text)
        print('')

if __name__ == '__main__':
    main()
