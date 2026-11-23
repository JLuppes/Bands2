from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from model import db, Bands, Members, Albums, admin
from flask_admin.contrib.sqla import ModelView
import os

# Create our Flask app object
app = Flask(__name__)

# Configure the flask app instance
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(CONFIG_TYPE)

# Create an instance of SQLAlchemy as our db object
db.init_app(app)

admin.init_app(app)
admin.add_view(ModelView(Bands, db.session, category="Bands"))
admin.add_view(ModelView(Members, db.session, category="Members"))
admin.add_view(ModelView(Albums, db.session, category="Albums"))


# ==========================
# ROUTES
# ==========================

# Home page view


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bands/view')
def view_by_band():
    bands = Bands.query.all()
    return render_template('display_by_band.html', bands=bands)


@app.route('/bands/view/<int:id>')
def view_band(id):
    band = Bands.query.get_or_404(id)
    return render_template('view_band.html', band=band)


@app.route('/bands/add', methods=['GET', 'POST'])
def add_band():
    if request.method == 'POST':
        new_band = Bands(
            BandName=request.form['bandname'],
            FormedYear=request.form['formedyear'],
            HomeLocation=request.form['homelocation']
        )
        db.session.add(new_band)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_band.html')


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    bands = Bands.query.all()  # Students see querying with relationships
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form['membername'],
            MainPosition=request.form['mainposition'],
            BandID=request.form['bandid']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html', bands=bands)

@app.route('/members/view')
def view_by_members():
    members = Members.query.all()
    memberships = memberships.query.all()
    return render_template('display_by_member.html', members=members, memberships=memberships)

@app.route('/members/view/<int:id>')
def view_member(id):
    member = Members.query.get_or_404(id)
    memberships = memberships.query.all()
    return render_template('view_member.html', member=member, memberships=memberships)


@app.route('/albums/add', methods=['GET', 'POST'])
def add_album():
    bands = Bands.query.all()
    if request.method == 'POST':
        band_ids = request.form.getlist('bandids')
        if not band_ids:
            error = 'Select at least one band for this album.'
            return render_template('add_album.html', bands=bands, error=error)

        new_album = Albums(
            AlbumTitle=request.form['albumtitle'],
            ReleaseYear=request.form['releaseyear']
        )
        for band_id in set(band_ids):
            band = db.session.get(Bands, int(band_id))
            if band:
                new_album.bands.append(band)
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_album.html', bands=bands)


@app.route('/bands/edit/<int:band_id>')
def edit_band(band_id):
    band = Bands.query.get_or_404(band_id)
    if request.method == 'POST':
        try:
            band.Name = request.form.get('bandname')
            band.FormedYear = request.form.get('formedyear')
            band.HomeLocation = request.form.get('homelocation')
            db.session.add(band)
            db.session.commit()
            return redirect(url_for('view_by_band'))

        except Exception as e:
            db.session.rollback()
            error = f"Error updating band: {e}"
            return render_template('edit_band.html', band=band, error=error)

@app.route('/bands/delete/int:band_id')
def delete_band(band_id):
    band = Bands.query.get_or_404(band_id)

    try:
        db.session.delete(band)
        db.session.commit()
        return redirect(url_for('view_by_band'))
    except Exception as e: 
        db.session.rollback()
        error = f"Error deleting band: {e}"
        return redirect(url_for('view_by_band'))

# Create DB and tables if they don't exist
with app.app_context():
    db.create_all()

# Run the app if this file is launched via Python (instead of flask run --debug)
if __name__ == '__main__':
    app.run(debug=True)
