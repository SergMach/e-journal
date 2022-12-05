import math
import sqlite3
from datetime import time


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
        print(role)
        if role == 'student':
            [user_group], = self.__cur.execute('SELECT group_name FROM users WHERE id=?', (user,))
            print(user_group)
            [group], = self.__cur.execute('SELECT id FROM schedule_group WHERE schedule_group_text=?', (user_group,))
            print(group)
            sql = f"SELECT schedule.id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_group_id) LIKE '{group}' ORDER BY schedule_day_id DESC, schedule_place_id ASC, schedule_number_id ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

        if role == 'teacher':
            [user_name], = self.__cur.execute('SELECT name FROM users WHERE id=?', (user,))
            print(user_name)
            [name], = self.__cur.execute('SELECT id FROM schedule_teacher WHERE schedule_teacher_text=?', (user_name,))
            print(name)
            sql = f"SELECT schedule.id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_teacher_id) LIKE '{name}' ORDER BY schedule_day_id DESC, schedule_place_id ASC, schedule_number_id ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

        else:
            return []


    def addUser(self, name, code, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует" )
                return False
            try:
                self.__cur.execute(f"SELECT * FROM kode WHERE code = '{code}' LIMIT 1")
                res = self.__cur.fetchone()
                if not res:
                    print("Неверный код")
                    return False
                [role], = self.__cur.execute('SELECT role FROM kode WHERE code=?', (code,))
                [group_name], = self.__cur.execute('SELECT group_name FROM kode WHERE code=?', (code,))
                print(role)
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
        sql = "SELECT * FROM schedule_name"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getTeacherList(self):
        sql = "SELECT * FROM schedule_teacher"
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
        sql = "SELECT * FROM schedule_group"
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
            print(group)
            [group], = self.__cur.execute('SELECT id FROM schedule_group WHERE schedule_group_text=?', (group,))
            sql = f"SELECT schedule.id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_group_id) LIKE '{group}' ORDER BY schedule_day_id DESC, schedule_place_id ASC, schedule_number_id ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                print(res)
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []


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
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False
