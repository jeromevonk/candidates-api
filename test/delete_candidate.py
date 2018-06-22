#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import requests
import sys
import getpass
from requests.auth import HTTPBasicAuth

#-------------------------------------------------------------------------------
# Hosted locally or in heroku
#-------------------------------------------------------------------------------
LOCAL  = 'http://localhost:5000/candidates/api/v2.0/'
HEROKU = 'https://candidates-api.herokuapp.com/candidates/api/v2.0/'
AWS    = 'http://candidates-api.sa-east-1.elasticbeanstalk.com/candidates/api/v2.0/'

# Default to localhost
URL_BASE = LOCAL

# Initialize with 0
candidate_id = 0

# Parse command line arguments
if len(sys.argv) > 1:
    try:
        # Get candidate ID
        candidate_id = int(sys.argv[1])
    except:
        print("Candidate id must be an integer, aborting.")
        sys.exit()

if candidate_id == 0:
    print("Candidate id not specified, aborting.")
    sys.exit()


if len(sys.argv) > 2:
    if 'heroku' == sys.argv[1]:
        URL_BASE = HEROKU
    if 'aws' == sys.argv[1]:
        URL_BASE = AWS

_pswd  = getpass.getpass('Password: ')
#-------------------------------------------------------------------------------
# Delete one candidate a time
#-------------------------------------------------------------------------------
try:
    url = URL_BASE + 'candidates/{}'.format(candidate_id)
    r = requests.delete(url, auth=('user', _pswd))
    print(r.status_code)
    print(r.text)

except requests.exceptions.RequestException as e:
    print(e)

