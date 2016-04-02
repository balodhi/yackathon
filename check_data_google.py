import json
import sys
import urllib2
import 'keys'

'''
	Read from json_file, then make a call too Google API, to find Google address.
	Dumps results to target file.
	You need a keys.py file where you store (at least) 5 API keys.
'''

target = open('mtl_compare.json', 'w')
json_file = 'mtl_data.json'
i = 0
with open(json_file) as f:
	for line in f:
		i=i+1
		if i % 5 == 0:
			api_key = API_KEY_1
		elif i % 5 == 1:
			api_key = API_KEY_2
		elif i % 5 == 2:
			api_key = API_KEY_3
		elif i % 5 == 3:
			api_key = API_KEY_4
		else:
			api_key = API_KEY_5
		data = json.loads(line)
		name = (data['name'] + '+' + data['city']).replace(' ', '+')
		url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + name + '&key=' + api_key
		print data['name']
		print url
		google_data = json.load(urllib2.urlopen(url.encode('utf8')))
		#print google_data
		if (len(google_data['results']) == 1):
			google_business = google_data['results'][0]
			result = {}
			result['name'] = data['name']
			result['yelp_addr'] = data['full_address'].replace('\n', ', ')
			result['yelp_long'] = data['longitude']
			result['yelp_lat'] = data['latitude']
			result['yelp_neighborhoods'] = data['neighborhoods']
			result['google_addr'] = google_business['formatted_address']
			result['google_long'] = google_business['geometry']['location']['lng']
			result['google_lat'] = google_business['geometry']['location']['lat']
			#print result
			json.dump(result, target)
			
			



