#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import requests
import sys
import json

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

#-------------------------------------------------------------------------------
# Get list of candidates
#-------------------------------------------------------------------------------
def getAllCandidates():
    url = URL_BASE + 'candidates'

    try:
        r = requests.get(url)
        print(r.status_code)
        print(r.text)

    except requests.exceptions.RequestException as e:
        print(e)

    return r.text


if __name__ == '__main__':
    # Parse command line argument
    if len(sys.argv) > 1:
        if 'heroku' == sys.argv[1]:
            URL_BASE = HEROKU

    # Get all candidates
    data = json.loads(getAllCandidates())

    # Print some information
    print("Number of candidates in database: {}".format(len(data['candidates'])) )

    # Print the IDs
    print("IDs")
    for candidate in data['candidates']:
        print(candidate['id'])