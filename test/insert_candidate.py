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
        if r.status_code not in range(200, 300):
            print(r.text)

    except requests.exceptions.RequestException as e:
        print(e)

#-------------------------------------------------------------------------------
# Hosted locally or in heroku
#-------------------------------------------------------------------------------
LOCAL  = 'http://localhost:5000/candidates/api/v2.0/'
HEROKU = 'https://candidates-api.herokuapp.com/candidates/api/v2.0/'
AWS    = 'http://candidates-api.sa-east-1.elasticbeanstalk.com/candidates/api/v2.0/'

# Default to localhost
URL_BASE = LOCAL

# Parse command line argument
if len(sys.argv) > 1:
    if 'heroku' == sys.argv[1]:
        URL_BASE = HEROKU
    if 'aws' == sys.argv[1]:
        URL_BASE = AWS

#-------------------------------------------------------------------------------
# Insert one candidate
#-------------------------------------------------------------------------------
url = URL_BASE + 'candidates'
candidate = { "name" : "Jerome Vonk", "picture" : "", "birthdate" : "18/02/1988", "gender" : 1,
              "email" : "vonk@gmail.com", "phone" : "11912345678", "address" : "Avenida Paulista, 1",
              "longitude": 0, "latitude": 0, "tags" : ["mecathronics", "dutch", "engineer"], "experience" : [], "education" : []}

# Education
graduation = {"institution" : "USP", "degree" : "Engineering", "date_start" : "01/01/2007", "date_end" : "31/12/2011", "description" : "Mechatronics Engineering is a field between mechanics and elethronics"}
masters    = {"institution" : "UV", "degree" : "Computación en nube", "date_start" : "01/10/2017", "date_end" : "8/10/2017", "description" : "Dropped out"}
candidate['education'].append(graduation)
candidate['education'].append(masters)

# Experience
diebold = {"company" : "Diebold", "job_title" : "Engineer", "date_start" : "01/01/2007", "date_end" : "31/12/2011", "description" : "Mechatronics Engineering is a field between mechanics and elethronics"}
ea      = {"company" : "EA",      "job_title" : "Tester",   "date_start" : "01/10/2017", "date_end" : "8/10/2017",  "description" : "Localization tester for brazilian portuguese"}
candidate['experience'].append(diebold)
candidate['experience'].append(ea)

print("### Inserting candidate...")
postCandidate(candidate)
