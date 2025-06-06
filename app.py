import datetime
import json
import secrets
import os
import time
import psycopg2
from flask import Flask, render_template, request, redirect, flash, url_for, get_flashed_messages, abort, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from bcrypt import hashpw, gensalt, checkpw
import configparser
from get_from_bd import BD

config = configparser.ConfigParser()
config.read('config')

app = Flask(__name__, static_url_path='/static/')
app.secret_key = config.get('data', 'secret_key')
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpg', 'gif'}

def allowed_file(file_name):
    if file_name.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        return True

def hash_password(password):
    # Генерация соли и хэширование
    salt = gensalt(rounds=12)  # Фактор стоимости = 12
    hashed = hashpw(password.encode(), salt)
    return hashed

# Проверка пароля
def verify_password(password, hashed):
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        bd = BD()
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        token = request.form['token']
        tokens = bd.give_tokens()
        if password == password2 and token in tokens:
            hased_password = hash_password(password).decode()
            conn = psycopg2.connect(dbname='trening_app', user='maksim',
                                    password=config.get('data', 'dbpassword'), host='localhost')
            cur = conn.cursor()
            cur.execute("""INSERT INTO users(user_name, password) 
            VALUES(%s, %s)""", (username, hased_password))
            conn.commit()
            bd.use_token(token)
            return redirect('login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        timestamp = int(request.form['timestamp'])
        cur_time = int(time.time() * 1000)
        if cur_time - timestamp <= 3000:
            get_flashed_messages()
            flash('Уходи', 'error')
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(dbname='trening_app', user='maksim',
                                password=config.get('data', 'dbpassword'), host='localhost')
        cur = conn.cursor()
        cur.execute("""SELECT password FROM users WHERE user_name = %s""", (username,))
        hashed = cur.fetchone()[0]
        if len(hashed) > 0 and verify_password(password, hashed):
            user = User(username)
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')

@app.route('/', methods=['GET'])
@login_required
def main():
    user_name = current_user.id
    bd = BD()
    trenings = bd.get_trening(user_name)
    role = bd.get_role(user_name)
    for i in range(len(trenings)):
        trenings[i] = str(trenings[i][1])[:10]
    trenings_dict = {}
    for i in  trenings:
        trenings_dict[i] = trenings_dict.get(i, 0) + 1
    types = bd.get_typs(user_name)
    return render_template('main.html', trenings=json.dumps(trenings_dict), types=types, role = role )

@app.route('/trainings/<trening_date>', methods=['POST', 'GET'])
@login_required
def trening(trening_date):
    if trening_date == 'today':
        trening_date = datetime.date.today()
    bd = BD()
    user_name = current_user.id
    if request.method == 'POST':
        all_gets = list(request.form)
        trening_id = bd.create_trening(trening_date, user_name)

        number_of_types = []
        exercises = []
        i = 0
        while i < len(all_gets):
            if 'exercise' in all_gets[i]:
                exercises.append(all_gets.pop(i))
            i += 1
        for exercise in exercises:
            number_of_exercise = exercise.split('_')[-1]
            exercise_type = request.form[exercise]
            exercise_id = bd.create_exercese(exercise_type, trening_id)
            for i in all_gets:
                if f'weight_{number_of_exercise}' in i:
                    number = i.split('_')[-1]
                    weight = request.form[i]
                    amount = request.form[f'amount_{number_of_exercise}_{number}']
                    bd.create_repetition(exercise_id, amount, weight)
    trening = bd.get_trening(user_name, trening_date)
    exercises = []
    exercise_types = bd.get_typs()
    for tren in trening:
        exercises.extend(bd.get_exercese_for_trening(tren[0]))
    return render_template('trainings.html', exercises=exercises, exercise_types = exercise_types, trening_date = trening_date )

@app.route('/trening_type/<trening_type_id>/', methods=['GET'])
@login_required
def trening_type_info(trening_type_id):
    bd = BD()
    user_name = current_user.id
    info = bd.get_all_repetitions_for_type(trening_type_id, user_name)
    labels = [str(i[0])[0:10] for i in info]
    amounts = [i[1] for i in info]
    weight = [i[2] for i in info]

    return render_template('trening_type.html', labels=labels, amounts=amounts, weight=weight )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    get_flashed_messages()
    flash('Вы успешно вышли из системы.', 'success')
    return redirect(url_for('login'))

@app.route('/delete_exercise', methods=['POST'])
@login_required
def delete_exercise():
    if request.method == 'POST' and check_role():
        exercese_id = request.form['exercese_id']
        trening_date = request.form['trening_date']
        bd = BD()
        bd.delete_exercese(exercese_id)
        return redirect(f'trainings/{trening_date}')

@app.route('/add_exercise', methods=['POST', 'GET'])
@login_required
def add_exercise_type():
    bd = BD()
    user_name = current_user.id
    if request.method == "POST" and bd.get_role(user_name):
        name = request.form['Ex_type']
        description = request.form['Description']
        file = request.files['image']
        if file and allowed_file(file.filename):
            f_format = file.filename.rsplit('.',1)[1]
            file_name = f'{name}{str(datetime.date.today())}.{f_format}'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            file.save(file_path)
            bd.create_type(name, description, file_name, file_path)
        else:
            bd.create_type(name, description)
    return render_template('add_exercise_type.html')

@app.route('/show_all_exercise', methods=['POST', 'GET', 'UPDATE'])
def show_all_exercise():
    bd = BD()
    ex_types = bd.get_typs()
    return render_template('all_exercise.html', types=ex_types)

@app.route('/edit_type/<trening_type_id>', methods=['POST', 'GET'])
def edit_type(trening_type_id):
    bd = BD()
    user_name = current_user.id
    if bd.get_role(user_name):
        ex_type = bd.get_typs(type_id = trening_type_id)[0]
        if request.method == 'POST' and bd.get_role(user_name):
            name = request.form['Ex_type']
            description = request.form['Description']
            file = request.files['image']
            if file and allowed_file(file.filename):
                f_format = file.filename.rsplit('.',1)[1]
                file_name = f'{name}{str(datetime.date.today())}.{f_format}'
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                file.save(file_path)
                bd.update_type(trening_type_id, name, description, file_name, file_path)
                return redirect('/show_all_exercise')

        return render_template('edit_exercise_type.html', type=ex_type)
    else:
        return render_template('you_dont_have_rights.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    user_name = current_user.id
    bd = BD()
    if bd.get_role(user_name):
        if request.method == 'POST':
            user_name = request.form['user_name']
            role = request.form['new_role']
            bd.set_role(user_name, role)
            return redirect(url_for('main'))
        users = bd.get_users()
        return render_template('admin.html', users = users)
    else:
        return render_template('you_dont_have_rights.html')

@app.route("/generate-token", methods=["GET"])
def generate_token():
    user_name = current_user.id
    bd = BD()
    if bd.get_role(user_name):
        bd = BD()
        token = secrets.token_hex(16)
        bd.add_token(token)
        return jsonify({"token": token})
    else:
        return render_template('you_dont_have_rights.html')

@app.route("/get-token", methods=["GET"])
def give_tokens():
    user_name = current_user.id
    bd = BD()
    if bd.get_role(user_name):
        bd = BD()
        tokens = bd.give_tokens()
        return jsonify({"token": tuple(tokens)})
    else:
        return render_template('you_dont_have_rights.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)