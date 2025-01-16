# Copyright (c) 2024, Kevin Salt and contributors
# For license information, please see license.txt
# 
# Just a catchall class for those useful functions that pop up
# regularly. I'm droppingh them here so I don't have to keep
# on typing them in

def dump(obj, indent=0, itemcount = 0): 
	
	'''
	dump(object, indent, itemcount) ##
	A debugging tool which recursively dismantles a CLASS, LIST OR DICT object and 
	prints it out to the console as a nicely ordered display ... For any other object 
	it just prints them oudirectly.

	Parameters:
	obj: the object to be dumped
	indent: the number of sapaces to indent each recursive iteration
	itemcount: the value of the current index in a list as it id printed

	Outputs:
	None .. it prints to the console.

	'''	
	if isinstance(obj, list): 
		itemcount = 0 
		for value in obj: 
			if isinstance(value, list): # or isinstance(value, dict) or isinstance(value, object) and not isinstance(value, (int, float, str, bool, list, dict)): 
				print(' ' * indent + "[list " + str(itemcount) + "]") 
				dump(value, indent + 4, itemcount) 
				itemcount += 1 
			else: 
				print(' ' * indent + "[list " + str(itemcount) + "]: " + str(value)) 
				itemcount += 1 
	elif isinstance(obj, dict): 
		for key, value in obj.items(): 
			if isinstance(value, dict) or isinstance(value, list): 
				print(' ' * indent + f"{key}:") 
				dump(value, indent + 4, itemcount) 
			else: 
				print(' ' * indent + f"{key}: {value}") 
	elif isinstance(obj, object) and not isinstance(obj, (int, float, str, bool, list, dict, set, type(None))): 
		print(' ' * indent + f"Instance of {obj.__class__.__name__}:") 
		dump(obj.__dict__, indent + 4) 
	else: 
		print(' ' * indent + str(obj))
	

class Support_mail():
	# I am forced to set up thos sort of stuff because of the way Frappe uses
	# class objects for most things ... It's kust a repository for certain 
	# variables which can be used to send pro-forma mails. I may create more
	# for different purposes - e.g. sales

	def __init__(self):
		self.email_id = "kevin@kanban-group.com"
		self.sender   = "noreply@kanban-group.com"
