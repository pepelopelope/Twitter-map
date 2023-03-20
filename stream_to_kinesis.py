import tweepy
import json
import boto3
from datetime import datetime

# Variables de autenticación de Twitter
consumer_key = 'TU_CONSUMER_KEY'
consumer_secret = 'TU_CONSUMER_SECRET'
access_token = 'TU_ACCESS_TOKEN'
access_token_secret = 'TU_ACCESS_TOKEN_SECRET'

# Palabra clave o hashtag para seguir
hashtag = "#TUCERTAINHASHTAG"

# Variables de configuración de Kinesis
kinesis_client = boto3.client('kinesis', region_name='TU_REGION')
kinesis_stream_name = 'TU_NOMBRE_DE_STREAM'

# Clase StreamListener
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            # Filtra los tweets que contienen el hashtag
            if tweet['text'].find(hashtag) >= 0:
                # Convierte la información del tweet en un diccionario Python
                tweet_dict = {}
                tweet_dict['id'] = tweet['id']
                tweet_dict['text'] = tweet['text']
                tweet_dict['created_at'] = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                tweet_dict['coordinates'] = tweet['coordinates']['coordinates'] if tweet['coordinates'] else None
                tweet_dict['user'] = {
                    'screen_name':
