#-------------------------------------------------------------------------------
# Name:        Candidates API: main file
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_marshmallow import Marshmallow
from zipfile import ZipFile, BadZipfile
import json
import os
import hashlib
import datetime
import sys
import traceback
import base64
import re

# ----------------------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------------------
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# Get path to database
db_path   = os.path.join(os.path.dirname(__file__), 'candidates.sqlite')
pics_path = os.path.join(os.path.dirname(__file__), 'pictures')

# Ensure pictures folder exists
if not os.path.exists(pics_path):
    os.makedirs(pics_path)

# App configuration
app.config['UPLOAD_FOLDER'] = pics_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Must initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Password is stored as a salted SHA-256 hash
# Dictionary contains username as a key, then a tuple pair of hashed password and salt
login = {'user': ("7655812bca678302fa70d06d913e52b23f638d66a27751f459af0b44cd6ac286", "1AaBb".encode('utf-8') ) }

# ----------------------------------------------------------------------------------
# Password callbacks
# ----------------------------------------------------------------------------------
@auth.verify_password
def verify_password(user, password):
    try:
        hashed_passwd = login[user][0]
        salt = login[user][1]
    except:
        return False

    # Verify password
    if hashlib.sha256( password.encode('utf-8') + salt ).hexdigest() == hashed_passwd:
        return True

    return False

# ----------------------------------------------------------------------------------
# Error Handlers
# ----------------------------------------------------------------------------------
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)

# ----------------------------------------------------------------------------------
# Our database
# ----------------------------------------------------------------------------------
class Candidate(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(80), unique=True)
    email        = db.Column(db.String(120), unique=True)
    gender       = db.Column(db.SmallInteger)
    phone        = db.Column(db.String(12))
    address      = db.Column(db.String(120))
    latitude     = db.Column(db.Float)
    longitude    = db.Column(db.Float)
    birthdate    = db.Column(db.Date)
    picture      = db.Column(db.String(120))
    experience   = db.Column(db.String(400))
    education    = db.Column(db.String(400))
    tags         = db.Column(db.String(200))

    def __init__(self,  info):
        self.fill_parameters(info)


    def update(self,  info):
        self.fill_parameters(info)

    def fill_parameters(self, info):
        self.name       =  info['name']
        self.email      =  info['email']
        self.gender     =  info['gender']
        self.phone      =  info['phone']
        self.address    =  info['address']

        if 'latitude' in info:
            self.latitude   =  info['latitude']

        if 'longitude' in info:
            self.longitude  =  info['longitude']

        if 'birthdate' in info:
            self.birthdate  =  info['birthdate']

        if 'experience' in info:
            self.experience  =  info['experience']

        if 'education' in info:
            self.education  =  info['education']

        if 'tags' in info:
            self.tags  =  info['tags']

        if 'picture' in info:
            if info['picture'] == "":
                self.picture = info['picture']
            else:
                # Do not save picture in database
                # Save it in the filesystem and store path in database
                picture_path =  os.path.join(app.config['UPLOAD_FOLDER'], "{}{}".format(self.name, '.jpg') )
                with open(picture_path, 'wb') as fo:
                    fo.write(info['picture'])

                # Store only the path in database
                self.picture = picture_path

class CandidateSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'email', 'gender', 'phone', 'address', 'latitude', 'longitude', 'birthdate', 'picture', 'experience', 'education', 'tags')

user_schema  = CandidateSchema()
users_schema = CandidateSchema(many=True)

REQUIRED = ['name', 'email', 'gender', 'phone', 'address']

# ----------------------------------------------------------------------------------
# Index page
# ----------------------------------------------------------------------------------
@app.route("/")
def start_page():
    ''' Shows the index page '''
    return render_template('index.html')

# ----------------------------------------------------------------------------------
# Get list of candidates
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates', methods = ['GET'])
def get_candidates():
    ''' Get all candidates information from database '''

    # Query all candidates
    all_candidates = Candidate.query.all()

    # List of dictionaries to be returned
    to_return = []

    # Necessary step before sending to client
    for candidate in all_candidates:

        # Convert from database to a dictionary
        candidate_dict = dictFromDB(candidate)

        # Add to list
        to_return.append(candidate_dict)

    return jsonify(to_return)

