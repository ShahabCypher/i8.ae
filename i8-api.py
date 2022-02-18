import sys
import json
import subprocess
import pkg_resources

# check if modules are installed
required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

# install missing modules
if missing:
	python = sys.executable
	subprocess.check_call([python, '-m', 'pip', 'install', *missing],  stdout=subprocess.DEVNULL)

import requests

class i8():
	def __init__(self):
		self.key = None
	
	# add api key
	def add(self, api_key):
		self.key = api_key
	
	# link shortener
	def short(self, url, password=None):
		
		if self.key == None:
			raise Exception("Please add API KEY first => i8.add(key)")
			
		else:
			headers = {
				'Authorization': self.key,
				'Content-Type': 'application/json'
			}
			
			data = {
				'url': url
			}
			
			# adding password if exists
			if password != None:
				data['password'] = password
			
			# sending request to i8.ae
			url_req = requests.post(
				'https://i8.ae/api/url/add',
				json=data,
				headers=headers
			)
			
			# getting i8.ae response
			response = url_req.json()
			
			if response['error'] != 0:
				message = response['message']
				raise Exception(message)
			
			shorted = response['shorturl']
			
			# return shorted link
			return shorted