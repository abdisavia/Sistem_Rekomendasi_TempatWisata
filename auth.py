from flask import Blueprint, request, redirect, url_for, flash
from . import db
from .models import Users, Users_Info
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user =  Users.query.filter_by(email=email).first()

    if not user or not check_password_hash(pw_hash=user.password, password=password):
        flash(message="Username / password salah",category="danger")
        return redirect(url_for('main.login'))
    
    login_user(user)
    return redirect(url_for("main.profile"))


@auth.route('/signup', methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    lokasi = request.form.get("location")
    usia = int(request.form.get("usia"))

    user = Users.query.filter_by(email=email).first()

    if user : 
        flash(message="email sudah digunakan harap ganti email anda",category="danger")
        return redirect(url_for("main.signup"))

    new_user = Users(email=email, password=generate_password_hash(password))

    db.session.add(new_user)
    
    new_user_id = Users.query.filter_by(email=email).first()

    new_userInfo = Users_Info(user_id=new_user_id.id,name=name,location=lokasi,age=usia)
    db.session.add(new_userInfo)
    db.session.commit()

    return redirect(url_for("main.login"))

@auth.route('/logout')
def logout():
    return 'Logout'
