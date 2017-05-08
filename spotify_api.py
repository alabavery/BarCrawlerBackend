import requests
from typing import List


def get_spotify_track(artist_name: str):
	
	def query_artist_id(artist_name: str) -> str:
		
		BASE_URI = "https://api.spotify.com/v1/search?query={0}&limit=1&type=artist&market=US"
		artist_name = artist_name.strip().replace(" ", "+")
		uri = BASE_URI.format(artist_name)
		json_response = requests.get(uri).json()
		artist_results = json_response['artists']['items']

		if len(artist_results) == 0:
			print("No results")
			return ""
		return artist_results[0]['id']


	def get_artist_top_track(artist_id: str):
		
		uri = ("https://api.spotify.com/v1/artists/{0}/top-tracks?country=US").format(artist_id)
		tracks_json = requests.get(uri).json()['tracks']

		if len(tracks_json) > 0:
			return tracks_json[0]['id']
		return None

	artist_id = query_artist_id(artist_name)
	if len(artist_id) > 0:
		return get_artist_top_track(artist_id)
	return None