# ----------------------------------------------------------------------------------
# Get a single candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['GET'])
def get_candidate(candidate_id):
    ''' Get a candidate information from database '''

    # Make a query
    candidate = Candidate.query.get(candidate_id)
    if candidate is None:
        # Invalid id
        return jsonify({'error' : 'No candidate with ID = {} in database'.format(candidate_id) } ), 400

    # Convert from database to a dictionary
    candidate_dict = dictFromDB(candidate)

    return jsonify(candidate_dict), 201

# ----------------------------------------------------------------------------------
# Insert a single candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates', methods = ['POST'])
def insert():
    ''' Insert a candidate on the database  '''
    if not request.json:
        abort(400)

    for parameter in REQUIRED:
        if not parameter in request.json:
            print("MISSING: ", parameter)
            return jsonify({'error' : 'Missing one or more required parameters {}'.format(REQUIRED) } ), 400

    # Get parameters from Flask's request
    possible_candidate = request_all()

    # Validate candidate
    valid, msg = validateCandidate(possible_candidate)
    if valid == False:
        return jsonify({'error' : msg}), 400

    # Is the candidate name already in the database?
    if Candidate.query.filter_by(name = possible_candidate['name']).first() is not None:
        return jsonify({'error' : 'Candidate name already in database'}), 400

    # Is the candidate email already in the database?
    if Candidate.query.filter_by(email = possible_candidate['email']).first() is not None:
        return jsonify({'error' : 'Candidate email already in database'}), 400

    try:
        # Create candidate
        new_candidate = Candidate(possible_candidate)

        # Add to database
        db.session.add(new_candidate)
        db.session.commit()

    except exc.IntegrityError as e:
        # Must rollback
        db.session().rollback()
        return jsonify({'error' : 'IntegrityError'}), 400

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        return jsonify({'error' : 'Internal error'}), 500


    # Convert from database to a dictionary
    candidate_dict = dictFromDB(new_candidate)

    return jsonify(candidate_dict), 201

# ----------------------------------------------------------------------------------
# Insert a batch of candidates
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/batch', methods = ['POST'])
def batch_insert():
    ''' Insert or updated candidates from a batch of json files '''
    # Retrieve the zip file
    received_file = request.files['zipfile']

    # Create a ZipFile object
    try:
        myZip = ZipFile(received_file)
    except BadZipfile:
        # Not a valid zipfile, abort
        return jsonify({'error' : 'Not a valid .zip file'}), 400

    # Get a list of json objects contained in the ZipFile
    list_candidates = [json.loads(myZip.read(name)) for name in myZip.namelist() if '.json' in name]

    if not list_candidates:
        return jsonify({'error' : 'No valid .json files inside zip file'}), 400

    # Count
    candidates_added   = 0
    candidates_updated = 0
    invalid_candidates = 0

    for candidate in list_candidates:
        # Skip invalid candidates
        valid, msg = validateCandidate(candidate)
        if valid == False:
            invalid_candidates += 1
            continue

        # Candidate already in database?
        db_candidate = Candidate.query.filter_by(name = candidate['name']).first()

        # Candidate does not exist in database
        if db_candidate is None:
            try:
                # Create candidate
                new_cand = Candidate(candidate)

                # Add to database
                db.session.add(new_cand)
                db.session.commit()

                candidates_added   += 1

            except exc.IntegrityError as e:
                # Must rollback
                print(e)
                db.session().rollback()
                return jsonify({'error' : 'IntegrityError'}), 400

            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                return jsonify({'error' : 'Internal error'}), 500

        # Candidate exists in database
        else:
            # Update
            db_candidate.update(candidate)
            db.session.commit()
            candidates_updated += 1

    return jsonify({'added' : candidates_added, 'updated' : candidates_updated, 'invalid': invalid_candidates}), 201

# ----------------------------------------------------------------------------------
# Update a candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['PUT'])
def update_candidate(candidate_id):
    ''' Update a candidate information in database '''

    # Query by ID
    db_candidate = Candidate.query.get(candidate_id)
    if db_candidate is None:
        # Invalid id
        return jsonify({'error' : 'No candidate with ID = {} in database'}.format(candidate_id) ), 400

    # Get parameters from Flask's request
    to_update = request_all()

    # Validate candidate
    valid, msg = validateCandidate(to_update)
    if valid == False:
        return jsonify({'error' : msg}), 400

    # Update
    db_candidate.update(to_update)
    db.session.commit()

    # Convert from database to a dictionary
    candidate_dict = dictFromDB(db_candidate)

    return jsonify(candidate_dict), 201

