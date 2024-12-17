from . import db
from flask_login import UserMixin
from datetime import datetime
import csv

class Tourism_Rating(db.Model):
    __tablename__ = "tourism_rating"

    # User_Id,Place_Id,Place_Ratings
    place_ratings_id = db.Column(db.Integer, primary_key = True)
    User_Id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Place_Id = db.Column(db.Integer, db.ForeignKey('tourism_with_id.place_id'), nullable=False)
    Place_Ratings = db.Column(db.Integer, nullable=True)
    
    # Relasi
    user = db.relationship('Users', backref='tourism_ratings')
    tourism_place = db.relationship('Tourism_With_Id', backref='tourism_ratings')

    @staticmethod
    def insert_from_csv(file_path):
        """
        Fungsi untuk memasukkan data dari file CSV ke dalam tabel User.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)  # Membaca CSV sebagai dictionary
                for row in reader:
                    # Pastikan data sesuai kolom di model User 

                    user = Tourism_Rating(
                        User_Id=int(row['User_Id']),
                        Place_Id=row['Place_Id'],
                        Place_Ratings=row['Place_Ratings']
                    )
                    db.session.add(user)  # Menambahkan ke sesi database

                db.session.commit()  # Commit transaksi
                print("Data berhasil dimasukkan ke dalam database!")

        except Exception as e:
            db.session.rollback()  # Rollback jika terjadi error
            print(f"Error saat memasukkan data: {e}")
    #digunkan untuk mencetak string setiap kali membuat elemen baru
    def __repr__(self):
        return '<Users %r>' % self.id


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    users_info = db.relationship('Users_Info', backref='users', uselist=False, cascade="all, delete")
    
    @staticmethod
    def insert_from_csv(file_path):
        """
        Fungsi untuk memasukkan data dari file CSV ke dalam tabel User.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)  # Membaca CSV sebagai dictionary
                for row in reader:
                    # Pastikan data sesuai kolom di model User
                    user = Users(
                        id=int(row['id']),
                        email=row['email'],
                        password=row['password'],
                        date_created = row["date_created"]
                    )
                    db.session.add(user)  # Menambahkan ke sesi database

                db.session.commit()  # Commit transaksi
                print("Data berhasil dimasukkan ke dalam database!")

        except Exception as e:
            db.session.rollback()  # Rollback jika terjadi error
            print(f"Error saat memasukkan data: {e}")


    #digunkan untuk mencetak string setiap kali membuat elemen baru
    def __repr__(self):
        return '<Users %r>' % self.id

class Users_Info(UserMixin, db.Model):
    __tablename__ = "users_info"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key ke User.id
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    @staticmethod
    def insert_from_csv(file_path):
        """
        Fungsi untuk memasukkan data dari file CSV ke dalam tabel User.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)  # Membaca CSV sebagai dictionary
                for row in reader:
                    # Pastikan data sesuai kolom di model User
                    user = Users_Info(
                        user_id=int(row['User_Id']),
                        name=row['name'],
                        location=row['location'],
                        age = row["age"]
                    )
                    db.session.add(user)  # Menambahkan ke sesi database

                db.session.commit()  # Commit transaksi
                print("Data berhasil dimasukkan ke dalam database!")

        except Exception as e:
            db.session.rollback()  # Rollback jika terjadi error
            print(f"Error saat memasukkan data: {e}")
    #digunkan untuk mencetak string setiap kali membuat elemen baru
    def __repr__(self):
        return '<Users %r>' % self.id

class Tourism_With_Id(db.Model):
    __tablename__ = "tourism_with_id"

    place_id = db.Column(db.Integer, primary_key=True)
    Place_Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(255), nullable=True)
    Category = db.Column(db.String(255), nullable=False)
    City = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.String(255), nullable=True)
    Rating = db.Column(db.Integer, nullable=True)
    Time_Minutes = db.Column(db.Integer, nullable=True)
    Latitude = db.Column(db.String(255), nullable=True)
    Longitude = db.Column(db.String(255), nullable=True)
    
    @staticmethod
    def insert_from_csv(file_path):
        """
        Fungsi untuk memasukkan data dari file CSV ke dalam tabel User.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)  # Membaca CSV sebagai dictionary
                for row in reader:
                    # Pastikan data sesuai kolom di model User 

                    user = Tourism_With_Id(
                        place_id=int(row['Place_Id']),
                        Place_Name=row['Place_Name'],
                        Description=row['Description'],
                        Category = row["Category"],
                        City = row["City"],
                        Price = row["Price"],
                        Rating = row["Rating"],
                        Time_Minutes = row["Time_Minutes"],
                        Latitude = row["Lat"],
                        Longitude = row["Long"]
                    )
                    db.session.add(user)  # Menambahkan ke sesi database

                db.session.commit()  # Commit transaksi
                print("Data berhasil dimasukkan ke dalam database!")

        except Exception as e:
            db.session.rollback()  # Rollback jika terjadi error
            print(f"Error saat memasukkan data: {e}")
    #digunkan untuk mencetak string setiap kali membuat elemen baru
    def __repr__(self):
        return '<tourism_with_id %r>' % self.place_id
    
