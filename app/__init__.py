import os
import time
from flask import Flask
from flasgger import Swagger
from sqlalchemy.exc import OperationalError

from app.database import db, migrate

def create_app():
    app = Flask(__name__)
    
    database_url = os.environ.get("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:postgres@db:5432/users_db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    swagger = Swagger(app, template={
        "info": {
            "title": "User Management API",
            "description": "API для керування користувачами",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    })
    
    from app.routes import user_bp
    app.register_blueprint(user_bp)
    
    with app.app_context():
        retry_count = 5
        while retry_count > 0:
            try:
                db.create_all()
                print("Database tables created successfully!")
                break
            except OperationalError as e:
                retry_count -= 1
                print(f"Database connection failed: {e}. Retrying in 5 seconds... ({retry_count} attempts left)")
                if retry_count == 0:
                    print("Failed to connect to the database after multiple attempts.")
                time.sleep(5)
    
    return app