# ----------------------------------------------------------------------------------
# Delete a candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['DELETE'])
@auth.login_required
def delete_candidate(candidate_id):
    ''' Delete one candidate from database '''
    candidate = Candidate.query.get(candidate_id)
    if candidate is None:
        # Invalid id
        abort(404)

    db.session.delete(candidate)
    db.session.commit()

    return jsonify( { 'result': True } )


# ----------------------------------------------------------------------------------
# Delete all candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates', methods = ['DELETE'])
@auth.login_required
def delete_all():
    ''' Delete all candidates from database '''
    db.session.query(Candidate).delete()
    db.session.commit()

    return jsonify( { 'result': True } )

# ----------------------------------------------------------------------------------
# Auxiliar functions
# ----------------------------------------------------------------------------------
def request_all():
    ''' Retrieve all parameters from a specific request'''
    candidate = {}
    candidate['name']       = request.json['name']
    candidate['email']      = request.json['email']
    candidate['gender']     = request.json['gender']
    candidate['phone']      = request.json['phone']
    candidate['address']    = request.json['address']

    # These are not mandatory
    if 'latitude' in request.json:
        candidate['latitude']   = request.json['latitude']

    if 'longitude' in request.json:
        candidate['longitude']  = request.json['longitude']

    if 'birthdate' in request.json:
        candidate['birthdate']  = request.json['birthdate']

    if 'picture' in request.json:
        candidate['picture']  = request.json['picture']

    if 'experience' in request.json:
        candidate['experience']  = request.json['experience']

    if 'education' in request.json:
        candidate['education']  =  request.json['education']

    if 'tags' in request.json:
        candidate['tags']  =  request.json['tags']

    return candidate

def convertToList(info):
    ''' Create a list from base64 encoded string'''
    # Deserialize
    info = base64.b64decode(info).decode("utf-8")

    # Remove some characters
    info = re.sub('\]|"', '', info)
    info = re.sub('\[', '', info)

    # Conver it to a list
    list = info.split(',')

    return list

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
            dict['picture'] = base64.b64encode(data)

    # The non-mandatory ones
    if db_entry.birthdate:
        dict['birthdate'] = db_entry.birthdate

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
        try:
            lat = float(candidate['latitude'])

            if lat > 90.0 or lat < -90.0:
                return False, 'Latitude must between -90 and +90'
        except ValueError:
            return False, 'Latitude should be a float'

    if 'longitude' in candidate:
        try:
            lon = float(candidate['longitude'])

            if lon > 180.0 or lon < -180.0:
                return False, 'Longitude must between -180 and +180'
        except ValueError:
            return False, 'Longitude should be a float'

    # Birthdate is not mandatory, but if present should be in the format DD/MM/YYYY
    if 'birthdate' in candidate:
        if candidate['birthdate'] == "":
            # Invalid, so pop this key out of the dictionary
            candidate.pop('birthdate', None)

        else:
            try:
                (day, month, year) = candidate['birthdate'].split('/');

                if int(day) < 1 or int(day)> 31:
                    return False, 'Invalid day for birthdate'

                if int(month) < 1 or int(month)> 12:
                    return False, 'Invalid month for birthdate'

                if int(year) < 1900 or int(year)> 2018:
                    return False, 'Invalid year for birthdate'

                # Change format to datetime.date
                candidate['birthdate'] = datetime.date(int(year), int(month), int(day))

            except:
                print('except')
                return False, 'Birthdate should be in the format DD/MM/YYYY'

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
        candidate['experience'] = base64.b64encode(serialized.encode())

    # Education: should be a list of strings
    if 'education' in candidate:
        if type(candidate['education']) != type(list()):
            return False, 'Education must be a list'
        else:
            for item in candidate['education']:
                if type(item) != type(str()):
                    return False, 'Education must be a list of STRINGS'

        # Serialize the list, and then encode it to prevent SQL injection
        serialized = json.dumps(candidate['education'])
        candidate['education'] = base64.b64encode(serialized.encode())

    # Tags: should be a list of strings
        if type(candidate['tags']) != type(list()):
            return False, 'Tags must be a list'
        else:
            for item in candidate['tags']:
                if type(item) != type(str()):
                    return False, 'Tags must be a list of STRINGS'

        # Serialize the list, and then encode it to prevent SQL injection
        serialized = json.dumps(candidate['tags'])
        candidate['tags'] = base64.b64encode(serialized.encode())

    return True, ""


# ----------------------------------------------------------------------------------
# Initialize application
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)