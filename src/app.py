from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import login_manager, login_user, logout_user, login_required
from config import config
from models.ModelUser import ModelUser 
from models.entities.user import User
app = Flask(__name__)

db=MySQL(app)



@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = User(0, request.form['identification'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:  # Assuming this is where you check if the password is valid
                return redirect(url_for('home'))  # Corrected: Added return statement
            else:
                flash("Contraseña inválida")
        else:
            flash("Usuario no encontrado")
    return render_template('auth/login.html')  # Moved outside the if-else block


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout8():
    return render_template('logout.html')



if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
