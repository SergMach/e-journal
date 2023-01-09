import sqlite3
from flask import flash



class DataBase:
    def __init__ (self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def getSchedule(self, user):
        [role], = self.__cur.execute('SELECT role FROM users WHERE id=?', (user,))
        if role == 'student':
            [user_group], = self.__cur.execute('SELECT group_name FROM users WHERE id=?', (user,))
            [group], = self.__cur.execute('SELECT id FROM schedule_group WHERE schedule_group_text=?', (user_group,))
            sql = f"SELECT schedule.id, schedule.p_g, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_group_id) LIKE '{group}' ORDER BY filt ASC, schedule_place_id ASC, schedule_number_id ASC, p_g ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

        if role == 'teacher':
            [user_name], = self.__cur.execute('SELECT name FROM users WHERE id=?', (user,))
            [name], = self.__cur.execute('SELECT id FROM schedule_teacher WHERE schedule_teacher_text=?', (user_name,))
            sql = f"SELECT schedule.id, schedule.p_g, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_teacher_id) LIKE '{name}' ORDER BY filt ASC, schedule_place_id ASC, schedule_number_id ASC, p_g ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

        else:
            return []


    def addUser(self, code, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                flash("Пользователь с таким email уже существует" )
                return False
            self.__cur.execute(f"SELECT COUNT() as count FROM users WHERE code LIKE '{code}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                flash("Пользователь с таким кодом уже существует" )
                return False
            try:
                self.__cur.execute(f"SELECT * FROM kode WHERE code = '{code}' LIMIT 1")
                res = self.__cur.fetchone()
                if not res:
                    flash("Неверный код")
                    return False
                [role], = self.__cur.execute('SELECT role FROM kode WHERE code=?', (code,))
                [group_name], = self.__cur.execute('SELECT group_name FROM kode WHERE code=?', (code,))
                [name], = self.__cur.execute('SELECT FIO FROM kode WHERE code=?', (code,))
            except sqlite3.Error as e:
                print("Ошибка получения данных из БД " + str(e))

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?)", (name, role, group_name, email, hpsw, code))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self .__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getNameList(self):
        sql = "SELECT * FROM schedule_name ORDER BY schedule_name_text, schedule_name_text_type"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getTeacherList(self):
        sql = "SELECT * FROM schedule_teacher ORDER BY schedule_teacher_text"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getAudList(self):
        sql = "SELECT * FROM schedule_aud"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getGroupList(self):
        sql = "SELECT * FROM schedule_group ORDER BY schedule_group_text"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getGroupSchedule(self, group):
        if group == 'Выберите из списка':
            return []
        else:
            sql = f"SELECT schedule.id, schedule.p_g, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_group_id) LIKE '{group}' ORDER BY filt ASC, schedule_place_id ASC, schedule_number_id ASC, p_g ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

####################################################
    def getAttend(self, group, teacher, subj):
        try:
            self .__cur.execute(f"SELECT attend_list.attend_list_id, students_name.students_name_text AS full_name_list, schedule_group.schedule_group_text AS group_list, schedule_name.schedule_name_text AS subject_list, schedule_teacher.schedule_teacher_text AS teacher_list, schedule_name.schedule_name_text_type AS type_list FROM attend_list JOIN schedule_group ON attend_list.group_list = schedule_group.id JOIN schedule_name ON attend_list.subject_list = schedule_name.id JOIN students_name ON attend_list.full_name_list = students_name.id  JOIN schedule_teacher ON attend_list.teacher_list = schedule_teacher.id  WHERE trim(teacher_list) LIKE '{teacher}' AND trim(group_list) LIKE '{group}' AND trim(subject_list) LIKE '{subj}' ORDER BY full_name_list ASC")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    def getStudentsList(self):
        sql = "SELECT * FROM students_name"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
############################################################

    def getUserInfo(self, user):
        try:
            self .__cur.execute(f"SELECT * FROM users WHERE id = '{user}' LIMIT 1")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                flash("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    def addScheduleBlock(self, schedule_group, name, day, place, time, teacher, aud, id2, p_group, check_p_group):

        if schedule_group == '' or name == '""' or day == '' or place == '' or time == '' or teacher == '' or aud == '' or id2 == '':
            flash("Заполните все строки")
            return False

        if check_p_group == 'None' and p_group != '0':
            flash("Это пара не для подгрупп")
            return False

        if check_p_group != 'None' and p_group == '0':
            flash("Это пара для подгрупп")
            return False

        if check_p_group == 'None' and p_group == '0':
            try:
                if schedule_group == '' or name == '' or day == '' or place == '' or time == '' or teacher == '' or aud == '' or id2 == '':
                    flash("Заполните все строки")
                    return False
            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False
            try:
                self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_time_id LIKE '{time}' AND schedule_day_id LIKE '{day}' AND schedule_group_id LIKE '{schedule_group}' AND schedule_place_id LIKE '{place}'")
                res = self.__cur.fetchone()
                if res['count'] > 0:
                    flash("Время занято" )
                    return False
            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False

            try:
                [type_check], = self.__cur.execute('SELECT schedule_name_text_type FROM schedule_name WHERE id=?', (name,))
                [voenka], = self.__cur.execute('SELECT schedule_name_text FROM schedule_name WHERE id=?', (name,))
                if type_check == 'Лекция' or voenka == 'Военная подготовка':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_name_id NOT LIKE '{name}' AND schedule_aud_id NOT LIKE '{aud}' AND schedule_day_id LIKE '{day}' AND schedule_teacher_id LIKE '{teacher}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Преподователь занят")
                        return False
                if type_check == 'Практика' and voenka != 'Военная подготовка':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_day_id LIKE '{day}' AND schedule_teacher_id LIKE '{teacher}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Преподователь занят")
                        return False
            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False

            try:
                [type_check], = self.__cur.execute('SELECT schedule_name_text_type FROM schedule_name WHERE id=?', (name,))
                [voenka], = self.__cur.execute('SELECT schedule_name_text FROM schedule_name WHERE id=?', (name,))
                if type_check == 'Практика' and voenka != 'Военная подготовка':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_day_id LIKE '{day}' AND schedule_aud_id LIKE '{aud}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Аудитория занята")
                        return False

                if type_check == 'Лекция' or voenka == 'Военная подготовка':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_teacher_id NOT LIKE '{teacher}' AND schedule_day_id LIKE '{day}' AND schedule_aud_id LIKE '{aud}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Аудитория занята")
                        return False
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_teacher_id LIKE '{teacher}' AND schedule_day_id LIKE '{day}' AND schedule_aud_id NOT LIKE '{aud}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Лекция и аудитории не совпадают")
                        return False

            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False

            try:
                self.__cur.execute("INSERT INTO schedule VALUES(NULL, ?, ?, NULL, ?, ?, ?, ?, ?, NULL, ?, ?, NULL )", (schedule_group, day, time, teacher, place, name, aud, day, id2))
                self.__db.commit()
                self.__cur.execute("INSERT INTO redactor_list_check VALUES(NULL, ?)", (id2,))
                self.__db.commit()
            except sqlite3.Error as e:
                print("Ошибка добавления  в БД "+str(e))
                return False
            return True

        if check_p_group != 'None' and p_group != '0':
            try:
                if schedule_group == '' or name == '' or day == '' or place == '' or time == '' or teacher == '' or aud == '' or id2 == '':
                    flash("Заполните все строки")
                    return False
            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False
            try:
                self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_time_id LIKE '{time}' AND schedule_day_id LIKE '{day}' AND schedule_group_id LIKE '{schedule_group}' AND schedule_place_id LIKE '{place}' AND p_g LIKE '{p_group}'")
                res = self.__cur.fetchone()
                if res['count'] > 0:
                    flash("Время занято" )
                    return False
            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False

            try:
                self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_time_id LIKE '{time}' AND schedule_day_id LIKE '{day}' AND schedule_group_id LIKE '{schedule_group}' AND schedule_place_id LIKE '{place}' AND p_g IS NULL")
                res = self.__cur.fetchone()
                if res['count'] > 0:
                    flash("Время занято" )
                    return False
            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False

            try:
                [type_check], = self.__cur.execute('SELECT schedule_name_text_type FROM schedule_name WHERE id=?', (name,))
                if type_check == 'Лекция':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_name_id NOT LIKE '{name}' AND schedule_aud_id NOT LIKE '{aud}' AND schedule_day_id LIKE '{day}' AND schedule_teacher_id LIKE '{teacher}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Преподователь занят")
                        return False
                if type_check == 'Практика':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_day_id LIKE '{day}' AND schedule_teacher_id LIKE '{teacher}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Преподователь занят")
                        return False
            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False

            try:
                [type_check], = self.__cur.execute('SELECT schedule_name_text_type FROM schedule_name WHERE id=?', (name,))
                if type_check == 'Практика':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_day_id LIKE '{day}' AND schedule_aud_id LIKE '{aud}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Аудитория занята")
                        return False

                if type_check == 'Лекция':
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_teacher_id NOT LIKE '{teacher}' AND schedule_day_id LIKE '{day}' AND schedule_aud_id LIKE '{aud}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Аудитория занята")
                        return False
                    self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_teacher_id LIKE '{teacher}' AND schedule_day_id LIKE '{day}' AND schedule_aud_id NOT LIKE '{aud}' AND schedule_place_id LIKE '{place}' AND schedule_time_id LIKE '{time}'")
                    res = self.__cur.fetchone()
                    if res['count'] > 0:
                        flash("Лекция и аудитории не совпадают")
                        return False

            except sqlite3.Error as e:
                print("Ошибка добавления в БД "+str(e))
                return False

            try:
                self.__cur.execute("INSERT INTO schedule VALUES(NULL, ?, ?, NULL, ?, ?, ?, ?, ?, NULL, ?, ?, ? )", (schedule_group, day, time, teacher, place, name, aud, day, id2, p_group))
                self.__db.commit()
                self.__cur.execute("INSERT INTO redactor_list_check VALUES(NULL, ?)", (id2,))
                self.__db.commit()
            except sqlite3.Error as e:
                print("Ошибка добавления  в БД "+str(e))
                return False
            return True

    def deleteScheduleBlock(self, schedule_group_delete, day_delete, place_delete, time_delete, p_group_delete):
        if schedule_group_delete == '' or day_delete == '' or place_delete == '' or time_delete == '' or p_group_delete == '':
            flash("Заполните все строки")
            return False
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_group_id ={schedule_group_delete} AND schedule_time_id = {time_delete} AND schedule_place_id ={place_delete} and schedule_day_id ={day_delete}")
            res = self.__cur.fetchone()
            if res['count'] == 0:
                flash("Пары нет")
                return False
            if p_group_delete == '0':
                self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_group_id ='{schedule_group_delete}' AND schedule_time_id ='{time_delete}' AND schedule_place_id ='{place_delete}' and schedule_day_id ='{day_delete}'")
                checking = self.__cur.fetchone()
                if checking['count'] > 1:
                    flash("Выберите подгруппу")
                    return False
                [id], = self.__cur.execute('SELECT c_id FROM schedule WHERE schedule_group_id =? AND schedule_time_id =? AND schedule_place_id =? and schedule_day_id =?', (schedule_group_delete,time_delete,place_delete,day_delete))
                self.__cur.execute(f"DELETE FROM schedule WHERE schedule_group_id = {schedule_group_delete} AND schedule_time_id = {time_delete} AND schedule_place_id = {place_delete} and schedule_day_id = {day_delete}")
                self.__db.commit()
                self.__cur.execute(f"DELETE FROM redactor_list_check WHERE check_id_parse = {id}")
                self.__db.commit()
            else:
                self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_group_id ='{schedule_group_delete}' AND schedule_time_id ='{time_delete}' AND schedule_place_id ='{place_delete}' and schedule_day_id ='{day_delete}' and p_g ='{p_group_delete}'")
                checking = self.__cur.fetchone()
                if checking['count'] == 0:
                    flash("Выберите подгруппу корректно")
                    return False
                [id], = self.__cur.execute('SELECT c_id FROM schedule WHERE schedule_group_id =? AND schedule_time_id =? AND schedule_place_id =? and schedule_day_id =? and p_g =?' , (schedule_group_delete,time_delete,place_delete,day_delete, p_group_delete))
                self.__cur.execute(f"DELETE FROM schedule WHERE schedule_group_id = {schedule_group_delete} AND schedule_time_id = {time_delete} AND schedule_place_id = {place_delete} and schedule_day_id = {day_delete} and p_g = {p_group_delete}")
                self.__db.commit()
                self.__cur.execute(f"DELETE FROM redactor_list_check WHERE check_id_parse = {id}")
                self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка удаления из БД "+str(e))
            return False
        return True

    def getUserRole(self, user):
        try:
            [res], = self.__cur.execute('SELECT role FROM users WHERE id=?', (user,))
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getTeacherSchedule(self, teacher):
        if teacher == 'Выберите из списка':
            return []
        else:
            sql = f"SELECT schedule.id, schedule.p_g, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_teacher_id) LIKE '{teacher}' ORDER BY filt ASC, schedule_place_id ASC, schedule_number_id ASC, p_g ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

    def getAudSchedule(self, aud):
        if aud == 'Выберите из списка':
            return []
        else:
            sql = f"SELECT schedule.id, schedule.p_g, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_aud_id) LIKE '{aud}' ORDER BY filt ASC, schedule_place_id ASC, schedule_number_id ASC, p_g ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

    def getTeacherGlobalList(self, group_active):
        sql = f"SELECT DISTINCT list_teacher AS id, schedule_teacher.schedule_teacher_text AS list_teacher FROM schedule_redactor_list JOIN schedule_teacher ON schedule_redactor_list.list_teacher = schedule_teacher.id WHERE trim(list_group) LIKE '{group_active}' ORDER BY list_teacher"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getNameGlobalList(self, group_active):
        sql = f"SELECT list_name AS id, schedule_name.schedule_name_text AS list_name, schedule_name.schedule_name_text_type AS list_type, list_id as check_id, list_p_group FROM schedule_redactor_list JOIN schedule_name ON schedule_redactor_list.list_name = schedule_name.id WHERE trim(list_group) LIKE '{group_active}' AND trim(check_id) NOT IN (select check_id_parse from redactor_list_check) ORDER BY list_name"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
            else: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False


    def deleteScheduleAll(self, group):
        try:
            self.__cur.execute(f"DELETE FROM redactor_list_check WHERE check_id_parse IN (SELECT c_id FROM schedule WHERE trim(schedule_group_id) LIKE '{group}')")
            self.__db.commit()
            self.__cur.execute(f"DELETE FROM schedule WHERE trim(schedule_group_id) LIKE '{group}'")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def SchUpd(self, num):
        try:
            #import parser
            self.__cur.execute("DELETE FROM schedule_name")
            self.__db.commit()
            self.__cur.execute("DELETE FROM schedule_group")
            self.__db.commit()
            self.__cur.execute("DELETE FROM schedule_aud")
            self.__db.commit()
            self.__cur.execute("DELETE FROM schedule_teacher")
            self.__db.commit()
            self.__cur.execute("DELETE FROM schedule_redactor_list")
            self.__db.commit()
            self.__cur.execute("DELETE FROM schedule")
            self.__db.commit()
            self.__cur.execute("DELETE FROM redactor_list_check")
            self.__db.commit()
            self.__cur.execute("INSERT OR REPLACE into schedule_name (schedule_name_text, schedule_name_text_type) SELECT DISTINCT subject, subj_type from parse_schedule")
            self.__db.commit()
            self.__cur.execute("INSERT OR REPLACE into schedule_group (schedule_group_text) SELECT DISTINCT full_group from parse_schedule")
            self.__db.commit()
            self.__cur.execute("INSERT OR REPLACE into schedule_aud (schedule_aud_text) SELECT DISTINCT aud from parse_schedule")
            self.__db.commit()
            self.__cur.execute("INSERT OR REPLACE into schedule_teacher (schedule_teacher_text) SELECT DISTINCT teacher from parse_schedule")
            self.__db.commit()
            self.__cur.execute("INSERT OR REPLACE into schedule_redactor_list (list_id ,list_group, list_teacher, list_name, list_type, list_p_group)  SELECT parse_id, schedule_group.id AS full_group, schedule_teacher.id AS teacher, schedule_name.id AS subject, schedule_name.id AS subj_type, p_group FROM parse_schedule JOIN schedule_group ON parse_schedule.full_group = schedule_group.schedule_group_text JOIN schedule_teacher ON parse_schedule.teacher = schedule_teacher.schedule_teacher_text JOIN schedule_name ON parse_schedule.subject = schedule_name.schedule_name_text WHERE trim(subject) LIKE trim(schedule_name_text) AND trim(subj_type) LIKE trim(schedule_name_text_type)")
            self.__db.commit()
            self.__cur.execute("INSERT OR REPLACE into schedule (c_id, schedule_group_id, schedule_place_id, schedule_day_id, schedule_time_id, schedule_teacher_id, schedule_aud_id, schedule_name_id, schedule_type_id, filt, p_g) SELECT parse_id, schedule_group.id AS full_group, schedule_place.id AS week, schedule_day.id AS day, schedule_time.id AS number_lesson, schedule_teacher.id AS teacher, schedule_aud.id AS aud, schedule_name.id AS subject, schedule_name.id AS subj_type, schedule_day.id AS filt, p_group FROM parse_schedule JOIN schedule_group ON parse_schedule.full_group = schedule_group.schedule_group_text JOIN schedule_place ON parse_schedule.week  = schedule_place.schedule_place_text JOIN schedule_day ON parse_schedule.day  = schedule_day.schedule_day_text JOIN schedule_time ON parse_schedule.number_lesson  = schedule_time.schedule_time_text_place JOIN schedule_teacher ON parse_schedule.teacher = schedule_teacher.schedule_teacher_text JOIN schedule_aud ON parse_schedule.aud = schedule_aud.schedule_aud_text JOIN schedule_name ON parse_schedule.subject = schedule_name.schedule_name_text WHERE trim(subject) LIKE trim(schedule_name_text) AND trim(subj_type) LIKE trim(schedule_name_text_type)")
            self.__db.commit()
            self.__cur.execute("INSERT OR REPLACE into redactor_list_check (check_id_parse) SELECT c_id from schedule")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False