#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import requests
import sys
import json
import ast
from get_all_candidates import getAllCandidates

#-------------------------------------------------------------------------------
# Helper function
#-------------------------------------------------------------------------------
def updateCandidate(candidate):
    try:
        r = requests.put(url, json = candidate)
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
# Find the candidate ID
#-------------------------------------------------------------------------------

# Perform the query
response = getAllCandidates()

# Conver to a list of dictionaries
jdata = json.loads(response)

# Hold information of the ID
id_to_update = 0

# Find id of candidate 'Jerome Vonk'
for item in jdata['candidates']:
    if item['name'] == 'Jerome Vonk':
        id_to_update = item['id']
        print("Found Jerome Vonk with id = {}".format(id_to_update) )

if id_to_update == 0:
    print("Did not find Jerome Vonk on database")
    sys.exit()

#-------------------------------------------------------------------------------
# Update a candidate
#-------------------------------------------------------------------------------
url = URL_BASE + 'candidates/{}'.format(id_to_update)
candidate = { "name" : "Jerome Vergueiro Vonk", "picture" : "", "birthdate" : "18/02/1988", "gender" : 1,
              "email" : "vonk@gmail.com", "phone" : "11912345678", "address" : "Avenida Paulista, 1",
              "longitude": 0, "latitude": 0, "tags" : ["mecathronics", "dutch/brazilian",], "experience" : [], "education" : []}

# Education
graduation = {"institution" : "USP", "degree" : "Engineering", "date_start" : "01/01/2007", "date_end" : "31/12/2011", "description" : "Mechatronics Engineering is a field between mechanics and elethronics"}
candidate['education'].append(graduation)

# Experience
diebold = {"company" : "Diebold", "job_title" : "Engineer", "date_start" : "01/01/2007", "date_end" : "31/12/2011", "description" : "Mechatronics Engineering is a field between mechanics and elethronics"}
ea      = {"company" : "EA",      "job_title" : "Tester",   "date_start" : "15/06/2017", "date_end" : "28/09/2018",  "description" : "Localization tester for brazilian portuguese"}
candidate['experience'].append(diebold)
candidate['experience'].append(ea)

print("Updating candidate...")
updateCandidate(candidate)
