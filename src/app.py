from flask import Flask, render_template, redirect, url_for, request
from config import config

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        print(request.form['identification'])  
        print(request.form['password'])  
    return render_template('auth/login.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()

