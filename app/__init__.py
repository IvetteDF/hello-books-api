from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# our instance of SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        #connect to the database, connects packages to central app
        app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
        # postgresql+psycopg2 is the protocol that allows u to connect to the database, use it to interepret the following str
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        # shows sql commands run
        # app.config["SQLALCHEMY_ECHO"] = True
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    # creates the bare bones of the Flask API app
    db.init_app(app)
    migrate.init_app(app, db)

    # imports the Book model
    from app.models.book import Book

    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app
