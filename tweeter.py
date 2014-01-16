import tweepy
import datetime
import simplejson as json
import os
import urllib
import pyen
 
consumer_key = os.environ['twitter_consumer_key']
consumer_secret = os.environ['twitter_consumer_secret']
access_token = os.environ['twitter_access_token']
access_token_secret = os.environ['twitter_access_token_secret']

testing = False

start_date = datetime.date(2014, 1, 10)
short_length = 20

en = pyen.Pyen()

def authenticate():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def post(text):
    if testing:
        print text
    else:
        print text
        api.update_status(text)


def get_genre_of_the_day():
    return 'jazz'


def get_date():
    return datetime.date.today().strftime("%b %d")

def get_day_delta():
    delta =  datetime.date.today() - start_date
    return delta.days


def load_genre_list():
    s = open('genres.js').read()
    genres = json.loads(s)
    return genres

def  get_genre_artists(genre):
    results = en.get('genre/artists', name=genre)
    return results['artists']


def add_artists(tweet, length, artists):
    prefix = ' with music by '
    suffix = ' and more '
    sartists = ''
    cur_len = len(prefix) + len(suffix)

    for a in artists:
        name = a['name']
        if len(name) + 2 + len(prefix) + len(suffix) + len(sartists) < length:
            if len(sartists) > 0:
                sartists += ', '
            sartists += name

    if len(sartists) > 0:
        full_artist_string = prefix + sartists + suffix
        tweet = tweet.replace('::', full_artist_string)

    return tweet
    
def build_tweet(date, genre, artists):
    link = 'http://static.echonest.com/GenreADay/?'
    link += urllib.urlencode( {'genre':genre} ) 
    tweet = 'The Genre-A-Day for ' + date + ' is ' + genre.title() + '::'
    remaining_length = short_length + len(tweet) 
    tweet = add_artists(tweet, remaining_length, artists)
    return tweet + link
    

if __name__ == '__main__':
    api = authenticate()
    date = get_date()
    delta = get_day_delta()
    genres = load_genre_list()
    cur_genre = genres[delta]
    artists = get_genre_artists(cur_genre)
    tweet = build_tweet(date, cur_genre, artists)
    post(tweet)





