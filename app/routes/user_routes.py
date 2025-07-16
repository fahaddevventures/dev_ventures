from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.user import User
from app.enums import UserRoleEnum
from werkzeug.security import generate_password_hash
from flask_login import login_required

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/add", methods=["GET", "POST"])
# @login_required
def add_user():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        contact = request.form.get("contact")
        role = request.form.get("role")
        profile_image_url = request.form.get("profile_image_url") or "None"

        # Basic validation
        if not all([first_name, last_name, email, password, contact, role]):
            flash("All fields are required.", "danger")
            return render_template("users/add_user.html")

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return render_template("users/add_user.html")

        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=generate_password_hash(password),
                contact=contact,
                role=UserRoleEnum[role],
                profile_image_url=profile_image_url,
            )
            db.session.add(user)
            db.session.commit()
            flash("User added successfully!", "success")
            return redirect(url_for("user.add_user"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while adding the user.", "danger")

    return render_template("users/add_user.html")
