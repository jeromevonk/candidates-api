#-------------------------------------------------------------------------------
# Name:        Candidates API
# Author:      Jerome Vergueiro Vonk
# Created:     30/05/2018
#-------------------------------------------------------------------------------

import requests
 
URL_BASE = 'http://localhost:5000/candidates/api/v1.0/'
 
#-------------------------------------------------------------------------------
# Get list of candidates
#-------------------------------------------------------------------------------
print("Updating candidate...")
candidate = { "name" : "Jerome Vergueiro Vonk", "picture" : "TODO", "birthdate" : "18/02/1988", "gender" : "Male",
	          "email" : "vonkjerome@gmail.com", "phone" : "+5511912345678", "address" : "Avenida Paulista, 1",
              "longitude": 9.96233, "latitude": 49.80404, "tags" : ["engineer", "mecathronics"], "experience" : ["Electronic Arts", "Diebold Nixdorf"], "education" : ["USP", "Udacity"]}
url = URL_BASE + 'candidates/0'
r = requests.put(url, json = candidate)
print(r.status_code)
print(r.text) 
