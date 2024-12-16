from flask import Blueprint, request, redirect, url_for, flash
from . import db
from .models import Users
from flask_bcrypt import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user =  Users.query.filter_by(email=email).first()

    if not user or not check_password_hash(pw_hash=user.password, password=password):
        flash("Username / password salah")
        return redirect(url_for('auth.login'))
    
    return 'Login'


@auth.route('/signup')
def signup():

    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'