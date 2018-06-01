#-------------------------------------------------------------------------------
# Name:        Candidates API: database file
# Author:      Jerome Vergueiro Vonk
# Created:     31/05/2018
#-------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# Our database
# ----------------------------------------------------------------------------------  
class SimpleDatabase:
    def __init__(self):
        self.candidates = []

    def add_candidate(self, candidate):
        index = len(self.candidates)
        print(index)
        candidate['id'] = index
        self.candidates.append(candidate)
        return index
        
    def update_candidate(self, candidate, id):
        for entry in self.candidates:
            if entry['id'] == id:
                for key, value in entry.items():
                    # Skip 'id' key
                    if key == 'id':
                        continue
                    # Only update keys whose values doesn't match
                    if entry[key] != candidate[key]:
                       entry[key] = candidate[key]  
        
    def add_or_update(self, candidate):
        candidate_exists = False
        # If candidate already exists in the database, simply update
        for entry in self.candidates:
            if entry['name'] == candidate['name']:
                for key, value in entry.items():
                    # Skip 'id' key
                    if key == 'id':
                        continue
                
                    # Only update keys whose values doesn't match
                    if entry[key] != candidate[key]:
                       entry[key] = candidate[key]  
                
                # Flag that this candidate is already in the database
                candidate_exists = True
                
                # Break from this loop
                return self.UPDATED
                
        # Candidate not in the database, so create an entry
        if False == candidate_exists:
            self.add_candidate(candidate)
            return self.ADDED
        
    def delete_candidate(self, id):
        self.candidates[:] = [d for d in self.candidates if d.get('id') != id]
        
    def get_candidate_by_id(self, id):
        for entry in self.candidates:
            if entry['id'] == id:
                return entry
        return None
        
    def get_candidate_by_name(self, name):
        for entry in self.candidates:
            if entry['name'] == name:
                return entry
        return None
                
    def get_all_candidates(self):
        return self.candidates
     
    # Definitions 
    UPDATED = 0
    ADDED   = 1
