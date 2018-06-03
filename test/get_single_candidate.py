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
#[IMPROVEMENT]: first call get all candidates and then get the ID of wanted candidate
url = URL_BASE + 'candidates/1'

try:
    r = requests.get(url)
    print(r.status_code)
    print(r.text)
except requests.exceptions.RequestException as e:
    print(e)
