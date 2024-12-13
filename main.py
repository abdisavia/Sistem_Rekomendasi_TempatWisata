from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("loginForm.html")

@main.route('/profile')
def profile():
    return 'Profile'

@main.route("/home")
def home():
    return render_template("index.html")