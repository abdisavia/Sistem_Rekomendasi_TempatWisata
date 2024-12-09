from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required
)


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3360/touristAttraction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
db.init_app(app)


@app.route("/")
def authOption() :
    return render_template("authOption.html")

@app.route("/loginForm")
def loginForm():
    return render_template("loginForm.html")

@app.route("/regisForm")
def regisForm():
    return render_template("regisForm.html")

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
