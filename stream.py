import tweepy
import json
from datetime import datetime

# Variables de autenticación de Twitter
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

# Palabra clave o hashtag para seguir
hashtag = "#YOUR_HASHTAG"

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
                    'screen_name': tweet['user']['screen_name'],
                    'location': tweet['user']['location']
                }
                # Convierte el diccionario Python en una cadena JSON y la imprime en la consola
                print(json.dumps(tweet_dict))
        except Exception as e:
            print(e)

# Autenticación de Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Crear una instancia de StreamListener
listener = StreamListener()

# Crear un objeto Stream de Tweepy
stream = tweepy.Stream(auth=auth, listener=listener, tweet_mode='extended')

# Iniciar el streaming de tweets que contienen el hashtag
stream.filter(track=[hashtag])