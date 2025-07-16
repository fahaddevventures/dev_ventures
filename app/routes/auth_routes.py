from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("auth/login.html")

        # Lookup user by email
        user = User.query.filter_by(email=email).first()

        # Validate user exists and password matches
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.first_name}!", "success")
            return redirect(url_for("auth.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
