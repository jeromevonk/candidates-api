#-------------------------------------------------------------------------------
# Name:        Candidates API
# Author:      Jerome Vergueiro Vonk
# Created:     30/05/2018
#-------------------------------------------------------------------------------

import requests
 
URL_BASE = 'http://localhost:5000/candidates/api/v1.0/'
 
#-------------------------------------------------------------------------------
# Get list of candidates
#-------------------------------------------------------------------------------
url = URL_BASE + 'candidates'
r = requests.get(url)
print(r.status_code)
print(r.text) 
