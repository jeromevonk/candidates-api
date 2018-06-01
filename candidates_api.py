#-------------------------------------------------------------------------------
# Name:        Candidates API: main file
# Author:      Jerome Vergueiro Vonk
# Created:     30/05/2018
#-------------------------------------------------------------------------------

from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from zipfile import ZipFile, BadZipfile
import json
from database import Database

app = Flask(__name__, static_url_path = "")

# ----------------------------------------------------------------------------------
# Error Handlers
# ----------------------------------------------------------------------------------  
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# ----------------------------------------------------------------------------------
# Our database
# ----------------------------------------------------------------------------------       
db = Database()
 
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
    candidate_list = db.get_all_candidates()
    return jsonify({'total': len(candidate_list),'candidates': candidate_list})
    
    
# ----------------------------------------------------------------------------------
# Get a single candidate
# ----------------------------------------------------------------------------------     
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['GET'])
def get_candidate(candidate_id):
    candidate = db.get_candidate_by_id(candidate_id)
    if candidate is None:
        abort(404)
    
    return jsonify({'candidate': candidate})
 
# ----------------------------------------------------------------------------------
# Insert a single candidate
# ----------------------------------------------------------------------------------     
@app.route('/candidates/api/v1.0/candidates', methods = ['POST'])
def insert():
    if not request.json:
        abort(400)
    if not 'name' in request.json or not 'email' in request.json:
        abort(400)
        
    # Candidate already in database?
    if db.get_candidate_by_name(request.json['name']) is not None:
        # Client should call update
        abort(400)
    
    candidate = {
        'name': request.json['name'],
        'picture': request.json.get('picture', ""),
        'birthdate': request.json.get('birthdate', ""),
        'gender': request.json.get('gender', ""),
        'email': request.json.get('email', ""),
        'phone': request.json.get('phone', ""),
        'address': request.json.get('address', ""),
        'longitude': request.json.get('longitude', ""),
        'latitude': request.json.get('latitude', ""),
        'tags': request.json.get('latitude', ""),
        'experience': request.json.get('latitude', ""),
        'education': request.json.get('latitude', "")
    }
    
    # Add to database
    id = db.add_candidate(candidate)
    
    # Add id to the candidate, so we can return to client
    candidate['id'] = id
    
    return jsonify({'inserted': candidate}), 201 
    
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
        
        # Add or update candidate in database  
        ret = db.add_or_update(candidate)
            
        if ret == Database.UPDATED:
           candidates_updated += 1 
        else:
           candidates_added   += 1
        
    return jsonify({'added' : candidates_added, 'updated' : candidates_updated}), 201

# ----------------------------------------------------------------------------------
# Update a candidate
# ----------------------------------------------------------------------------------     
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['PUT'])
def update_candidate(candidate_id):
    if not request.json:
        abort(400)
    if not 'name' in request.json or not 'email' in request.json:
        abort(400)
        
    # Candidate already in database?
    if db.get_candidate_by_name(request.json['name']) is None:
        # Client should call insert
        abort(400)
        
    candidate = {
        'name': request.json['name'],
        'picture': request.json.get('picture', ""),
        'birthdate': request.json.get('birthdate', ""),
        'gender': request.json.get('gender', ""),
        'email': request.json.get('email', ""),
        'phone': request.json.get('phone', ""),
        'address': request.json.get('address', ""),
        'longitude': request.json.get('longitude', ""),
        'latitude': request.json.get('latitude', ""),
        'tags': request.json.get('tags', ""),
        'experience': request.json.get('experience', ""),
        'education': request.json.get('education', "")
    }
    
    # Add to database
    id = db.update_candidate(candidate, candidate_id)
    
    return jsonify({'updated': candidate}), 201 
    
# ----------------------------------------------------------------------------------
# Delete a candidate
# ---------------------------------------------------------------------------------- 
@app.route('/candidates/api/v1.0/candidates/<int:candidate_id>', methods = ['DELETE'])
def delete_candidate(candidate_id):
    print('delete_candidate')
    print(candidate_id)
    candidate = db.get_candidate_by_id(candidate_id)
    if candidate is None:
        abort(404)
    
    # Remove from database
    db.delete_candidate(candidate_id)
    
    return jsonify( { 'result': True } )
    
# ----------------------------------------------------------------------------------
# Auxiliar functions
# ----------------------------------------------------------------------------------  
def validateCandidate(candidate):
    if 'name' not in candidate:
        return False
    if 'email' not in candidate:
        return False
    
    return True

    
# ----------------------------------------------------------------------------------
# Initialize application
# ----------------------------------------------------------------------------------     
if __name__ == '__main__':
    app.run(debug = True)