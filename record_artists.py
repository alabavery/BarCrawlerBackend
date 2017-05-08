import json
import spotify_api

def record_artists(songkick_shows, artist_file_path):

	artist_file = open(artist_file_path, 'r')
	recorded_artists = json.loads(artist_file.read())
	artist_file.close()

	for date in songkick_shows:
		for show in date[1]:
			already_recorded = 0 < len([0 for artist in recorded_artists if artist['songkick_id'] == show['artist_id']])

			if already_recorded:
				continue
			else:
				spotify_track_id = spotify_api.get_spotify_track(show['artist_name'])
				new_artist_dict = {'songkick_id':show['artist_id'], 'name':show['artist_name'], 'spotify_track_uri':spotify_track_id, \
									'genres':"not sure yet where this will come from"}
				recorded_artists.append(new_artist_dict)

	new_json = json.dumps(recorded_artists)
	artist_file = open(artist_file_path, 'w')
	artist_file.write(new_json)
	artist_file.close()