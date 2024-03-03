from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config
from models.ModelUser import ModelUser 
from models.entities.user import User
from flask_wtf import CSRFProtect
app = Flask(__name__)

# Configuración de la base de datos y del login manager
db = MySQL(app)
csrf= CSRFProtect()
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = User(0, request.form['identification'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password: # Si la contraseña es correcta
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña inválida")
        else:
            flash("Usuario no encontrado")
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')


def status404(error):
    return "<center><h1> No se pudo encontrar la pagina </h1></center>", 404

def status401(error):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(404, status404)
    app.register_error_handler(401, status401)
    app.run()
