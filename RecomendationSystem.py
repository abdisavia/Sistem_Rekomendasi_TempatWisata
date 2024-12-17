from ast import dump
from .models import Users_Info, Tourism_With_Id
from math import radians, sin, cos, sqrt, atan2
import pandas as pd
from . import db
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize
import string


def age_preference(age):
    if 15 <= age <= 25:
        return ['Taman Hiburan', 'Pantai', 'Kuliner']
    elif 26 <= age <= 40:
        return ['Budaya', 'Alam', 'Kuliner']
    else:
        return ['Budaya', 'Relaksasi', 'Alam']

# Fungsi untuk menghitung jarak
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius Bumi dalam kilometer
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def recommend_places_by_age(user, max_distance=50):
    # Ambil data pengguna berdasarkan user_id
    engine = create_engine(url='mysql+pymysql://root@localhost:3306/touristattraction')
    data = pd.read_sql_query("SELECT * FROM tourism_with_id",con=engine)
    tourism_with_id = data
    user_info = Users_Info.query.filter_by(user_id = user.id).first()


    user_age = user_info.age
    user_lat = 0
    user_long= 0

    if user_info.location == "Yogyakarta" :
        user_lat, user_long = -7.801455, 110.364757  # Lokasi default (sesuaikan dengan dataset)
    elif user_info.location == "Surabaya" :
        user_lat, user_long = -7.245476, 112.738700
    elif user_info.location == "Bandung" : 
        user_lat, user_long = -6.917444, 107.618180
    elif user_info.location == "Jakarta":
        user_lat, user_long = -6.194429, 106.822589
    else :
        user_lat, user_long = -6.969341, 110.424337
        
    # Preferensi kategori berdasarkan usia
    preferred_categories = age_preference(user_age)

    # Hitung jarak tempat wisata ke lokasi user
    tourism_with_id['distance_km'] = tourism_with_id.apply(
        lambda row: haversine(user_lat, user_long, float(row['Latitude']), float(row['Longitude'])),
        axis=1
    )

    # Filter tempat wisata dalam radius tertentu dan sesuai kategori preferensi
    nearby_places = tourism_with_id[
        (tourism_with_id['distance_km'] <= max_distance) &
        (tourism_with_id['Category'].isin(preferred_categories))
    ]

    # Urutkan berdasarkan rating tertinggi
    recommendations = nearby_places.sort_values(by='Rating', ascending=False)

    recommendations = pd.DataFrame(recommendations)

    

    return recommendations[['Place_Name', 'Description', 'Category', 'Rating', 'distance_km']]


def preprocess(text):
    text = text.lower()  # Mengubah ke huruf kecil
    text = text.translate(str.maketrans('', '', string.punctuation))  # Menghapus tanda baca
    # tokens = word_tokenize(text)  # Tokenisasi
    return ' '.join(text)

def DataTransformation(data, df):
    factory = StopWordRemoverFactory()
    stopword = factory.get_stop_words()
    tfidf = TfidfVectorizer(stop_words=stopword)
    tfidf.fit(df["Description"])
    tfidf_matriks = tfidf.transform(data)
    return tfidf_matriks

def recommended_attraction(similarity_scores,df_Attrac_City):
    sim_attrac = similarity_scores.sort_values("score",ascending=False)[0:15].index
    recommended_attrac = pd.DataFrame(df_Attrac_City.iloc[sim_attrac])
    return recommended_attrac

def CBRSs(lokasi,input_des=""):
    engine = create_engine(url='mysql+pymysql://root@localhost:3306/touristattraction')

    if input_des == "":
        df = pd.read_sql_query("SELECT * FROM tourism_with_id WHERE city = '"+lokasi+"'",con=engine)
        df = pd.DataFrame(df)
        
        return df
    
    df = pd.read_sql_query("SELECT * FROM tourism_with_id",con=engine)
    
    description_transformed = DataTransformation([input_des], df)
    attraction =  df[df["City"] == lokasi].reset_index(drop=True)

    transformedData = DataTransformation(attraction["Description"], df)

    cosine_sim_Description = cosine_similarity(transformedData,description_transformed)
    cosine_sim_score = pd.DataFrame(cosine_sim_Description,columns=["score"])

    return recommended_attraction(similarity_scores=cosine_sim_score,df_Attrac_City=attraction)
