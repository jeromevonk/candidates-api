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
print("Updating candidate...")
candidate = { "name" : "Jerome Vergueiro Vonk", "picture" : "", "birthdate" : "18/02/1988", "gender" : 1,
	          "email" : "vonk2@gmail.com", "phone" : "11912345678", "address" : "Avenida Paulista, 1",
              "longitude": 12.1314, "latitude": 12.13145, "tags" : ["engineer", "mecathronics"], "experience" : ["Electronic Arts", "Diebold Nixdorf"], "education" : ["USP", "Udacity"]}
url = URL_BASE + 'candidates/{}'.format(id_to_update)

try:
    r = requests.put(url, json = candidate)
    print(r.status_code)
    print(r.text)

except requests.exceptions.RequestException as e:
    print(e)
