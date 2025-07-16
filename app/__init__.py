from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from app.config import Config
from app.extensions import db, migrate

from app.models.user import User

from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates')  # ✅ Keep only this one
    app.config.from_object(Config)

    
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    # ✅ This renders template directly, no url_for()
    @app.route("/", methods=["GET"])
    def home():
        return redirect(url_for('auth.login'))  # ✅ redirect to login page

    
    # from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
