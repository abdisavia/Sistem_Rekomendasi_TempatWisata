from flask import Blueprint, render_template,redirect, url_for, request
from flask_login import login_required, current_user
from .models import Users_Info, Tourism_With_Id
import pandas as pd
from . import db
from .RecomendationSystem import recommend_places_by_age, CBRSs

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for("main.login"))

@main.route('/profile', methods=["GET"])
@login_required
def profile():
    user_info = Users_Info.query.filter_by(user_id=current_user.id).first()
    nama = user_info.name
    kota = user_info.location

    heroImg=""
    if kota == "Yogyakarta":
        heroImg = "fuad-najib-xYhYTGP2tjQ-yogyakarta.jpg"
    elif kota == "Semarang":
        heroImg = "irfan-bayuaji-COs4GbeDYzk-semarang.jpg"
    elif kota == "Surabaya":
        heroImg = "kristian-tandjung-8wubO8zG8vg-surabaya.jpg"
    elif kota == "Jakarta":
        heroImg = "fiqih-alfarish-sRm2vcUprpA-unsplash-jakarta.jpg"
    else :
        heroImg = "zulfikar-arifuzzaki-o4tUA3yxuH4-bandung.jpg"

    desc = request.args.get("query_desc","")
    lokasi = request.args.get("lokasi", kota)

    rekomendasiCBRSs = CBRSs(input_des=desc, lokasi=lokasi).to_dict(orient="records")
    rekomendasi_tempatWisata = recommend_places_by_age(user=current_user).to_dict(orient="records")
    return render_template("index.html", name=nama,rekomendasi_wisata = rekomendasi_tempatWisata, heroImg=heroImg, rekomendasiCBRSs=rekomendasiCBRSs)


@main.route("/home")
def home():
    return render_template("index.html")

@main.route("/login")
def login():
    return render_template("loginForm.html")

@main.route("/signup")
def regis():
    return render_template("regisForm.html")


