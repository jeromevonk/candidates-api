import datetime
import json
import base64

def convertToList(info):
    ''' Create a list from base64 encoded string'''
    myList = []

    # If info is empty
    if info is None:
        return myList

    # Deserialize
    info = base64.b64decode(info).decode("utf-8")

    # Remove some characters
    info = re.sub('\]|"', '', info)
    info = re.sub('\[', '', info)

    # Conver it to a list
    myList = info.split(',')

    # If list is NoneType, create a new list
    if list is None:
        myList = []

    return myList

def dictFromDB(db_entry):
    ''' Create a dictionary containing all info drom a database entry'''
    dict = {}

    dict['experience'] = convertToList(db_entry.experience)
    dict['education']  = convertToList(db_entry.education)
    dict['tags']       = convertToList(db_entry.tags)

    # If there is a picture, get contents
    if db_entry.picture:
        with open(db_entry.picture, 'rb') as fi:
            data = fi.read()
            dict['picture'] = base64.b64encode(data).decode("utf-8")
    else:
        dict['picture'] = ""

    # The non-mandatory ones
    if db_entry.birthdate:
        # Change to format DD/MM/YYYY
        dict['birthdate'] = db_entry.birthdate.strftime("%d/%m/%Y")

    if db_entry.latitude:
        dict['latitude'] = db_entry.latitude

    if db_entry.longitude:
        dict['longitude'] = db_entry.longitude

    # Finally, the mandatory ones
    dict['name']    = db_entry.name
    dict['email']   = db_entry.email
    dict['gender']  = db_entry.gender
    dict['phone']   = db_entry.phone
    dict['address'] = db_entry.address
    dict['id']      = db_entry.id

    return dict

def convertDate(str_date):
    try:
        (day, month, year) = str_date.split('/');

        if int(day) < 1 or int(day)> 31:
            return False, 'invalid day'

        if int(month) < 1 or int(month)> 12:
            return False, 'invalid month'

        if int(year) < 1900 or int(year)> 2018:
            return False, 'invalid year'

        # Change format to datetime.date
        return datetime.date(int(year), int(month), int(day)), 'Success'

    except:
        return False, 'date should be in the format DD/MM/YYYY'

