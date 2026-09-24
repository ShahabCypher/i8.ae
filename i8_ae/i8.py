import requests

class i8():
	def __init__(self, api_key):
		self.key = api_key

	# link shortener
	def short(self, url, password=None):
		if self.key == None:
			raise Exception("Please add API KEY first: i8 = i8(key)")

		else:
			# API requires "Bearer <key>" (https://i8.ae/developers)
			key = str(self.key)
			if not key.lower().startswith("bearer "):
				key = "Bearer " + key

			headers = {
				'Authorization': key,
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
			try:
				response = url_req.json()
			except ValueError:
				# non-JSON body, e.g. hitting the 30 req/min rate limit
				raise Exception("HTTP %s: %s" % (url_req.status_code, url_req.text[:200]))

			if response['error'] != 0:
				message = response['message']
				raise Exception(message)
			
			shorted = response['shorturl']
			
			# return shorted link
			return shorted
