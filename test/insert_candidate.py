#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import sys
import requests
import base64

#-------------------------------------------------------------------------------
# Helper function
#------------------------------------------------------------------------------- 
def postCandidate(candidate):
    try:
        r = requests.post(url, json = candidate)
        print(r.status_code)
        print(r.text)
        
    except requests.exceptions.RequestException as e:
        print(e)

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
url = URL_BASE + 'candidates'
candidate = { "name" : "Jerome Vonk", "picture" : "", "birthdate" : "18/02/1988", "gender" : 1,
	          "email" : "vonk@gmail.com", "phone" : "11912345678", "address" : "Avenida Paulista, 1",
              "longitude": 0, "latitude": 0, "tags" : [], "experience" : ['Diebold', 'EA'], "education" : ['USP', 'Udacity']}
              
print("### Inserting candidates...")     

# a) Valid
postCandidate(candidate)

# b) Same name
candidate['email'] = 'not@thesame.com'
postCandidate(candidate)

# c) Same email
candidate['name']  = 'Jerominho Vonk'
candidate['email'] = 'vonk@gmail.com'
postCandidate(candidate)

# d) Missing birthdate, latitude, longitude 
candidate['name']  = 'Missing fields'
candidate['email'] = 'missing@fields.com'
candidate.pop('birthdate', None)
candidate.pop('latitude', None)
candidate.pop('longitude', None)
postCandidate(candidate)

# e) Insert with picture
candidate['name']  = 'Jerome with Picture'
candidate['email'] = 'jerome@picture.com'
with open('jvv.jpg', 'rb') as fi:
    content = fi.read()
    candidate['picture'] = base64.b64encode(content)
    postCandidate(candidate)
