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
LOCAL  = 'http://localhost:5000/candidates/api/v1.0/'
HEROKU = 'https://candidates-api.herokuapp.com/candidates/api/v1.0/'
AWS    = 'http://candidates-api.sa-east-1.elasticbeanstalk.com/candidates/api/v1.0/'

# Default to localhost
URL_BASE = LOCAL

# Parse command line argument
if len(sys.argv) > 1:
    if 'heroku' == sys.argv[1]:
        URL_BASE = HEROKU
    if 'aws' == sys.argv[1]:
        URL_BASE = AWS

_pswd  = getpass.getpass('Password: ') 
#-------------------------------------------------------------------------------
# Delete all candidates
#-------------------------------------------------------------------------------
try:
    url = URL_BASE + 'candidates'
    r = requests.delete(url, auth=('user', _pswd))
    print(r.status_code)
    print(r.text)
    
except requests.exceptions.RequestException as e:
    print(e)
        
