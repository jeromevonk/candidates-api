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
# Insert a batch of candidates by sendind a zip file
#-------------------------------------------------------------------------------
print("Sending batch of candidates...")

url = URL_BASE + 'candidates/batch'
filename = 'examples/batch_candidates.zip'


#multipart_form_data = {'zipfile': (filename, open(filename, 'rb')), 'action': ('', 'store'), 'path': ('', '/path1')}
multipart_form_data = {'zipfile': (filename, open(filename, 'rb'), "multipart/form-data")}

r = requests.post(url, files = multipart_form_data)

print(r.status_code)
print(r.text)
 

