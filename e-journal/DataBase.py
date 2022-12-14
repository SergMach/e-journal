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
            sql = f"SELECT schedule.id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_group_id) LIKE '{group}' ORDER BY schedule_day_id DESC, schedule_place_id ASC, schedule_number_id ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                print(res)
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

    def addAttendList(self):
        try:
            self .__cur.execute("SELECT * FROM attend_list")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False


    def getMyTeacher(self, user):
        try:
            self .__cur.execute(f"SELECT * FROM schedule_teacher WHERE id = '{user}' LIMIT 1")
            res = self.__cur.fetchone()
            return res
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
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    def addScheduleBlock(self, schedule_group, name, day, place, time, teacher, aud):
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM schedule WHERE schedule_time_id LIKE '{time}' AND schedule_day_id LIKE '{day}' AND schedule_group_id LIKE '{schedule_group}' AND schedule_place_id LIKE '{place}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Время занято" )
                return False
        except sqlite3.Error as e:
            print("Ошибка добавления в БД "+str(e))
            return False
        try:
            self.__cur.execute("INSERT INTO schedule VALUES(NULL, ?, ?, NULL, ?, ?, ?, ?, ?, NULL)", (schedule_group, day, time, teacher, place, name, aud))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления  в БД "+str(e))
            return False
        return True

    def deleteScheduleBlock(self, schedule_group_delete, day_delete, place_delete, time_delete):
        try:
            self.__cur.execute(f"DELETE FROM schedule WHERE schedule_group_id = {schedule_group_delete} AND schedule_time_id = {time_delete} AND schedule_place_id = {place_delete} and schedule_day_id = {day_delete}")
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
            sql = f"SELECT schedule.id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_teacher_id) LIKE '{teacher}' ORDER BY schedule_day_id DESC, schedule_place_id ASC, schedule_number_id ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                print(res)
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

    def getAudSchedule(self, aud):
        if aud == 'Выберите из списка':
            return []
        else:
            sql = f"SELECT schedule.id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_aud.schedule_aud_text AS schedule_aud_id, schedule_day.schedule_day_text AS schedule_day_id, schedule_group.schedule_group_text AS schedule_group_id, schedule_name.schedule_name_text AS schedule_name_id, schedule_time.schedule_time_text_place AS schedule_number_id, schedule_place.schedule_place_text AS schedule_place_id, schedule_teacher.schedule_teacher_text AS schedule_teacher_id, schedule_time.schedule_time_text AS schedule_time_id, schedule_name.schedule_name_text_type AS schedule_type_id FROM schedule JOIN schedule_day ON schedule.schedule_day_id = schedule_day.id JOIN schedule_group ON schedule.schedule_group_id = schedule_group.id JOIN schedule_name ON schedule.schedule_name_id = schedule_name.id JOIN schedule_place ON schedule.schedule_place_id = schedule_place.id JOIN schedule_teacher ON schedule.schedule_teacher_id = schedule_teacher.id JOIN schedule_time ON schedule.schedule_time_id = schedule_time.id JOIN schedule_aud ON schedule.schedule_aud_id = schedule_aud.id WHERE trim(schedule_aud_id) LIKE '{aud}' ORDER BY schedule_day_id DESC, schedule_place_id ASC, schedule_number_id ASC"
            try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                print(res)
                if res: return res
            except:
                print("Ошибка чтения из БД")
            return []

    def getTeacherGlobalList(self, group_active):
        sql = f"SELECT DISTINCT list_teacher AS id, schedule_teacher.schedule_teacher_text AS list_teacher FROM schedule_redactor_list JOIN schedule_teacher ON schedule_redactor_list.list_teacher = schedule_teacher.id WHERE trim(list_group) LIKE '{group_active}' ORDER BY id ASC"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getNameGlobalList(self, group_active):
        print(group_active)
        sql = f"SELECT DISTINCT list_name AS id, schedule_name.schedule_name_text AS list_name, schedule_name.schedule_name_text_type AS list_type FROM schedule_redactor_list JOIN schedule_name ON schedule_redactor_list.list_name = schedule_name.id WHERE trim(list_group) LIKE '{group_active}' ORDER BY id ASC"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False