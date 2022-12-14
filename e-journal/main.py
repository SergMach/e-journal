from flask import Flask, render_template,  request, g, redirect, url_for, flash, render_template_string
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

@app.errorhandler(404)
def page_not_found():
    return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404

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
    try:
        user = current_user.get_id()
        role = dbase.getUserRole(user)
    except: role = ''
    return render_template("index.html", menu=dbase.getMenu(), role=role, title="Главная")

@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        user = current_user.get_id()
        role = dbase.getUserRole(user)
        if role: return redirect(url_for('index'))
    except: role = ''
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('profile'))

    return render_template("login.html", menu=dbase.getMenu(), role=role, title="Вход")

@app.route("/profile")
@login_required
def profile():
    user = current_user.get_id()
    role = dbase.getUserRole(user)
    return render_template("profile.html", menu=dbase.getMenu(), role=role, user=dbase.getUserInfo(user), title="Личный кабинет")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=["POST", "GET"])
def register():
    try:
        user = current_user.get_id()
        role = dbase.getUserRole(user)
        if role: return redirect(url_for('index'))
    except: role = ''
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['code'], request.form['email'], hash)
            if res:
                return redirect(url_for('login'))
    return render_template("register.html", menu=dbase.getMenu(), role=role, title="Регистрация")

@app.route("/schedule")
@login_required
def schedule():
    user = current_user.get_id()
    role = dbase.getUserRole(user)
    return render_template("schedule.html", menu=dbase.getMenu(), schedule=dbase.getSchedule(user), role=role, title="Быстрое расписание")

##################################################################
@app.route("/attend", methods=["POST", "GET"])
@login_required
def attend():
    user = current_user.get_id()
    role = dbase.getUserRole(user)
    if role == "teacher":
        teacher_id = dbase.getMyTeacher(user)
        menu = dbase.getMenu()
        group = dbase.getGroupList()
        teacher = dbase.getTeacherList()
        subj = dbase.getNameList()
        attend_list = dbase.getAttendList()
        try:
            if request.form['group'] and request.form['teacher'] and request.form['subj'] and request.method == 'POST':
                curr_group = int(request.form['group'])
                curr_teacher = int(request.form['teacher'])
                curr_subj = int(request.form['subj'])
        except:
            print('1')
        return render_template("attend.html", attend_list=attend_list, user=teacher_id, menu=menu, group=group, role=role, teacher=teacher, subj=subj, title="Посещаемость")



    # elif role == 'moderator':attend=dbase.getAttend(user, dbase.getTeacherList(), dbase.getNameList()),
    #     return render_template("attend.html", menu=dbase.getMenu(), attend=dbase.getAttend(user), teacher=dbase.getTeacherList(), group=dbase.getGroupList(), role=role, title="Посещаемость")
    return page_not_found()
#####################################################################

@app.route("/schedule_global", methods=["POST", "GET"])
def schedule_global():
    try:
        user = current_user.get_id()
        role = dbase.getUserRole(user)
    except: role = ''
    if request.method == "POST":
        try:
            if request.form['group']:
                group = request.form['group']
                return render_template("schedule_global.html", menu=dbase.getMenu(), schedule=dbase.getGroupSchedule(group), role=role, group=dbase.getGroupList(), title="Расписание")
        except: print ('1')
    return render_template("schedule_global.html", menu=dbase.getMenu(), role=role, group=dbase.getGroupList(), title="Расписание")

@app.route("/schedule_teacher", methods=["POST", "GET"])
def schedule_teacher():
    try:
        user = current_user.get_id()
        role = dbase.getUserRole(user)
    except: role = ''
    if request.method == "POST":
        try:
            if request.form['teacher']:
                teacher = request.form['teacher']
                return render_template("schedule_teacher.html", menu=dbase.getMenu(), schedule=dbase.getTeacherSchedule(teacher), role=role, teacher=dbase.getTeacherList(), title="Расписание")
        except: print('1')
    return render_template("schedule_teacher.html", menu=dbase.getMenu(), role=role, teacher=dbase.getTeacherList(), title="Расписание")

