from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    institution = db.relationship('Institution', back_populates='reviews')

Institution.reviews = db.relationship('Review', order_by=Review.id, back_populates='institution')