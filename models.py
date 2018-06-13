from flask_sqlalchemy import SQLAlchemy

# Must initialize SQLAlchemy before Marshmallow
db = SQLAlchemy()
#ma = Marshmallow()

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
    tags         = db.Column(db.String(200))
    experience   = db.Column(db.String(400))
    
    education    = db.relationship('Education', backref='candidate', lazy=True)
    
    '''
    education    = db.Column(db.String(400))
    '''

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

        if 'tags' in info:
            self.tags  =  info['tags']

        if 'picture' in info:
            if info['picture'] == "":
                self.picture = info['picture']
            else:
                # Do not save picture in database
                # Save it in the filesystem and store path in database
                picture_path = os.path.join(app.config['UPLOAD_FOLDER'].encode('utf-8'), "{}{}".format(self.name, '.jpg').encode('utf-8') )
                with open(picture_path, 'wb') as fo:
                    fo.write(info['picture'])

                # Store only the path in database
                self.picture = picture_path
'''
class CandidateSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'email', 'gender', 'phone', 'address', 'latitude', 'longitude', 'birthdate', 'picture', 'experience', 'education', 'tags')

user_schema  = CandidateSchema()
users_schema = CandidateSchema(many=True)'''

class Education(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    institution  = db.Column(db.String(80))
    major        = db.Column(db.String(80))
    date_start   = db.Column(db.Date)
    date_end     = db.Column(db.Date)
    description  = db.Column(db.String(300))

    def __init__(self, cand_id, info):
        self.fill_parameters(cand_id, info)

    def update(self, cand_id, info):
        self.fill_parameters(cand_id, info)

    def fill_parameters(self, cand_id, info):
        self.candidate_id = cand_id
    
        if 'institution' in info:
            self.institution =  info['institution']
        
        if 'major' in info:
            self.major   =  info['major']
            
        if 'date_start' in info:
            self.date_start   =  info['date_start']
            
        if 'date_end' in info:
            self.date_end   =  info['date_end']
            
        if 'description' in info:
            self.description   =  info['description']
            
            
class Experience(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    company      = db.Column(db.String(80))
    job_title    = db.Column(db.String(80))
    date_start   = db.Column(db.Date)
    date_end     = db.Column(db.Date)
    description  = db.Column(db.String(300))

    def __init__(self, cand_id, info):
        self.fill_parameters(cand_id, info)

    def update(self, cand_id, info):
        self.fill_parameters(cand_id, info)

    def fill_parameters(self, cand_id, info):
        self.candidate_id = cand_id
    
        if 'company' in info:
            self.company =  info['company']
        
        if 'job_title' in info:
            self.job_title   =  info['job_title']
            
        if 'date_start' in info:
            self.date_start   =  info['date_start']
            
        if 'date_end' in info:
            self.date_end   =  info['date_end']
            
        if 'description' in info:
            self.description   =  info['description']
