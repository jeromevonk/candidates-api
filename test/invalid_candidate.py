#-------------------------------------------------------------------------------
# Name:        Candidates API test
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------
import requests
import sys
import pytest
import copy

#-------------------------------------------------------------------------------
# Helper function
#------------------------------------------------------------------------------- 
def postInvalidCandidate(candidate):
    try:
        r = requests.post(url, json = candidate)
        print(r.text)
        assert r.status_code == 400
        
    except requests.exceptions.RequestException as e:
        print(e)

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
# Insert invalid candidates
#-------------------------------------------------------------------------------
url = URL_BASE + 'candidates'
template = { "name" : "Jerome Vonkkkie", "picture" : "", "birthdate" : "01/02/1988", "gender" : 1,
             "email" : "vonk@gmail.com", "phone" : "11912345678", "address" : "Avenida Paulista, 1",
             "longitude": -12.75, "latitude": 45.11122, "tags" : [], "experience" : [], "education" : []}
'''
#-------------------------------------------------------------------------------
# Invalid / missing name
#------------------------------------------------------------------------------- 
print("### Inserting candidate(s) with invalid/missing name...")
invalid_name = copy.deepcopy(template)

# a) Empty
invalid_name['name'] = ''
postInvalidCandidate(invalid_name)

# b) Too big
invalid_name['name'] = 'Nome muito muito muito muito muito muito muito muito muito muito muito muito grande'
postInvalidCandidate(invalid_name)

# c) Missing name
invalid_name.pop('name', None)
postInvalidCandidate(invalid_name)

#-------------------------------------------------------------------------------
# Missing email
#-------------------------------------------------------------------------------             
print("### Inserting candidate(s) with missing email...")
invalid_email = copy.deepcopy(template)

# a) Empty
invalid_email['email'] = ''
postInvalidCandidate(invalid_email)

# b) Too big
invalid_email['email'] = 'email@muitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitomuitogrande.com'
postInvalidCandidate(invalid_email)

# c) Without '.'
invalid_email['email'] = 'email@acom'
postInvalidCandidate(invalid_email)

# d) Without '@'
invalid_email['email'] = 'emaila.com'
postInvalidCandidate(invalid_email)

# e) Missing name
invalid_email.pop('email', None)
postInvalidCandidate(invalid_email)

#-------------------------------------------------------------------------------
# Invalid / missing gender (see https://en.wikipedia.org/wiki/ISO/IEC_5218)
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid/missing gender...")
invalid_gender = copy.deepcopy(template)

# a) Invalid number
invalid_gender['gender'] = 3
postInvalidCandidate(invalid_gender)

# b) Strings are not accepted
invalid_gender['gender'] = 'Male'
postInvalidCandidate(invalid_gender)

# c) Missing gender
invalid_gender.pop('gender', None)
postInvalidCandidate(invalid_gender)


#-------------------------------------------------------------------------------
# Invalid / missing phone (format: 11912345678)
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid/missing phone...")
invalid_phone = copy.deepcopy(template)

# a) Too small
invalid_phone['phone'] = '912345678'
postInvalidCandidate(invalid_phone)

# b) Too big
invalid_phone['phone'] = '5511912345678'
postInvalidCandidate(invalid_phone)

# c) Strings are not accepted
invalid_phone['phone'] = 'nove sete cinco um meia quatro meia dois'
postInvalidCandidate(invalid_phone)

# d) Missing phone
invalid_phone.pop('phone', None)
postInvalidCandidate(invalid_phone)


#-------------------------------------------------------------------------------
# Invalid / missing address (at least 5 characters)
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid/missing address...")
invalid_address = copy.deepcopy(template)

# a) Too small
invalid_address['address'] = 'Rua'
postInvalidCandidate(invalid_address)

# b) Too big
invalid_address['address'] = 'Endereço muito muito muito muito muito muito muito muito muito muito muito muito muito muito muito muito muito muito grande'
postInvalidCandidate(invalid_address)

# c) Missing address
invalid_address.pop('address', None)
postInvalidCandidate(invalid_address)
'''
#-------------------------------------------------------------------------------
# Invalid latitude (optional, but if present should be valid )
# (see https://en.wikipedia.org/wiki/Decimal_degrees)
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid latitude...")
invalid_latitude = copy.deepcopy(template)

