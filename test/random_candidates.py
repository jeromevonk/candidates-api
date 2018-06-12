#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

import sys
import requests
import base64
import random
import names
from random_words import RandomWords
from random_words import RandomNicknames
from faker import Faker

#-------------------------------------------------------------------------------
# Helper function
#------------------------------------------------------------------------------- 
def postCandidate(candidate):
    try:
        r = requests.post(url, json = candidate)
        print(r.status_code)
        if r.status_code not in range(200, 300):
            print(r.text)
        
    except requests.exceptions.RequestException as e:
        print(e)

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
# Insert one candidate with missing information
#-------------------------------------------------------------------------------
url = URL_BASE + 'candidates'
candidate = { "name" : "", "picture" : "", "birthdate" : "", "gender" : 1,
	          "email" : "@random.com", "phone" : "", "address" : "",
              "longitude": 0, "latitude": 0, "tags" : [], "experience" : [], "education" : []
            }
              
print("### Inserting candidates...") 

# Get objects
rw = RandomWords()  
rn = RandomNicknames()
fake = Faker('pt_BR')

for i in range(20):
    
    # Generate a name and set gender
    if i%2 == 0:
        candidate['gender'] = 1
        candidate['name']  = names.get_full_name(gender='male')
    else:
        candidate['gender'] = 2
        candidate['name'] = names.get_full_name(gender='female')
        
    # Set the email according to the name
    #candidate['email'] = candidate['name'].split()[0].lower() + "@" + rw.random_word() + ".com"
    candidate['email'] = fake.ascii_safe_email()
    
    # Random latitude and longitude
    candidate['latitude']  = round(random.uniform(-90.0, 90.0), 6)
    candidate['longitude'] = round(random.uniform(-180.0, 180.0), 6)
    
    # Random education
    candidate['education'] = rn.random_nicks(count = 2)
    
    # Random experience
    candidate['experience'] = rw.random_words(count = 2)
    
    # Random tags
    candidate['tags'] = rw.random_words(count = 2)
    
    # Random address
    candidate['address'] = fake.address()
    
    # Fake phone
    candidate['phone'] = fake.msisdn()[2:]
    
    # Fake birthdate
    candidate['birthdate'] = "{}/{}/19{}".format(random.randint(1, 28), random.randint(1, 12), random.randint(10, 99) ) 
    
    # Post
    postCandidate(candidate)