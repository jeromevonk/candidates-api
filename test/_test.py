#-------------------------------------------------------------------------------
# Name:        Candidates API
# Author:      Jerome Vergueiro Vonk
# Created:     30/05/2018
#-------------------------------------------------------------------------------

import requests
 
URL_BASE = 'http://localhost:5000/candidates/api/v1.0/'
 
#-------------------------------------------------------------------------------
# Insert one candidate with missing information
#-------------------------------------------------------------------------------
# print("Inserting candidate...")
# candidate = { "name" : "Jerome Vergueiro Vonk", "picture" : "TODO", "birthdate" : "18/02/1988", "gender" : "Male",
	          # "email" : "vonkjerome@gmail.com", "phone" : "+5511912345678", "address" : "Avenida Paulista, 1",
              # "longitude": 0, "latitude": 0, "tags" : [], "experience" : [], "education" : []}
# url = URL_BASE + 'insert'
# r = requests.post(url, json=candidate)
# print(r.status_code)
# print(r.text)
 
# #-------------------------------------------------------------------------------
# # Get list of candidates
# #-------------------------------------------------------------------------------
# url = URL_BASE
# r = requests.get(url)
# print(r.status_code)
# print(r.text) 
 
 
 
# # API v1.2 - PUT (Metadata)
# url = URL_BASE + 'api/v1_2/recipes/2'
# json_data = {'title': 'Updated recipe', 'description': 'My favorite recipe'}
# r = requests.put(url, json=json_data, auth=token_auth)
# print(r.status_code)
# print(r.text)
 
# # API v1.2 - PUT (Add image)
# url = URL_BASE + 'api/v1_2/recipes/2'
# r = requests.put(url, auth=token_auth, files={'recipe_image': open('IMG_6127.JPG', 'rb')})
# print(r.status_code)
# print(r.text)