import os

import sys
#sys.path.append( ".." )
from models import db
from candidates_api import db_path

# Force?
force = False

# Parse command line argument
if len(sys.argv) > 1:
    if '-f' == sys.argv[1]:
        force = True

# If database is missing, create it
if os.path.exists(db_path):
    if force == True:
        print("Existing database removed")
        os.remove(db_path)
    else:
        print("Database already exists. Try -f to force a replacement")
        exit(0)
        
    
print("Creating database: ", db_path)
db.create_all()
    