from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Create our Flask app object
app = Flask(__name__)

# Configure the flask app instance
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(CONFIG_TYPE)

# Create an instance of SQLAlchemy as our db object
db = SQLAlchemy(app)

# ==========================
# DATABASE MODELS
# ==========================

# Set up our database models here

# ==========================
# ROUTES
# ==========================

# Home page view
@app.route('/')
def index():
    return render_template('index.html')


# Create DB and tables if they don't exist
with app.app_context():
    db.create_all()

# Run the app if this file is launched via Python (instead of flask run --debug)
if __name__ == '__main__':
    app.run(debug=True)
