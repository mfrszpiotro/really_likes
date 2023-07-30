from flask import Flask
from app.extensions import db, ck, bs
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'h+u5-sNA2%Fr&3"y"9nQEn==rfLjfKB{$RGShJ"$2I`d&j[5-J79:RJZoQJ('
    SQLALCHEMY_DATABASE_URI = "sqlite:///reallylikes.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_BOOTSWATCH_THEME = "lux"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ck.init_app(app)
    bs.init_app(app)
    with app.app_context():
        pass
        # NOTE: deploying correctly on free render.com requires turning off db drop/init with every initialization:
        # db.drop_all()
        # db.create_all()
        # init_movies(db)

    # Register blueprints here
    from app.auth import bp as auth_bp
    from app.movies import bp as movies_bp
    from app.music import bp as music_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(movies_bp, url_prefix="/movies")
    app.register_blueprint(music_bp, url_prefix="/music")

    @app.route("/")
    def index():
        return "<h1>Testing the Flask Application Factory Pattern</h1>"

    return app
