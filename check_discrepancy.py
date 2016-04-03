from math import sin, cos, sqrt, atan2, radians
import json
import sys

def get_distance(latitude1, longitude1, latitude2, longitude2):
	# approximate radius of earth in km
	R = 6373.0


	lat1 = radians(latitude1)
	lon1 = radians(longitude1)
	lat2 = radians(latitude2)
	lon2 = radians(longitude2)

	dlon = lon1 - lon2
	dlat = lat1 - lat2

	a = sin(dlat / 2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance

def compare_address(address1, address2):
	yelp_address = address1.replace(',', '').split(' ')
	google_address = address2.replace(',', '').split(' ')

	if yelp_address[0] == google_address[0]:
		if yelp_address[1] and yelp_address[1] in google_address:
			return True
		if yelp_address[2] and yelp_address[2] in google_address:
			return True
	return False

target = open('yelp_waterloo_location_discrepancies.json', 'w')
json_file = 'yelp_google_waterloo_data.json'

with open(json_file) as f:
	for line in f:
		result = {}
		data = json.loads(line)

		yelp_data = data['yelp_data']
		google_data = data['google_data']
		name = data['name']

		longitude = yelp_data['longitude']
		latitude = yelp_data['latitude']
		regions = yelp_data['neighborhoods']
		yelp_address = yelp_data['address']

		distance_discrepancy = False
		for business in google_data:
			print business['address'].encode('utf8')
			distance = get_distance(business['latitude'], business['longitude'], latitude, longitude)
			if distance > 0.05:
				continue
			else:
				distance_discrepancy = True
				break

		if distance_discrepancy:
			result['distance'] = distance
		else:
			result['distance'] = sys.maxint

		address_discrepancy = False
		for business in google_data:
			google_address = business['address']
			if not compare_address(yelp_address, google_address):
				address_discrepancy = True
				break

		if address_discrepancy:
			result['google_address'] = google_address
		else:
			result['google_address'] = yelp_address

		result['name'] = name
		result['longitude'] = longitude
		result['latitude'] = latitude
		result['distance_discrepancy'] = distance_discrepancy
		result['address_discrepancy'] = address_discrepancy
		result['yelp_address'] = yelp_address
		
		if len(regions) > 0:
			result['region'] = regions[0]
		else:
			result['region'] = ' '


		json.dump(result, target)
		target.write('\n')