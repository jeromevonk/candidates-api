#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import requests
import sys

#-------------------------------------------------------------------------------
# Hosted locally or in heroku
#------------------------------------------------------------------------------- 
LOCAL  = 'http://localhost:5000/candidates/api/v1.0/'
HEROKU = 'https://candidates-api.herokuapp.com/candidates/api/v1.0/'

# Default to localhost
URL_BASE = LOCAL

# Parse command line argument
if len(sys.argv) > 1:
    if 'heroku' == sys.argv[1]:
        URL_BASE = HEROKU 

 
#-------------------------------------------------------------------------------
# Get list of candidates
#-------------------------------------------------------------------------------
print("Updating candidate...")
candidate = { "name" : "Jerome Vergueiro Vonk", "picture" : "TODO", "birthdate" : "18/02/1988", "gender" : "Male",
	          "email" : "vonkjerome@gmail.com", "phone" : "+5511912345678", "address" : "Avenida Paulista, 1",
              "longitude": 9.96233, "latitude": 49.80404, "tags" : ["engineer", "mecathronics"], "experience" : ["Electronic Arts", "Diebold Nixdorf"], "education" : ["USP", "Udacity"]}
url = URL_BASE + 'candidates/1'
r = requests.put(url, json = candidate)
print(r.status_code)
print(r.text) 