# a) Too small
invalid_latitude['latitude'] = -91.2
postInvalidCandidate(invalid_latitude)

# b) Too big
invalid_latitude['latitude'] = 93.2
postInvalidCandidate(invalid_latitude)

# c) Strings are not accepted
invalid_latitude['latitude'] = '45 degrees'
postInvalidCandidate(invalid_latitude)

# d) Empty
invalid_latitude['latitude'] = ''
postInvalidCandidate(invalid_latitude)

#-------------------------------------------------------------------------------
# Invalid longitude (optional, but if present should be valid )
# (see https://en.wikipedia.org/wiki/Decimal_degrees)
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid longitude...")
invalid_longitude = copy.deepcopy(template)

# a) Too small
invalid_longitude['longitude'] = -181.22
postInvalidCandidate(invalid_longitude)

# b) Too big
invalid_longitude['longitude'] = 193.21
postInvalidCandidate(invalid_longitude)

# c) Strings are not accepted
invalid_longitude['longitude'] = '45 degrees'
postInvalidCandidate(invalid_longitude)

# d) Empty
invalid_longitude['longitude'] = ''
postInvalidCandidate(invalid_longitude)

'''
#-------------------------------------------------------------------------------
# Invalid birthdate (optional, but if present should be valid )
# format is DD/MM/YYYY
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid birthdate...")
invalid_birthdate = copy.deepcopy(template)

# a) Invalid day
invalid_birthdate['birthdate'] = "00/02/1988"
postInvalidCandidate(invalid_birthdate)

# b) Invalid month
invalid_birthdate['birthdate'] = "01/13/1988"
postInvalidCandidate(invalid_birthdate)

# c) Invalid year
invalid_birthdate['birthdate'] = "03/02/2048"
postInvalidCandidate(invalid_birthdate)

# d) Invalid day of month
invalid_birthdate['birthdate'] = "30/02/1988"
postInvalidCandidate(invalid_birthdate)

#-------------------------------------------------------------------------------
# Invalid picture (optional, but if present should be valid )
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid picture...")
invalid_picture = copy.deepcopy(template)

# a) Invalid string
invalid_picture['picture'] = "Empty"
postInvalidCandidate(invalid_picture)

# b) PNG image
invalid_picture['picture'] = "ypBORw0KGg0KICAgDQpJSERSICAgByAgIAkIAiAgIHE6wrQgICABc1JHQiDPjhzpoKAgBGdBTUEgINGPC++/ve+/vSAgCXBIWXMgIA7DoCAOw4HIr8mkICAgEklEQVQYV2Pwn6+OyYbXqN26IEk3Z92oQDPMoCAgIElFTkTPgmA="
postInvalidCandidate(invalid_picture)

#-------------------------------------------------------------------------------
# Invalid experience (optional, but if present should be valid )
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid experience...")
invalid_experience = copy.deepcopy(template)

# a) Invalid string
invalid_experience['experience'] = ""
postInvalidCandidate(invalid_experience)

# b) List of non-strings
invalid_experience['experience'] = [1, 2, 3]
postInvalidCandidate(invalid_experience)

#-------------------------------------------------------------------------------
# Invalid education (optional, but if present should be valid )
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid education...")
invalid_education = copy.deepcopy(template)

# a) Invalid string
invalid_education['education'] = ""
postInvalidCandidate(invalid_education)

# b) List of non-strings
invalid_education['education'] = [1, 2, 3]
postInvalidCandidate(invalid_education)

#-------------------------------------------------------------------------------
# Invalid tags (optional, but if present should be valid )
#-------------------------------------------------------------------------------
print("### Inserting candidate(s) with invalid tags...")
invalid_tags = copy.deepcopy(template)

# a) Invalid string
invalid_tags['tags'] = ""
postInvalidCandidate(invalid_tags)

# b) List of non-strings
invalid_tags['tags'] = [1, 2, 3]
postInvalidCandidate(invalid_tags)
'''
