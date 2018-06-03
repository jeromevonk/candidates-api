from candidates_api import db, db_path
import os

# If database is missing, create it
if not os.path.exists(db_path):
 print("Creating database: ", db_path)
 db.create_all()