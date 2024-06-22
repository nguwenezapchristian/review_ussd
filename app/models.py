from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Gov_institute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    gov_reviews = db.relationship('Gov_review', back_populates='institution')

class Hospitals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    hosp_reviews = db.relationship('Hosp_review', back_populates='hospital')

class Gov_review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('gov_institute.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    institution = db.relationship('Gov_institute', back_populates='gov_reviews')

class Hosp_review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    hospital = db.relationship('Hospitals', back_populates='hosp_reviews')
