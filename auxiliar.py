import datetime
import json
import base64

from models import *

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

    # Experience: should be a list of dictionaries
    if 'experience' in candidate:
        if type(candidate['experience']) != type(list()):
            return False, 'Experience must be a list'
        else:
            for entry in candidate['experience']:
                if type(entry) != type(dict()):
                    return False, 'Experience must be a list of DICTIONARIES'

                # Now, for every experience entry, check a few things
                if 'company' not in entry:
                    return False, 'Company name is mandatory'
                elif not isinstance(entry['company'], str):
                    return False, 'Company name must be a string'
                elif entry['company'] == "":
                    return False, 'Company name cannot be empty'

                if 'job_title' not in entry:
                    return False, 'Job title is mandatory'
                elif not isinstance(entry['job_title'], str):
                    return False, 'Job title must be a string'
                elif entry['job_title'] == "":
                    return False, 'Job title name cannot be empty'

                converted, msg = convertDate(entry['date_start'])
                if False == converted:
                    return False, 'Regarding {}, date_start: {}'.format(entry['company'], msg)
                entry['date_start'] = converted

                converted, msg = convertDate(entry['date_end'])
                if False == converted:
                    return False, 'Regarding {}, date_end: {}'.format(entry['company'], msg)
                entry['date_end'] = converted
                
                if 'description' in entry: 
                    if not isinstance(entry['description'], str):
                        return False, 'Experience description must be a string'

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
                elif not isinstance(entry['institution'], str):
                    return False, 'Institution must be a string'
                elif entry['institution'] == "":
                    return False, 'Institution name cannot be empty'

                if 'degree' not in entry:
                    return False, 'Degree name is mandatory'
                elif not isinstance(entry['degree'], str):
                    return False, 'Degree must be a string'
                elif entry['degree'] == "":
                    return False, 'Degree name cannot be empty'

                converted, msg = convertDate(entry['date_start'])
                if False == converted:
                    return False, 'Regarding {}, date_start: {}'.format(entry['institution'], msg)
                entry['date_start'] = converted

                converted, msg = convertDate(entry['date_end'])
                if False == converted:
                    return False, 'Regarding {}, date_end: {}'.format(entry['institution'], msg)
                entry['date_end'] = converted
                
                if 'description' in entry: 
                    if not isinstance(entry['description'], str):
                        return False, 'Education description must be a string'

    # Tags: should be a list of strings
    if 'tags' in candidate:
        if type(candidate['tags']) != type(list()):
            return False, 'Tags must be a list'
        else:
            for item in candidate['tags']:
                if type(item) != type(str()):
                    return False, 'Tags must be a list of STRINGS'

    return True, ""

def combineSchemas(to_return, id ):

    # Get the tags for that user
    tags = tags_schema.dump(Tags.query.filter_by(candidate_id=id).all()).data
    to_return['tags'] = [v for item in tags for k,v in item.items() if k == 'tag' ]

    # Get the experience for that user
    to_return['experience'] = experiences_schema.dump(Experience.query.filter_by(candidate_id = id).all()).data
    for item in to_return['experience']:
        item['date_start'] = datetime.datetime.strptime(item['date_start'], ("%Y-%m-%d")).strftime("%d/%m/%Y")
        item['date_end']   = datetime.datetime.strptime(item['date_end'],   ("%Y-%m-%d")).strftime("%d/%m/%Y")

    # Get the education for that user
    to_return['education'] = educations_schema.dump(Education.query.filter_by(candidate_id = id).all()).data
    for item in to_return['education']:
        item['date_start'] = datetime.datetime.strptime(item['date_start'], ("%Y-%m-%d")).strftime("%d/%m/%Y")
        item['date_end']   = datetime.datetime.strptime(item['date_end'],   ("%Y-%m-%d")).strftime("%d/%m/%Y")
    
    # Change birthdate
    to_return['birthdate'] = datetime.datetime.strptime(to_return['birthdate'], ("%Y-%m-%d")).strftime("%d/%m/%Y")
    
    # If there is a picture, get contents
    if 'picture' in to_return:
        if to_return['picture'] != "":
            try:
                with open(to_return['picture'].encode('utf-8'), 'rb') as fi:
                    data = fi.read()
                    to_return['picture'] = base64.b64encode(data).decode("utf-8")
            except:
                to_return['picture'] = ""          
    else:
        to_return['picture'] = ""