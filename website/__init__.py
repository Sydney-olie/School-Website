from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()



db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(__file__), "../instance", DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    from .views import views
    from .auth import auth
    from .contact import contact_bp
    from .input import input

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(contact_bp, url_prefix='/')
    app.register_blueprint(input, url_prefix='/')
    
    db.init_app(app)
    

    from .models import User  # make sure models.py has a User model defined

    create_database(app)

    return app


def create_database(app):
    db_path = os.path.join(os.path.dirname(__file__), "../instance", DB_NAME)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # create folder if missing

    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print('✅ Database created successfully!')
    else:
        print('⚠️ Database already exists.')

