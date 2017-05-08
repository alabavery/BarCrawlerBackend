from songkick_api import get_shows_from_songkick
from spotify_api import query_artist_spotify_id, get_artist_top_spotify_tracks
from record_artists import record_artists
import requests
from datetime import datetime
from json import dumps as json_dumps

JSON_FILE_PATH = "../posting/BarCrawler/json_file.json"
SONGKICK_BASE_URI = "http://api.songkick.com/api/3.0/venues/{0}/calendar.json?&apikey=xkHfc6I2r8CuJJfZ"
SONGKICK_VENUES = [('251',"Empty Bottle","empty-bottle"), ('524066',"Coles","coles"), ('34713',"Quenchers","quenchers"), \
					('17091',"Bottom Lounge","bottom-lounge"),('262',"Subterranean","subterranean"), \
					('212',"Beat Kitchen","beat-kitchen"), ('513326',"Lincoln Hall","lincoln-hall"), \
					('2133',"Schubas","schubas"),('1434818',"Thalia Hall","thalia-hall"),\
					('34695',"The Burlington","burlington"), ('259',"The Hideout","hideout")]

start_datetime = datetime.today()
end_datetime = datetime(2017,5,24)

all_shows = get_shows_from_songkick(SONGKICK_BASE_URI, SONGKICK_VENUES, start_datetime, end_datetime)
record_artists(all_shows, 'artist_file.json')


final_json = json_dumps(all_shows)
json_file = open(JSON_FILE_PATH, 'w')
json_file.write(final_json)
json_file.close()
