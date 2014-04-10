import tweepy
import datetime
import simplejson as json
import os
import urllib
import pyen
import sys
 
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

def  get_genre_description(genre):
    results = en.get('genre/profile', name=genre, bucket='description')
    return results['genres'][0]["description"]


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
   
def get_link(genre):
    link = ' http://static.echonest.com/GenreADay/?'
    link += urllib.urlencode( {'genre':genre} ) 
    return link

def post_tweet(date, genre):
    artists = get_genre_artists(cur_genre)
    link = get_link(genre)
    tweet = 'The Genre-A-Day for ' + date + ' is ' + genre.title() + '::'
    remaining_length = short_length + len(tweet) 
    tweet = add_artists(tweet, remaining_length, artists)
    tweet = tweet + link
    post(tweet)

def post_midnight_tweet(date, genre):
    artists = get_genre_artists(cur_genre)
    link = get_link(genre)
    tweet = "Get ready for the next Genre-A-Day: " + genre.title() 
    tweet = tweet + link
    post(tweet)
    

def trim_to_length(s, length, ch):
    while len(s) > length:
        # print 'ttl in', length, ch, s
        cpos = s.rfind(ch)
        if cpos > 0:
            s = s[:cpos]
        else:
            break
        #print 'ttl', length, len(s), s
    # print 'ttl out', len(s), s
    return s

def filter_description(desc, length):
    min_length = 30
    desc_out = trim_to_length(desc, length, '.')
    if len(desc_out) > length or len(desc_out) < min_length:
        desc_out = trim_to_length(desc, length - 4, ' ')
        if len(desc_out) > length or len(desc_out) < min_length:
            desc_out = desc[:length - 4]
        desc_out += ' ...'
    return desc_out
        

def post_tweet2(date, genre):
    description = get_genre_description(genre)
    if len(description ) == 0:
        post_tweet(date, genre)
    else:
        description = filter_description(description, 140 - (short_length + 4))
        tweet = description + get_link(genre)
        post(tweet)


if __name__ == '__main__':
    api = authenticate()
    date = get_date()
    delta = get_day_delta()
    genres = load_genre_list()
    cur_genre = genres[delta]

    if len(sys.argv) > 1:
        if sys.argv[1] == '--morning':
            post_tweet(date, cur_genre)
        elif sys.argv[1] == '--afternoon':
            post_tweet2(date, cur_genre)
        elif sys.argv[1] == '--midnight':
            post_midnight_tweet(date, cur_genre)

        if sys.argv[1] == '--midnight-test':
            testing = True
            post_midnight_tweet(date, cur_genre)

        if sys.argv[1] == '--morning-test':
            testing = True
            post_tweet(date, cur_genre)
        elif sys.argv[1] == '--afternoon-test':
            testing = True
            post_tweet2(date, cur_genre)
        elif sys.argv[1] == '--morning-full-test':
            testing = True
            for g in genres:
                post_tweet(date, g)
        elif sys.argv[1] == '--afternoon-full-test':
            testing = True
            for g in genres:
                post_tweet2(date, g)
    else:
        print "usage tweeter [--morning] [--afternoon]"

