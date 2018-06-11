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
AWS    = 'http://candidates-api.sa-east-1.elasticbeanstalk.com/candidates/api/v1.0/'

# Default to localhost
URL_BASE = LOCAL

# Default to candidate ID = 1
candidate_id = 1

# Parse command line arguments
if len(sys.argv) > 1:
    try:
        # Get candidate ID
        candidate_id = int(sys.argv[1])
    except:
        pass
        
        
if len(sys.argv) > 2:
    if 'heroku' == sys.argv[1]:
        URL_BASE = HEROKU
    if 'aws' == sys.argv[1]:
        URL_BASE = AWS      
 
#-------------------------------------------------------------------------------
# Get list of candidates
#-------------------------------------------------------------------------------
url = URL_BASE + 'candidates/{}'.format(candidate_id) 

try:
    r = requests.get(url)
    print(r.status_code)
    print(r.text)
except requests.exceptions.RequestException as e:
    print(e)
