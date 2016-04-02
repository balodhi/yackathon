import json
import sys

'''
	python find_mtl.py '/path/to/yelp_academic_dataset_business.json'
	This will dump all Montreal data to mtl_data.json
'''
if(len(sys.argv) == 1):
	print 'ERROR'

target = open('mtl_data.json', 'w')

json_file = sys.argv[1]
with open(json_file) as f:
	for line in f:
		if '"city": "Montr\u00e9al"' in line:
			print line
			target.write(line)
