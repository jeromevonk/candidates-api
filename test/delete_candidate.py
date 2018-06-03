#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import requests
import sys
from requests.auth import HTTPBasicAuth

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
# Delete one candidate a time
#-------------------------------------------------------------------------------

try:
    for i in range(1, 4):
        url = URL_BASE + 'candidates/{}'.format(i)
        r = requests.delete(url, auth=('user', '123'))
        print(r.status_code)
        print(r.text)
    
except requests.exceptions.RequestException as e:
    print(e)
        
