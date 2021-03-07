import os
import shutil
import tweepy
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def readSettings():

    import yaml

    with open('settings.yaml', 'r') as stream:
        all_settings = yaml.safe_load(stream)

    api_key = all_settings['api_key']
    api_secret_key = all_settings['api_secret_key']
    bearer_token = all_settings['bearer_token']
    fetch_properties = all_settings['fetch_properties']
    save_results = all_settings['save_results']
    do_plots = all_settings['do_plots']

    user_id = fetch_properties['user_id']

    full_parameters = (api_key,
                        api_secret_key,
                        bearer_token,
                        fetch_properties,
                        save_results,
                        do_plots,
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
        os.mkdir(os.path.join(user_output_directory, 'plots'))
    elif os.path.exists(user_output_directory):
        shutil.rmtree(user_output_directory)
        os.mkdir(user_output_directory)
        os.mkdir(os.path.join(user_output_directory, 'tweets'))
        os.mkdir(os.path.join(user_output_directory, 'plots'))

def fetchRecentTweets(api, fetch_properties):

    tweets = tweepy.Cursor(api.user_timeline, id = fetch_properties['user_id'], trim_user = fetch_properties['trim_user'], exclude_replies = fetch_properties['exclude_replies'], include_rts = fetch_properties['include_rts'], tweet_mode = 'extended').items(fetch_properties['nitems'])

    return tweets

def saveTweets(the_tweets, user_id, save_over = False):

    tweet_out_dir = os.path.join('output/' + user_id, 'tweets')

    for the_tweet in the_tweets:

        the_tweet = json.loads( json.dumps(the_tweet._json) )

        with open(os.path.join(tweet_out_dir, the_tweet['id_str'] + '.tweet'), 'w') as filewrite:
            json.dump(the_tweet, filewrite, indent = 4)

# ------------------------------------------------------------------------------

def setRCParameters():

    SMALL_SIZE = 15
    MEDIUM_SIZE = 20
    BIGGER_SIZE = 25

    plt.rc('font', size=SMALL_SIZE)          	# controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)     	# fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    	# fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    	# fontsize of the tick labels
    plt.rc('legend', fontsize=MEDIUM_SIZE)    	# legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  	# fontsize of the figure title

    plt.rcParams["font.family"] = "serif"
    plt.rcParams['mathtext.fontset'] = 'dejavuserif'

def extractPlotParameters(tweets):

    favourite_toplot = []
    retweet_toplot = []
    wordcounts_toplot = []

    for tweet in tweets:
        favourite_toplot.append(tweet.favorite_count)
        retweet_toplot.append(tweet.retweet_count)

        full_text = tweet.full_text
        full_text = ''.join(c for c in full_text if c not in '\n\t,.(){}[]<>*')

        # print(full_text)
        # print(full_text.split())
        # print(len(full_text.split()))
        # print('#######')

        wordcounts_toplot.append(len(full_text.split()))

    plot_parameters = {'favourites': favourite_toplot,
                        'retweets': retweet_toplot,
                        'wordcounts': wordcounts_toplot}

    return plot_parameters

def doHistogramFavouritesRetweets(plot_parameters):

    fig = plt.figure(figsize = (14, 8))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    favourite_toplot = plot_parameters['favourites']
    retweet_toplot = plot_parameters['retweets']

    ax1.hist(favourite_toplot, histtype = 'bar', edgecolor = 'black', facecolor = 'red', alpha = 0.5)
    ax2.hist(retweet_toplot, histtype = 'bar', edgecolor = 'black', facecolor = 'green', alpha = 0.5)

    ax1.set_xlabel('Favourites (likes)')
    ax1.set_ylabel('Frequency')

    ax2.set_xlabel('Retweets')

    fig.tight_layout()

    return fig

def doHistogramTweetWordCount(plot_parameters):

    fig = plt.figure(figsize = (10, 8))
    ax = fig.add_subplot(1, 1, 1)

    wordcounts_toplot = plot_parameters['wordcounts']

    ax.hist(wordcounts_toplot, histtype = 'bar', edgecolor = 'black', facecolor = 'blue', alpha = 0.5)

    ax.set_xlabel('Word count per tweet')
    ax.set_ylabel('Frequency')

    fig.tight_layout()

    return fig

def saveFigures(figures, user_id):

    figure_counter = 0

    for figure in figures:
        figure.savefig(os.path.join('output/%s/plots' %user_id, 'figure_%d.pdf' %figure_counter))
        figure_counter += 1

# ------------------------------------------------------------------------------

def main():

    (api_key,
    api_secret_key,
    bearer_token,
    fetch_properties,
    save_results,
    do_plots,
    user_id) = readSettings()

    auth, api = establishAuthAPI(api_key, api_secret_key)

    tweets = fetchRecentTweets(api, fetch_properties)

    if do_plots:
        setRCParameters()
        plot_params = extractPlotParameters(tweets)
        fig1 = doHistogramFavouritesRetweets(plot_params)
        fig2 = doHistogramTweetWordCount(plot_params)

        figs = [fig1, fig2]


    if save_results:
        makeMainOutputDirectory()
        makeResultsDirectories(user_id)
        saveTweets(tweets, user_id, save_over = True)
        saveFigures(figs, user_id)



if __name__ == '__main__':
    main()
