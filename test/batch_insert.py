#-------------------------------------------------------------------------------
# Name:        Candidates API
# Author:      Jerome Vergueiro Vonk
# Created:     30/05/2018
#-------------------------------------------------------------------------------

import requests
 
URL_BASE = 'http://localhost:5000/candidates/api/v1.0/'
 
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
 

