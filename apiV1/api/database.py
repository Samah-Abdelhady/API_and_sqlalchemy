from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def setup_db(app):
    db.init_app(app)
    migrate = Migrate(app, db)