@app.route("/schedule_aud", methods=["POST", "GET"])
def schedule_aud():
    try:
        user = current_user.get_id()
        role = dbase.getUserRole(user)
    except: role = ''
    if request.method == "POST":
        try:
            if request.form['aud']:
                aud = request.form['aud']
                return render_template("schedule_aud.html", menu=dbase.getMenu(), schedule=dbase.getAudSchedule(aud), role=role, aud=dbase.getAudList(), title="Расписание")
        except: print ('1')
    return render_template("schedule_aud.html", menu=dbase.getMenu(), role=role, aud=dbase.getAudList(), title="Расписание")

@app.route("/schedule_global_redactor",  methods=["POST", "GET"])
@login_required
def schedule_global_redactor():
    user = current_user.get_id()
    role = dbase.getUserRole(user)
    if role == "moderator":
        global i
        user = current_user.get_id()
        if request.method == "POST":
            try:
                res = request.form['group_r'], request.form['number']
                if res:
                    i = int(request.form['number'])
                    number = list(range(1, i+1))
                    print(number)
                    number = list(map(str, number))
                    print(number)
                    schedule_group = request.form['group_r']
                    return render_template("schedule_global_redactor.html", role=role,  menu=dbase.getMenu(), group=dbase.getGroupList(), name=dbase.getNameGlobalList(schedule_group), teacher=dbase.getTeacherGlobalList(schedule_group), aud=dbase.getAudList(), number=number, schedule_group=schedule_group, title="Редактирование расписания")
            except: print('1')
            try:
                schedule_group = (request.form.getlist('schedule_group'))
                name = (request.form.getlist('name'))
                day = (request.form.getlist('day'))
                place = (request.form.getlist('place'))
                time = (request.form.getlist('time'))
                teacher = (request.form.getlist('teacher'))
                aud = (request.form.getlist('aud'))
                for i1, i2, i3, i4, i5, i6, i7 in zip(schedule_group, name, day, place, time, teacher, aud):
                    res = dbase.addScheduleBlock(i1, i2, i3, i4, i5, i6, i7)
                if res:
                    return render_template("schedule_global_redactor.html", menu=dbase.getMenu(), role=role, group=dbase.getGroupList(), title="Редактирование расписания")
            except: print('1')

        return render_template("schedule_global_redactor.html", menu=dbase.getMenu(), role=role, group=dbase.getGroupList(), title="Редактирование расписания")
    else: return render_template("index.html", menu=dbase.getMenu(), title="Редактирование расписания")

@app.route("/schedule_redactor",  methods=["POST", "GET"])
@login_required
def schedule_redactor():
    user = current_user.get_id()
    role = dbase.getUserRole(user)
    if role == "moderator":
        user = current_user.get_id()
        if request.method == "POST":
            try:
                if request.form['group']:
                    group = request.form['group']
                    return render_template("schedule_redactor.html",  role=role, menu=dbase.getMenu(), group=dbase.getGroupList(), schedule=dbase.getGroupSchedule(group), aud=dbase.getAudList(), teacher=dbase.getTeacherList(), name=dbase.getNameList(), title="Редактирование расписания")
            except: print('1')
            try:
                res = dbase.addScheduleBlock(request.form['schedule_group'], request.form['name'], request.form['day'], request.form['place'], request.form['time'], request.form['teacher'], request.form['aud'])
                if res:
                    return render_template("schedule_redactor.html", role=role, schedule=dbase.getGroupSchedule(request.form['schedule_group']),  menu=dbase.getMenu(), group=dbase.getGroupList(), aud=dbase.getAudList(), teacher=dbase.getTeacherList(), name=dbase.getNameList(), title="Редактирование расписания")
            except: print('1')
            try:
                res = dbase.deleteScheduleBlock(request.form['schedule_group_delete'],  request.form['day_delete'], request.form['place_delete'], request.form['time_delete'])
                if res:
                    return render_template("schedule_redactor.html", role = role, schedule=dbase.getGroupSchedule(request.form['schedule_group_delete']),  menu=dbase.getMenu(), group=dbase.getGroupList(), aud=dbase.getAudList(), teacher=dbase.getTeacherList(), name=dbase.getNameList(), title="Редактирование расписания")
            except: print('1')


        return render_template("schedule_redactor.html", menu=dbase.getMenu(), role = role, group=dbase.getGroupList(), aud=dbase.getAudList(), teacher=dbase.getTeacherList(), name=dbase.getNameList(), title="Редактирование расписания")
    else: return render_template("index.html", menu=dbase.getMenu(), title="Редактирование расписания")

if __name__ == "__main__":
    app.run(debug=True)