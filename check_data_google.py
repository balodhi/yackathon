import json
import sys
import urllib2
import keys

'''
	Read from json_file, then make a call too Google API, to find Google address.
	Dumps results to target file.
	You need a keys.py file where you store (at least) 5 API keys.
'''

target = open('yelp_google_mtl_data.json', 'w')
json_file = 'yelp_mtl_data.json'

i = 0
with open(json_file) as f:
	for line in f:
		i=i+1
		if i % 5 == 0:
			api_key = keys.API_KEY_1
		elif i % 5 == 1:
			api_key = keys.API_KEY_2
		elif i % 5 == 2:
			api_key = keys.API_KEY_3
		elif i % 5 == 3:
			api_key = keys.API_KEY_4
		else:
			api_key = keys.API_KEY_5
		data = json.loads(line)
		name = (data['name'] + '+' + data['city']).replace(' ', '+')
		url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + name + '&key=' + api_key

		google_data = json.load(urllib2.urlopen(url.encode('utf8')))
	
		google_businesses = google_data['results']
		result = {}
		result['name'] = data['name']
		yelp_data = {}
		yelp_data['address'] = data['full_address'].replace('\n', ', ')
		yelp_data['long'] = data['longitude']
		yelp_data['lat'] = data['latitude']
		yelp_data['neighborhoods'] = data['neighborhoods']
		result['yelp_data'] = yelp_data

		google_locations = []
		for google_business in google_businesses:
			google_data = {}
			google_data['address'] = google_business['formatted_address']
			google_data['long'] = google_business['geometry']['location']['lng']
			google_data['lat'] = google_business['geometry']['location']['lat']
			google_locations.append(google_data)
		result['google_data'] = google_locations


		print name
		print url
		json.dump(result, target)
			
			



