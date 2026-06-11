import tweepy
import os
from dotenv import load_dotenv
import re
import pyjson5
import time
from datetime import datetime

def get_client():
    client = tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )
    return client


def read_archive():
    with open('tweets.js', 'r', encoding='utf-8') as f:
        contenido = f.read()

    data_clean = re.sub(r'window\.YTD\.tweets\.part\d+ =', '', contenido).strip().rstrip(';').strip()
    tweets     = pyjson5.loads(data_clean)
    return tweets


def extract_data(tweets):
    data_list    = []
    retweet_list = []

    for tweet in tweets:
        data_id   = tweet['tweet']['id']
        data_date = tweet['tweet']['created_at']
        date      = datetime.strptime(data_date, '%a %b %d %H:%M:%S %z %Y')
        if not tweet['tweet']['full_text'].startswith('RT @'):
            data_list.append({'id': data_id, 'created': date})

        if tweet['tweet']['full_text'].startswith('RT @'):
            retweet_list.append({'id': data_id, 'created': date})

    return data_list, retweet_list

def delete_tweets(data_list, client):
    for tweet_id in data_list:
        try:
            client.delete_tweet(tweet_id, user_auth=True)
            print(f'Tweet con el ID: {tweet_id} eliminado')
        except tweepy.TweepyException as e:
            print(f'Error eliminando {tweet_id}: {e}')
        time.sleep(53)

if __name__ == '__main__':
    load_dotenv()
    client  = get_client()
    tweets  = read_archive()
    id_list = extract_data(tweets)
    delete_tweets(id_list, client)