import tweepy
import os
from dotenv import load_dotenv
import re
import json
import time

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

    data_clean = re.sub(r'window\.YTD\.tweets\.part\d+ =', '', contenido)
    tweets     = json.loads(data_clean)
    return tweets


def extract_ids(tweets):
    id_list    = []

    for tweet in tweets:
        id = tweet["tweet"]["id"]
        id_list.append(id)

    return id_list

def delete_tweets(id_list, client):
    for tweet_id in id_list:
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
    id_list = extract_ids(tweets)
    delete_tweets(id_list, client)