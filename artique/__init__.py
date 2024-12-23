from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS  # Import CORS

import config
import yaml

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Enable CORS for all routes (allow all origins)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, expose_headers=["Authorization", "Access-Token", "Refresh-Token"])

    # Alternatively, to restrict to specific origins:
    # CORS(app, origins=["http://localhost:3000"])

    # JWT
    jwt = JWTManager(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # Swagger
    with open("api_specification.yml", "r", encoding="utf-8") as file:
        api_specification = yaml.safe_load(file)
    swagger = Swagger(app, template=api_specification)

    # 블루프린트
    from .views import main_views, user_views, admin, chat, picture_views, combined_picture, db_manipulate
    app.register_blueprint(main_views.bp)
    app.register_blueprint(user_views.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(picture_views.bp)
    app.register_blueprint(combined_picture.bp)
    app.register_blueprint(db_manipulate.bp)

    return app
