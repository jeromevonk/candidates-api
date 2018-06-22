#-------------------------------------------------------------------------------
# Name:        Candidates API: main file
# Author:      Jerome Vergueiro Vonk
# Created:     01/06/2018
#-------------------------------------------------------------------------------

from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import exc

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
from models import *
REQUIRED = ['name', 'email', 'gender', 'phone', 'address', 'education', 'experience', 'tags' ] #TODO find a better way

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
fh = logging.FileHandler(log_file, encoding = "UTF-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set formater and add handler
fh.setFormatter(formatter)
logger.addHandler(fh)

# ----------------------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------------------
logger.info("App started at {}".format(datetime.datetime.now()))
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
@app.route('/candidates/api/v2.0/candidates', methods = ['GET'])
def get_candidates():
    ''' Get all candidate's information from database '''

    # Query all candidates
    all_candidates = Candidate.query.all()

    # List of dictionaries to be returned
    to_return = []

    # Necessary step before sending to client
    for candidate in all_candidates:

        # Temporary: mount response
        candidate_full = candidate_schema.dump(candidate).data
        aux.combineSchemas(candidate_full, candidate.id)

        # Add to list
        to_return.append(candidate_full)

    return jsonify( { 'candidates': to_return } )

# ----------------------------------------------------------------------------------
# Get a single candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v2.0/candidates/<int:candidate_id>', methods = ['GET'])
def get_candidate(candidate_id):
    ''' Get a candidate information from database '''

    # Make a query
    candidate = Candidate.query.get(candidate_id)
    if candidate is None:
        # Invalid id
        return jsonify({'error' : 'No candidate with ID = {} in database'.format(candidate_id) } ), 400
    
    # Temporary: mount response
    candidate_full = candidate_schema.dump(candidate).data
    aux.combineSchemas(candidate_full, candidate.id)

    return jsonify( { 'candidate': candidate_full } )

# ----------------------------------------------------------------------------------
# Insert a single candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v2.0/candidates', methods = ['POST'])
def insert():
    ''' Insert a candidate on the database  '''
    if not request.json:
        abort(400)

    for parameter in REQUIRED:
        if not parameter in request.json:
            logger.error('Missing parameter: {}'.format(parameter))
            return jsonify({'error' : 'Missing required parameter: {}'.format(parameter) } ), 400

    # Get parameters from Flask's request
    possible_candidate = request_all()

    # Validate candidate
    valid, msg = aux.validateCandidate(possible_candidate)
    if valid == False:
        return jsonify({'error' : msg}), 400

    # Is the candidate name already in the database?
    if Candidate.query.filter_by(name = possible_candidate['name']).first() is not None:
        logger.error("Candidate named '{}' already in database".format(possible_candidate['name']) )
        return jsonify({'error' : 'Candidate name already in database'}), 400

    # Is the candidate email already in the database?
    if Candidate.query.filter_by(email = possible_candidate['email']).first() is not None:
        logger.error("Candidate with email '{}' already in database".format(possible_candidate['email']) )
        return jsonify({'error' : 'Candidate email already in database'}), 400

    try:
        logger.info(possible_candidate)
        db_candidate = insert_on_database(possible_candidate)

    except exc.IntegrityError as e:
        # Must rollback
        print(e)
        db.session().rollback()
        return jsonify({'error' : 'IntegrityError'}), 400

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        return jsonify({'error' : 'Internal error'}), 500

    # Log
    logger.info("Inserted candidate with ID = {}".format(db_candidate.id))

    # Temporary: mount response
    candidate_full = candidate_schema.dump(db_candidate).data
    aux.combineSchemas(candidate_full, db_candidate.id )

    return jsonify( { 'inserted': candidate_full } )

# ----------------------------------------------------------------------------------
# Insert a batch of candidates
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v2.0/candidates/batch', methods = ['POST'])
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
        return jsonify({'error' : 'At least one invalid json file inside zip file'}), 400

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
            print()
            logger.info("Error validating candidate {}: {}".format(candidate['name'], msg))
            continue

        # Candidate already in database?
        db_candidate = Candidate.query.filter_by(name = candidate['name']).first()
        
        try:
            # Candidate does not exist in database
            if db_candidate is None:
                # Insert
                insert_on_database(candidate)
                candidates_added += 1

            # Candidate exists in database
            else:
                # Update
                update_on_database(db_candidate, candidate)
                candidates_updated += 1
                
        except exc.IntegrityError as e:
            # Must rollback
            print(e)
            db.session().rollback()
            return jsonify({'error' : 'IntegrityError'}), 400

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return jsonify({'error' : 'Internal error'}), 500

    # Log
    logger.info("Batch insert | Added : {}, Updated : {}, Invalid: {}".format(candidates_added, candidates_updated, invalid_candidates))

    return jsonify({'added' : candidates_added, 'updated' : candidates_updated, 'invalid': invalid_candidates}), 201

# ----------------------------------------------------------------------------------
# Update a candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v2.0/candidates/<int:candidate_id>', methods = ['PUT'])
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

    try:
        update_on_database(db_candidate, to_update)
        
    except exc.IntegrityError as e:
        # Must rollback
        print(e)
        db.session().rollback()
        return jsonify({'error' : 'IntegrityError'}), 400

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        return jsonify({'error' : 'Internal error'}), 500


    # Temporary: mount response
    candidate_full = candidate_schema.dump(db_candidate).data
    aux.combineSchemas(candidate_full, db_candidate.id )

    # Log
    logger.info("Updated candidate with ID = {}".format(candidate_id))

    return jsonify( { 'updated': candidate_full } )

# ----------------------------------------------------------------------------------
# Delete a candidate
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v2.0/candidates/<int:candidate_id>', methods = ['DELETE'])
@auth.login_required
def delete_candidate(candidate_id):
    ''' Delete one candidate from database '''
    candidate = Candidate.query.get(candidate_id)
    if candidate is None:
        return jsonify({'error' : 'No candidate with id = {} on database'.format(candidate_id)}), 404

    # Delete
    db.session.query(Tags).filter_by(candidate_id = candidate_id).delete()
    db.session.query(Experience).filter_by(candidate_id = candidate_id).delete()
    db.session.query(Education).filter_by(candidate_id = candidate_id).delete()
    db.session.query(Candidate).filter_by(id = candidate_id).delete()

    db.session.commit()

    # Log
    logger.info("Deleted candidate with ID = {}".format(candidate_id))

    return jsonify( { 'result': True } )

# ----------------------------------------------------------------------------------
# Delete all candidates
# ----------------------------------------------------------------------------------
@app.route('/candidates/api/v2.0/candidates', methods = ['DELETE'])
@auth.login_required
def delete_all():
    ''' Delete all candidates from database '''
    db.session.query(Tags).delete()
    db.session.query(Experience).delete()
    db.session.query(Education).delete()
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

def insert_on_database(candidate):

    # Create candidate
    db_candidate = Candidate(candidate)

    # Add to database
    db.session.add(db_candidate)

    # Create education entries
    for entry in candidate['education']:
        db_entry = Education(db_candidate, entry)
        db.session.add(db_entry)

    # Create experience entries
    for entry in candidate['experience']:
        db_entry = Experience(db_candidate, entry)
        db.session.add(db_entry)

    # Create tag entries
    for entry in candidate['tags']:
        db_entry = Tags(db_candidate, entry)
        db.session.add(db_entry)

    # Add to database
    db.session.commit()
    
    return db_candidate

def update_on_database(db_candidate, to_update):
    # Update 'Candidate' table
    db_candidate.update(to_update)
    
    # 'Education': erase existing entries and add the new ones
    db.session.query(Education).filter_by(candidate_id = db_candidate.id).delete()
    for entry in to_update['education']:
        db_entry = Education(db_candidate, entry)
        db.session.add(db_entry)

    # 'Experience': erase existing entries and add the new ones
    db.session.query(Experience).filter_by(candidate_id = db_candidate.id).delete()
    for entry in to_update['experience']:
        db_entry = Experience(db_candidate, entry)
        db.session.add(db_entry)

    # 'Tags': erase existing entries and add the new ones
    db.session.query(Tags).filter_by(candidate_id = db_candidate.id).delete()
    for entry in to_update['tags']:
        db_entry = Tags(db_candidate, entry)
        db.session.add(db_entry)

    # Add to database
    db.session.commit()
      
# ----------------------------------------------------------------------------------
# Initialize application
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)