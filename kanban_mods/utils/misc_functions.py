# Copyright (c) 2024, Kevin Salt and contributors
# For license information, please see license.txt

def dump(obj):
	attrs = vars(obj)
	# {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
	# now dump this in some way or another
	print(', '.join("%s: %s \r\n" % item for item in attrs.items()))