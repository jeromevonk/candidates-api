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

# ----------------------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------------------
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# Get path to database
db_path   = os.path.join(os.path.dirname(__file__), 'candidates.sqlite')
pics_path = os.path.join(os.path.dirname(__file__), 'pictures')

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
    return render_template('index.html')

# ----------------------------------------------------------------------------------
# Get list of candidates
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates', methods = ['GET'])
def get_candidates():
    all_users = Candidate.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# ----------------------------------------------------------------------------------
# Get a single candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['GET'])
def get_candidate(candidate_id):
    
    # Make a query
    candidate = Candidate.query.get(candidate_id)
    if candidate is None:
        # Invalid id
        abort(404)
        
    # Base64 decode experience, education, tags
    candidate.experience = base64.b64decode(candidate.experience).decode("utf-8")
    candidate.education  = base64.b64decode(candidate.education).decode("utf-8")
    candidate.tags       = base64.b64decode(candidate.tags).decode("utf-8")
    
    # Get the picture
    
    return user_schema.jsonify(candidate)

# ----------------------------------------------------------------------------------
# Insert a single candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates', methods = ['POST'])
def insert():
    if not request.json:
        abort(400)

    for parameter in REQUIRED:
        if not parameter in request.json:
            print("MISSING: ", parameter)
            return jsonify({'error' : 'Missing one or more required parameters {}'.format(REQUIRED) } ), 400

    # Get parameters
    possible_candidate = {}
    possible_candidate['name']       = request.json['name']
    possible_candidate['email']      = request.json['email']
    possible_candidate['gender']     = request.json['gender']
    possible_candidate['phone']      = request.json['phone']
    possible_candidate['address']    = request.json['address']
    
    # These are not mandatory
    if 'latitude' in request.json:
        possible_candidate['latitude']   = request.json['latitude']

    if 'longitude' in request.json:
        possible_candidate['longitude']  = request.json['longitude']
    
    if 'birthdate' in request.json:
        possible_candidate['birthdate']  = request.json['birthdate']
    
    if 'picture' in request.json:
        possible_candidate['picture']  = request.json['picture']
        
    if 'experience' in request.json:
        possible_candidate['experience']  = request.json['experience']

    if 'education' in request.json:
        possible_candidate['education']  =  request.json['education']
            
    if 'tags' in request.json:
        possible_candidate['tags']  =  request.json['tags']

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

    result = user_schema.dump(new_candidate)

    return jsonify(result), 201

# ----------------------------------------------------------------------------------
# Insert a batch of candidates
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/batch', methods = ['POST'])
def batch_insert():
    # Retrieve the zip file
    received_file = request.files['zipfile']

    # Create a ZipFile object
    try:
        myZip = ZipFile(received_file)
    except BadZipfile:
        # Not a valid zipfile, abort
        abort(400)

    # Get a list of json objects contained in the ZipFile
    list_candidates = [json.loads(myZip.read(name)) for name in myZip.namelist()]

    # Count
    candidates_added   = 0
    candidates_updated = 0

    for candidate in list_candidates:

        # Skip invalid candidates
        if not validateCandidate(candidate):
            continue

        # Candidate already in database?
        db_candidate = Candidate.query.filter_by(name = candidate['name']).first()

        # Candidate does not exist in database
        if db_candidate is None:

            # Create candidate
            new_cand = Candidate(candidate)
            candidates_added   += 1

            # Add to database
            db.session.add(new_cand)
            db.session.commit()

        # Candidate exists in database
        else:

            # Update
            db_candidate.name  = candidate['name']
            db_candidate.email = candidate['email']
            db.session.commit()

            candidates_updated += 1

    return jsonify({'added' : candidates_added, 'updated' : candidates_updated}), 201

# ----------------------------------------------------------------------------------
# Update a candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['PUT'])
def update_candidate(candidate_id):

    candidate = Candidate.query.get(candidate_id)
    if candidate is None:
        # Invalid id
        abort(404)


    #TODO parameters exist?
    name  = request.json['name']
    email = request.json['email']

    candidate.email = email
    candidate.name  = name

    db.session.commit()
    return user_schema.jsonify(candidate)

# ----------------------------------------------------------------------------------
# Delete a candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['DELETE'])
@auth.login_required
def delete_candidate(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if candidate is None:
        # Invalid id
        abort(404)

    db.session.delete(candidate)
    db.session.commit()

    return jsonify( { 'result': True } )

# ----------------------------------------------------------------------------------
# Auxiliar functions
# ----------------------------------------------------------------------------------
def validateCandidate(candidate):

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
    elif candidate['gender'] not in ['0', '1', '2', '9']:
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
        try:
            print(candidate['birthdate'])
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
            return False, 'Birthdate should be in the format DD/MM/YYYY'

    # Picture: must be either empty or base64 encoded JPEG format
    if 'picture' in candidate:
        if candidate['picture'] == "":
            pass
        else:
            print("oi")
            image_data = base64.b64decode(candidate['picture'])
            if image_data[:2] != b'\xff\xd8':
                return False, 'Picture should be base64 encoded JPEG format'
            else:
                candidate['picture'] = image_data
        
    # Experience: should be a list of strings
    if 'experience' in candidate:
        if type(candidate['experience']) != type(list()):
            return False, 'Experience must be a list'
        else:
            for item in candidate['experience']:
                if type(item) != type(str()):
                    return False, 'Experience must be a list os STRINGS'
         
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
                    return False, 'Education must be a list os STRINGS'
         
        # Serialize the list, and then encode it to prevent SQL injection
        serialized = json.dumps(candidate['education'])
        candidate['education'] = base64.b64encode(serialized.encode())
    
    # Tags: should be a list of strings
        if type(candidate['tags']) != type(list()):
            return False, 'Tags must be a list'
        else:
            for item in candidate['tags']:
                if type(item) != type(str()):
                    return False, 'Tags must be a list os STRINGS'
         
        # Serialize the list, and then encode it to prevent SQL injection
        serialized = json.dumps(candidate['tags'])
        candidate['tags'] = base64.b64encode(serialized.encode())
    
    return True, ""


# ----------------------------------------------------------------------------------
# Initialize application
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)