from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()

admin = Admin()


class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    # Removed members relationship in favor of memberships
    # members = db.relationship('Members', backref='band', lazy=True)
    memberships = db.relationship('Memberships', backref='band', lazy=True)
    albums = db.relationship('Albums', backref='band', lazy=True)


class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    # Removed BandID
    # BandID = db.Column(db.Integer, db.ForeignKey(
    #     'band.BandID'), nullable=False)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))
    # Add relationship to memberships table
    memberships = db.relationship('Memberships', backref='member', lazy=True)


class Memberships(db.Model):
    MembershipID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey(
        'band.bandID', nullable=False))
    MemberID = db.Column(db.Integer, db.ForeignKey(
        'member.memberID', nullable=False))
    Position = db.Column(db.String(80))
    StartYear = db.Column(db.Integer)
    EndYear = db.Column(db.Integer)  # NULL if still active


class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey(
        'band.BandID'), nullable=False)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)