def validateCandidate(candidate):
    ''' Validate all parameters for a candidate'''

    # Name is mandatory
    if 'name' not in candidate:
        return False, 'Name is mandatory'
    elif len(candidate['name']) < 1 :
        return False, 'Invalid name'
    elif len(candidate['name']) > 80 :
        return False, 'Name maximum length is 80 characters'

    # Email is mandatory. Check for '@'
    if 'email' not in candidate:
        return False, 'Email is mandatory'
    elif candidate['email'].count('@') != 1:
        return False, 'Invalid email'
    elif candidate['email'].count('.') < 1:
        return False, 'Invalid email'
    elif len(candidate['email']) > 120 :
        return False, 'Email maximum length is 120 characters'

    # Gender is mandatory and must be (https://en.wikipedia.org/wiki/ISO/IEC_5218) either:
    # 0 = not known
    # 1 = male
    # 2 = female
    # 9 = not applicable
    if 'gender' not in candidate:
        return False, 'Gender is mandatory'
    elif candidate['gender'] not in [0, 1, 2, 9]:
        return False, 'Invalid gender. See https://en.wikipedia.org/wiki/ISO/IEC_5218'

    # Phone is mandatory and should be in the format 11912345678
    if 'phone' not in candidate:
        return False, 'Phone is mandatory'
    else:
        try:
            int(candidate['phone'])

            if len(candidate['phone']) < 10:
                return False, 'Insuficient digits. Phone should be in the format 11912345678'
            elif len(candidate['phone']) > 12:
                return False, 'Too many digits. Phone should be in the format 11912345678'
        except ValueError:
            return False, 'Phone should be in the format 11912345678 (only numbers)'


    # Address is tricky to validate. Let's consider is must be > 5 and <= 120
    if 'address' not in candidate:
        return False, 'Address is mandatory'
    elif len(candidate['address']) < 5 :
        return False, 'Address must be written with at least 5 characters'
    elif len(candidate['address']) > 120 :
        return False, 'Address maximum length is 120 characters'

    # Latitude and longitude are not mandatory, but if present should be floats
    if 'latitude' in candidate:
        if candidate['latitude'] is None:
            # Invalid, so pop this key out of the dictionary
            candidate.pop('latitude', None)
        else:
            try:
                lat = float(candidate['latitude'])

                if lat > 90.0 or lat < -90.0:
                    return False, 'Latitude must between -90 and +90'
            except ValueError:
                return False, 'Latitude should be a float'
            except:
                return False, 'Wrong type for latitude'

    if 'longitude' in candidate:
        if candidate['longitude'] is None:
            # Invalid, so pop this key out of the dictionary
            candidate.pop('longitude', None)
        else:
            try:
                lon = float(candidate['longitude'])

                if lon > 180.0 or lon < -180.0:
                    return False, 'Longitude must between -180 and +180'
            except ValueError:
                return False, 'Longitude should be a float'
            except:
                return False, 'Wrong type for longitude'

    # Birthdate is not mandatory, but if present should be in the format DD/MM/YYYY
    if 'birthdate' in candidate:
        if candidate['birthdate'] == "":
            # Invalid, so pop this key out of the dictionary
            candidate.pop('birthdate', None)
        else:
            converted, msg = convertDate(candidate['birthdate'])
            if False == converted:
                return False, 'Regarding birthdate: {}'.format(msg)
            candidate['birthdate'] = converted

    # Picture: must be either empty or base64 encoded JPEG format
    if 'picture' in candidate:
        if candidate['picture'] == "":
            pass
        else:
            try:
                image_data = base64.b64decode(candidate['picture'])
                if image_data[:2] != b'\xff\xd8':
                    return False, 'Picture should be base64 encoded JPEG format'
                else:
                    candidate['picture'] = image_data
            except:
                return False, 'Picture should be base64 encoded'

    # Experience: should be a list of strings
    if 'experience' in candidate:
        if type(candidate['experience']) != type(list()):
            return False, 'Experience must be a list'
        else:
            for item in candidate['experience']:
                if type(item) != type(str()):
                    return False, 'Experience must be a list of STRINGS'

        # Serialize the list, and then encode it to prevent SQL injection
        serialized = json.dumps(candidate['experience'])
        candidate['experience'] = base64.b64encode(serialized.encode("utf-8"))

    # Education: should be a list of dictionaries
    if 'education' in candidate:
        if type(candidate['education']) != type(list()):
            return False, 'Education must be a list'
        else:
            for entry in candidate['education']:
                if type(entry) != type(dict()):
                    return False, 'Education must be a list of DICTIONARIES'

                # Now, for every education entry, check a few things
                if 'institution' not in entry:
                    return False, 'Institution name is mandatory'
                elif entry['institution'] == "":
                    return False, 'Institution name cannot be empty'

                if 'major' not in entry:
                    return False, 'Major name is mandatory'
                elif entry['major'] == "":
                    return False, 'Major name cannot be empty'

                converted, msg = convertDate(entry['date_start'])
                if False == converted:
                    return False, 'Regarding {} date_start: {}'.format(entry['institution'], msg)
                entry['date_start'] = converted

                converted, msg = convertDate(entry['date_end'])
                if False == converted:
                    return False, 'Regarding {} date_end: {}'.format(entry['institution'], msg)
                entry['date_end'] = converted

    # Tags: should be a list of strings
    if 'tags' in candidate:
        if type(candidate['tags']) != type(list()):
            return False, 'Tags must be a list'
        else:
            for item in candidate['tags']:
                if type(item) != type(str()):
                    return False, 'Tags must be a list of STRINGS'

        # Serialize the list, and then encode it to prevent SQL injection
        serialized = json.dumps(candidate['tags'])
        candidate['tags'] = base64.b64encode(serialized.encode("utf-8"))

    return True, ""

