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
# Insert one candidate with missing information
#-------------------------------------------------------------------------------
print("Inserting candidate...")
candidate = { "name" : "Jerome Vonk", "picture" : "TODO", "birthdate" : "00/02/1988", "gender" : "Male",
	          "email" : "vonk@gmail.com", "phone" : "+5511912345678", "address" : "Avenida Paulista, 1",
              "longitude": 0.0, "latitude": 0.0, "tags" : [], "experience" : [], "education" : []}
url = URL_BASE + 'candidates'
r = requests.post(url, json = candidate)
print(r.status_code)
print(r.text)
 