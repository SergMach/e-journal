from flask import Flask, render_template,  request, g, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

import sqlite3
import os
from DataBase import DataBase
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = '/tmp/e_journal.db'
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'e_journal.db')))

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db



@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)

@app.route("/")
def index():
    return render_template("index.html", menu=dbase.getMenu(), title="Главная")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('success'))

    return render_template("login.html", menu=dbase.getMenu(), title="Aвтоpизaция")

@app.route("/success")
@login_required
def success():
    user = current_user.get_id()
    return render_template("success.html", menu=dbase.getMenu(), user=dbase.getUserInfo(user))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['code'], request.form['email'], hash)
            if res:
                return redirect(url_for('login'))
    return render_template("register.html", menu=dbase.getMenu(), title="")

@app.route("/schedule")
def schedule():
    user = current_user.get_id()
    return render_template("schedule.html", menu=dbase.getMenu(), schedule=dbase.getSchedule(user), title="Главная")

@app.route("/schedule_redactor",  methods=["POST", "GET"])
def schedule_redactor():
    user = current_user.get_id()
    if request.method == "POST":
        group = request.form['group']
        if group:
            return render_template("schedule_redactor.html", menu=dbase.getMenu(), group=dbase.getGroupList(), schedule=dbase.getGroupSchedule(group), aud=dbase.getAudList(), teacher=dbase.getTeacherList(), name=dbase.getNameList(), title="Главная")



    return render_template("schedule_redactor.html", menu=dbase.getMenu(), group=dbase.getGroupList(), aud=dbase.getAudList(), teacher=dbase.getTeacherList(), name=dbase.getNameList(), title="Главная")

if __name__ == "__main__":
    app.run(debug=True)