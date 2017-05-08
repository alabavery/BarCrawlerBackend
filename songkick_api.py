import requests
from datetime import datetime
from typing import Tuple, List, Generator, Dict


# Could also make sure you're putting only headliners or putting all bands for a given show together, using
# show id to group them and billing index to see which is headliner


Venue = List[str] # list of (songkick venue id, venue name, image file name)
def get_shows_from_songkick(base_uri: str, 
					venue_list: List[Venue],
					start_datetime: datetime, 
					end_datetime: datetime):


	Show_Dict = Dict[str, str] # dict of {venue, time, artist, artist_id}
	Show_List = List[Show_Dict]
	Date_And_Shows = Tuple[str, Show_List] # tuple of (date, Show_List)

	def insert_new_show_dict(new_show_dict: Show_Dict,
							new_date: str,
							all_dates_and_shows: List[Date_And_Shows]):
		
		for date_counter, date_and_shows in enumerate(all_dates_and_shows):
			
			if date_and_shows[0] > new_date:
				all_dates_and_shows.insert(date_counter, (new_date, [new_show_dict]))
				return
			elif date_and_shows[0] == new_date:
				date_and_shows[1].append(new_show_dict)
				return

		all_dates_and_shows.append((new_date, [new_show_dict]))


	def add_shows_for_venue(base_uri: str, 
					venue: Venue,
					start_datetime: datetime, 
					end_datetime: datetime,
					all_dates_and_shows: List[Date_And_Shows]
					):

			uri = base_uri.format(venue[0])
			try:
				response_events = requests.get(uri).json()['resultsPage']['results']['event']
			except KeyError: # in the case that a venue has no upcoming shows, no 'event' key
				return None

			for event in response_events:

				if event['type'] == 'Concert':
					show_datetime = datetime.strptime(event['start']['date'], "%Y-%m-%d")
					
					if show_datetime >= start_datetime:	
						if show_datetime <= end_datetime:
							show_dict = {}
							show_dict['event_id'] = str(event['id'])
							show_dict['time'] = event['start']['time']
							performance_json = event['performance']
							show_dict['artist_name'] = performance_json[0]['artist']['displayName']
							show_dict['artist_id'] = performance_json[0]['artist']['id']
							show_dict['band_img'] = "https://mohawkaustin.com/_/made/_/remote/https_res.\
							cloudinary.com/hjbfjdt7p/image/upload/c_fill,w_470/v1467240024/neqbteulerpqi\
							kkcroeb_256_256_80_s_c1_c_t_0_0_1.jpg"
							show_dict['venue'] = venue[1]
							show_dict['venue_img'] = venue[2]

							if len(all_dates_and_shows) > 0:
								insert_new_show_dict(show_dict, event['start']['date'], all_dates_and_shows)
							else:
								all_dates_and_shows.append((event['start']['date'], [show_dict]))


	all_dates_and_shows = []
	for venue in venue_list:
		add_shows_for_venue(base_uri, venue, start_datetime, end_datetime, all_dates_and_shows)
	return all_dates_and_shows


