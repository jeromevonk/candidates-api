from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

import os

# Must initialize SQLAlchemy before Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

# ----------------------------------------------------------------------------------
# Our database
# ----------------------------------------------------------------------------------
class Candidate(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True)
    gender      = db.Column(db.SmallInteger)
    phone       = db.Column(db.String(12))
    address     = db.Column(db.String(120))
    latitude    = db.Column(db.Float)
    longitude   = db.Column(db.Float)
    birthdate   = db.Column(db.Date)
    picture     = db.Column(db.String(120))    
    education   = db.relationship('Education',  backref='candidate', lazy=True)
    experience  = db.relationship('Experience', backref='candidate', lazy=True)
    tags        = db.relationship('Tags',       backref='candidate', lazy=True)

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

        if 'picture' in info:
            if info['picture'] == "":
                self.picture = info['picture']
            else:
                # Do not save picture in database
                # Save it in the filesystem and store path in database
                from candidates_api import pics_path
                picture_path = os.path.join(pics_path.encode('utf-8'), "{}{}".format(self.name, '.jpg').encode('utf-8') )
                with open(picture_path, 'wb') as fo:
                    fo.write(info['picture'])

                # Store only the path in database
                self.picture = picture_path

class Education(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    institution  = db.Column(db.String(80))
    degree        = db.Column(db.String(80))
    date_start   = db.Column(db.Date)
    date_end     = db.Column(db.Date)
    description  = db.Column(db.String(300))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

    def __init__(self, cand, info):
        self.fill_parameters(cand, info)

    def update(self, cand, info):
        self.fill_parameters(cand, info)

    def fill_parameters(self, cand, info):
        self.candidate = cand
    
        if 'institution' in info:
            self.institution =  info['institution']
        
        if 'degree' in info:
            self.degree   =  info['degree']
            
        if 'date_start' in info:
            self.date_start   =  info['date_start']
            
        if 'date_end' in info:
            self.date_end   =  info['date_end']
            
        if 'description' in info:
            self.description   =  info['description']

class Experience(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    company      = db.Column(db.String(80))
    job_title    = db.Column(db.String(80))
    date_start   = db.Column(db.Date)
    date_end     = db.Column(db.Date)
    description  = db.Column(db.String(300))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

    def __init__(self, cand, info):
        self.fill_parameters(cand, info)

    def update(self, cand, info):
        self.fill_parameters(cand, info)

    def fill_parameters(self, cand, info):
        self.candidate = cand
    
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
            
class Tags(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    tag          = db.Column(db.String(80))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    
    def __init__(self, cand, info):
        self.fill_parameters(cand, info)

    def update(self, cand, info):
        self.fill_parameters(cand, info)

    def fill_parameters(self, cand, info):
        self.candidate = cand
        self.tag = info


        
class EducationSchema(ma.ModelSchema):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'date_start', 'date_end', 'description']

class ExperienceSchema(ma.ModelSchema):
    class Meta:
        model = Experience 
        fields = ['company', 'job_title', 'date_start', 'date_end', 'description']
   
class TagsSchema(ma.ModelSchema):
    class Meta:
        model = Tags
        fields = ['tag']
        
class CandidateSchema(ma.ModelSchema):
    class Meta:
        model = Candidate
        #fields = ('id', 'name', 'tags')
    #tags = ma.Nested(TagsSchema)
 
# Schema objects 
candidate_schema    = CandidateSchema()
candidates_schema   = CandidateSchema(many=True)
tag_schema          = TagsSchema()
tags_schema         = TagsSchema(many=True)
experience_schema   = ExperienceSchema()
experiences_schema  = ExperienceSchema(many=True)
education_schema    = EducationSchema()
educations_schema   = EducationSchema(many=True)
      

