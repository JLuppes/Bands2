from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()

admin = Admin()


class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    # Relationship: One band has many members + albums
    members = db.relationship('Members', backref='band', lazy=True)
    albums = db.relationship('Albums', backref='band', lazy=True)


class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey(
        'bands.BandID'), nullable=False)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))


class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey(
        'bands.BandID'), nullable=False)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)
