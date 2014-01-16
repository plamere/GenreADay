# Genre A Day

Genre-A-Day is a web app that presents a new music genre every day. For each genre it presents:

 - a brief description of the genre
 - a list of similar genres
 - the set of top artists for that genre (which are linked to the echotron)
 - A set of playlists:
 	- intro - canonical songs meant to introduce the genre
 	- current - most popular being played today
 	- emerging - unfamiliar to most listeners
 	
 The app is hosted at[ Genre A Day](http://static.echonest.com/GenreADay/)
 
 Included in the web app is a python script: tweeter.py. This script runs
 as a daily cronjob. It collects Genre-A-Day info about the current day's genre and tweets it on th GenreADay twitter account.