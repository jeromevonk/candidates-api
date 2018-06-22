#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import requests
import sys

#-------------------------------------------------------------------------------
# Helper function
#------------------------------------------------------------------------------- 
def sendBatch(filename, multipart_form_data):
    try:
        r = requests.post(url, files = multipart_form_data)
        print(r.status_code)
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
# Insert a batch of candidates by sendind a zip file
#-------------------------------------------------------------------------------
print("Sending batch of candidates...")

url = URL_BASE + 'candidates/batch'

# Valid batch
filename = 'examples/zips/_batch_candidates.zip'
multipart_form_data = {'zipfile': (filename, open(filename, 'rb'), "multipart/form-data")}
sendBatch(filename, multipart_form_data)

# Valid zipfile with invalid document inside
filename = 'examples/zips/_wrong_format.zip'
multipart_form_data = {'zipfile': (filename, open(filename, 'rb'), "multipart/form-data")}
sendBatch(filename, multipart_form_data)

# Invalid zipfile (different algorithm, 7zip)
filename = 'examples/zips/_not_zip.7z'
multipart_form_data = {'zipfile': (filename, open(filename, 'rb'), "multipart/form-data")}
sendBatch(filename, multipart_form_data)

# One bad document inside zipfile
filename = 'examples/zips/_one_bad_document.zip'
multipart_form_data = {'zipfile': (filename, open(filename, 'rb'), "multipart/form-data")}
sendBatch(filename, multipart_form_data)

# Invalid json files inside
filename = 'examples/zips/_invalid.zip'
multipart_form_data = {'zipfile': (filename, open(filename, 'rb'), "multipart/form-data")}
sendBatch(filename, multipart_form_data)

# Missing required information
filename = 'examples/zips/_missing_required.zip'
multipart_form_data = {'zipfile': (filename, open(filename, 'rb'), "multipart/form-data")}
sendBatch(filename, multipart_form_data)