#-------------------------------------------------------------------------------
# Name:        Candidates API: main file
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask_httpauth import HTTPBasicAuth

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
import logging

# My modules
import auxiliar as aux
from models import db, Candidate, Education
REQUIRED = ['name', 'email', 'gender', 'phone', 'address'] #TODO find a better way

# ----------------------------------------------------------------------------------
# Different platform configurations
# ----------------------------------------------------------------------------------
platform = "local"

if platform == "AWS":
    log_file = filename='/opt/python/log/candidates_api.log'
else:
    log_file = filename='candidates_api.log'

# Create logger
logger = logging.getLogger('candidates_api')
logger.setLevel(logging.DEBUG)

# Create file handler and formatter
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set formater and add handler
fh.setFormatter(formatter)
logger.addHandler(fh)

# ----------------------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------------------
application = Flask(__name__, static_url_path = "")
app = application #dirty trick for elastib beanstalk. see (http://blog.uptill3.com/2012/08/25/python-on-elastic-beanstalk.html)
auth = HTTPBasicAuth()

# Get path to database
db_path   = os.path.join(os.path.dirname(__file__), 'static/candidates.sqlite')
pics_path = os.path.join(os.path.dirname(__file__), 'pictures')

# Ensure pictures folder exists
if not os.path.exists(pics_path):
    os.makedirs(pics_path)

# App configuration
app.config['UPLOAD_FOLDER'] = pics_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
with app.app_context():
    db.init_app(app)
    db.create_all() 
    
   

# Password is stored as a salted SHA-256 hash
# Dictionary contains username as a key, then a tuple pair of hashed password and salt
login = {'user': ("7655812bca678302fa70d06d913e52b23f638d66a27751f459af0b44cd6ac286", "1AaBb".encode('utf-8') ) }

# ----------------------------------------------------------------------------------
# Password callback
# ----------------------------------------------------------------------------------
@auth.verify_password
def verify_password(user, password):
    try:
        hashed_passwd = login[user][0]
        salt = login[user][1]
    except:
        logger.error('User not in database. User: {} | password: {}'.format(user, password) )
        return False

    # Verify password
    if hashlib.sha256( password.encode('utf-8') + salt ).hexdigest() == hashed_passwd:
        return True

    logger.error('Authentication failed. User: {} | password: {} | hashed: {} | calculated: {}'.format(user, password, hashed_passwd, hashlib.sha256( password.encode('utf-8') + salt ).hexdigest() ) )
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
# Index page
# ----------------------------------------------------------------------------------
@app.route("/")
def start_page():
    ''' Shows the index page '''
    return render_template('view.html')

# ----------------------------------------------------------------------------------
# Get list of candidates
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v1.0/candidates', methods = ['GET'])
def get_candidates():
    ''' Get all candidate's information from database '''

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

    return jsonify( { 'candidates': to_return } )

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

    return jsonify( { 'candidate': candidate_dict } )

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
    valid, msg = aux.validateCandidate(possible_candidate)
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
        
        # Create education entries
        for entry in possible_candidate['education']:
            db_entry = Education(new_candidate.id, entry)
            db.session.add(db_entry)

        # Add to database   
        db.session.commit()
        
    except exc.IntegrityError as e:
        # Must rollback
        print(e)
        db.session().rollback()
        return jsonify({'error' : 'IntegrityError'}), 400

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        return jsonify({'error' : 'Internal error'}), 500


    # Convert from database to a dictionary
    #candidate_dict = dictFromDB(new_candidate)
    
    # Log
    logger.info("Inserted candidate with ID = {}".format(new_candidate.id))

    return jsonify( { 'inserted': possible_candidate['name'] } )

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
    try:
        list_candidates = [json.loads(myZip.read(name)) for name in myZip.namelist() if '.json' in name]
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        return jsonify({'error' : 'Invalid json files inside zip file'}), 400

    if not list_candidates:
        return jsonify({'error' : 'No valid .json files inside zip file'}), 400

    # Count
    candidates_added   = 0
    candidates_updated = 0
    invalid_candidates = 0

    for candidate in list_candidates:
        # Skip invalid candidates
        valid, msg = aux.validateCandidate(candidate)
        if valid == False:
            invalid_candidates += 1
            print("Error validating candidate {}: {}".format(candidate['name'], msg))
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
            
    # Log
    logger.info("Batch insert | Added : {}, Updated : {}, Invalid: {}".format(candidates_added, candidates_updated, invalid_candidates))

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
    valid, msg = aux.validateCandidate(to_update)
    if valid == False:
        return jsonify({'error' : msg}), 400

    # Update
    db_candidate.update(to_update)
    db.session.commit()

    # Convert from database to a dictionary
    candidate_dict = dictFromDB(db_candidate)
    
    # Log
    logger.info("Updated candidate with ID = {}".format(candidate_id))

    return jsonify( { 'updated': candidate_dict } )

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
    
    # Log
    logger.info("Deleted candidate with ID = {}".format(candidate_id))

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
    
    # Log
    logger.info("Deleted all candidates")

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

# ----------------------------------------------------------------------------------
# Initialize application
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)