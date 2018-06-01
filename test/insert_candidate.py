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
print("Inserting candidate...")
candidate = { "name" : "Jerome Vergueiro Vonk", "picture" : "TODO", "birthdate" : "18/02/1988", "gender" : "Male",
	          "email" : "vonkjerome@gmail.com", "phone" : "+5511912345678", "address" : "Avenida Paulista, 1",
              "longitude": 0, "latitude": 0, "tags" : [], "experience" : [], "education" : []}
url = URL_BASE + 'candidates'
r = requests.post(url, json = candidate)
print(r.status_code)
print(r.text)
 