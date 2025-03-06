import json

import psycopg2
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from bcrypt import hashpw, gensalt, checkpw
import configparser
from get_from_bd import BD

config = configparser.ConfigParser()
config.read('config.ini')


def hash_password(password):
    # Генерация соли и хэширование
    salt = gensalt(rounds=12)  # Фактор стоимости = 12
    hashed = hashpw(password.encode(), salt)
    return hashed

# Проверка пароля
def verify_password(password, hashed):
    return checkpw(password.encode(), hashed)

app = Flask(__name__)
app.secret_key = config.read('data', 'secret_key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = psycopg2.connect(dbname='trening_app', user='maksim',
                                password=config.read('data', 'dbpassword'), host='localhost')
        cur = conn.cursor()
        cur.execute("""SELECT password FROM users WHERE user_name = %s""", (username,))
        hashed = cur.fetchone()
        if len(hashed) > 0 and checkpw(password.encode(), hashed[0]):
            user = User(username)
            load_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect('main')
        else:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')

@app.route('/', methods=['GET'])
def main():
    bd = BD()
    trenings = bd.get_trening()
    for i in range(len(trenings)):
        trenings[i] = str(trenings[i][1])[:10]
    trenings_dict = {}
    for i in  trenings:
        trenings_dict[i] = trenings_dict.get(i, 0) + 1

    return render_template('main.html', trenings=json.dumps(trenings_dict ))

@app.route('/treening/<trening_date>')
def trening(trening_date):
    bd = BD()
    trening = bd.get_trening(trening_date)

if __name__ == '__main__':
    app.run(debug=True)