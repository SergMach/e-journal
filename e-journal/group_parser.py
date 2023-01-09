import requests
from bs4 import BeautifulSoup
import sqlite3
import os.path



def main_parser():

    url_site = "http://studydep.miigaik.ru/index.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    dirty_data = list()
    fak = 'ФГиИБ' #str(input('Введите факультет (ГФ, КФ, ФАГ, ФОП, ФУТ, ФГиИБ, ЗФ): '))
    kurs = '1' # str(input('Введите курс (1, 2, 3, 4, 5)): '))
    grup = '2022-ФГиИБ-ИСиТ-1б' #, '2022-ФГиИБ-ИСиТ-2б', '2022-ФГиИБ-ИСиТ-3б'

    data_schedule = requests.post(url=url_site, data={'fak':fak, 'kurs':kurs, 'grup':grup}, headers=headers)
    soup_schedule = BeautifulSoup(data_schedule.text, 'lxml')
    """ Читаем разметку таблицы по строкам - пишем строки в list """
    schedule=[]
    for table_schedule in soup_schedule.find('table',attrs={"class":"t"}).find_all('tr'):
        rows_schedule = [row_schedule.text for row_schedule in table_schedule.find_all('td')]
        schedule.append(rows_schedule)
        dirty_data.append(schedule)

    """чистка данных"""

    if isinstance(dirty_data, list):
        try:
            dirty_data.remove('Понедельник\xa0')
            dirty_data.remove('Вторник\xa0')
            dirty_data.remove('Среда\xa0')
            dirty_data.remove('Четверг\xa0')
            dirty_data.remove('Пятница\xa0')
            dirty_data.remove('Суббота\xa0')
        except: 
            pass
        for i in dirty_data:
            if isinstance(i, list):
                try:
                    i.remove('Понедельник\xa0')
                    i.remove('Вторник\xa0')
                    i.remove('Среда\xa0')
                    i.remove('Четверг\xa0')
                    i.remove('Пятница\xa0')
                    i.remove('Суббота\xa0')
                except: 
                    pass
                for j in i:
                    if isinstance(j, list):
                        try:
                            j.remove('Понедельник\xa0')
                            j.remove('Вторник\xa0')
                            j.remove('Среда\xa0')
                            j.remove('Четверг\xa0')
                            j.remove('Пятница\xa0')
                            j.remove('Суббота\xa0')
                        except: 
                            pass
                    else:
                        try:
                            j.remove('Понедельник\xa0')
                            j.remove('Вторник\xa0')
                            j.remove('Среда\xa0')
                            j.remove('Четверг\xa0')
                            j.remove('Пятница\xa0')
                            j.remove('Суббота\xa0')
                        except: 
                            pass
            else:
                try:
                    i.remove('Понедельник\xa0')
                    i.remove('Вторник\xa0')
                    i.remove('Среда\xa0')
                    i.remove('Четверг\xa0')
                    i.remove('Пятница\xa0')
                    i.remove('Суббота\xa0')
                except: 
                    pass
    else:
        try:
            dirty_data.remove('Понедельник\xa0')
            dirty_data.remove('Вторник\xa0')
            dirty_data.remove('Среда\xa0')
            dirty_data.remove('Четверг\xa0')
            dirty_data.remove('Пятница\xa0')
            dirty_data.remove('Суббота\xa0')
        except: 
            pass
    
    one_data = []

    day = []
    lesson = []
    week = []
    p_group = []
    subject = []
    teacher = []
    aud = []
    subj_type = []
    comment = []

    for it in dirty_data:
        for ite in it:
            if (ite) and (len(ite) <= 2):
                del ite
                continue
            #print(ite)
            for iter in ite:
                one_data.append(iter.strip().lower())
                #print(len(one_data))
                if len(one_data) % 9 == 1:
                    day.append(iter.strip().lower())
                if len(one_data) % 9 == 2:
                    lesson.append(iter.strip().lower())
                if len(one_data) % 9 == 3:
                    week.append(iter.strip().lower())
                if len(one_data) % 9 == 4:
                    p_group.append(iter.strip().lower())
                if len(one_data) % 9 == 5:
                    subject.append(iter.strip().lower())
                if len(one_data) % 9 == 6:
                    teacher.append(iter.strip().title())
                if len(one_data) % 9 == 7:
                    aud.append(iter.strip().lower())
                if len(one_data) % 9 == 8:
                    subj_type.append(iter.strip().lower())
                # if len(one_data) % 9 == 0:
                #     comment.append(iter)
            #print(f'Факультет {fak} {len(fak)} \n Курс {kurs} {len(kurs)} \n Группа {grup} {len(grup)} \nДень {day} {len(day)} \n Пары {lesson} {len(lesson)} \n Неделя {week} {len(week)} \n Подгруппа {p_group} {len(p_group)} \n Предмет {subject} {len(subject)} \n Препод {teacher} {len(teacher)} \n Аудитория {aud} {len(aud)} \n Тип {subj_type} {len(subj_type)} \n Коммент {comment} {len(comment)} \n')
    if len(day)==len(lesson)==len(week)==len(p_group)==len(subject)==len(teacher)==len(aud)==len(subj_type):
        # print(len(day))
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "e_journal.db")
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        for num in range(1, len(day)):
            # print(f'Факультет {fak}\n Курс {kurs}\n Группа {grup}\nДень {day[num]}\n Пары {lesson[num]}\n Неделя {week[num]}\n Подгруппа {p_group[num]}\n Предмет {subject[num]}\n Препод {teacher[num]}\n Аудитория {aud[num]}\n Тип {subj_type[num]}')
            cursor.execute(""" 
                INSERT INTO parse_schedule (faculty, course, full_group, week, day, number_lesson, subject, teacher, aud, subj_type, p_group)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fak, kurs, grup, week[num], day[num], lesson[num], subject[num], teacher[num], aud[num], subj_type[num], p_group[num]))
            connection.commit()
            cursor.execute('''
                DELETE a.* FROM mytable a,
                    (SELECT
                    b.country_id, b.city_name, MIN(b.id) mid
                    FROM mytable b
                    GROUP BY b.country_id, b.city_name
                    ) c
                WHERE
                    a.country_id = c.country_id
                    AND a.city_name = c.city_name
                    AND a.id > c.mid
            ''')


    # for it in dirty_data:
    #     for iter in it:
    #         if iter:
    #             if len(iter) <= 2:
    #                 del iter
    #                 continue
    #             data.append(iter)
    #             for elem in iter:
    #                 if elem.strip() == '\xa0':
    #                     elem = ""
    #                 data.append(elem.strip())

    # day = []
    # lesson = []
    # week = []
    # p_group = []
    # subject = []
    # teacher = []
    # aud = []
    # subj_type = []
    # comment = []

    # for element in data:
    #     if len(element) <= 2:
    #         del element

        # day.append(element[0])
        # lesson.append(element[1])
        # week.append(element[2])
        # p_group.append(element[3])
        # subject.append(element[4])
        # teacher.append(element[5])
        # aud.append(element[6])
        # subj_type.append(element[7])
        # comment.append(element[8])

    # return print(f'Факультет {fak} {len(fak)} \n Курс {kurs} {len(kurs)} \n Группа {grup} {len(grup)} \nДень {day} {len(day)} \n Пары {lesson} {len(lesson)} \n Неделя {week} {len(week)} \n Подгруппа {p_group} {len(p_group)} \n Предмет {subject} {len(subject)} \n Препод {teacher} {len(teacher)} \n Аудитория {aud} {len(aud)} \n Тип {subj_type} {len(subj_type)} \n Коммент {comment} {len(comment)} \n')
    
    return print('worked') #one_data

def check(fak, kurs, group):
    fak = str(input('Введите факультет (ГФ, КФ, ФАГ, ФОП, ФУТ, ФГиИБ): '))
    if fak.strip().lower() == 'гф':
        kurs = str(input('Введите курс (1, 2, 3, 4, 5)): '))
        fak = 'ГФ'
        if str(kurs).strip() == '1':
            group = str(input('Введите группу (2022-ГФ-АКС-1асп, 2022-ГФ-Г-1асп, 2022-ГФ-ГиДЗакс-1б, 2022-ГФ-ГиДЗакс-1м, 2022-ГФ-ГиДЗг-1б, 2022-ГФ-ГиДЗг-1м, 2022-ГФ-ГиДЗипр-1б, \
                                               2022-ГФ-ГиДЗкгин-1б, 2022-ГФ-ПГинж.г-1с, 2022-ГФ-ПГинж.г-2с, 2022-ГФ-ПГинж.г-3с, 2022-ГФ-ПГинж.г-4с, 2022-ГФ-ПГинж.г-5с)): '))
        elif str(kurs).strip() == '2':
            group = str(input('Введите группу (2021-ГФ-АКС-1асп(зо), 2021-ГФ-АКС-1асп(оч), 2021-ГФ-Г-1асп(зо), 2021-ГФ-Г-1асп(оч), 2021-ГФ-ГиДЗакс-1б, 2021-ГФ-ГиДЗакс-1м, \
                                               2021-ГФ-ГиДЗг-1б, 2021-ГФ-ГиДЗг-1м, 2021-ГФ-ГиДЗипр-1б, 2021-ГФ-ГиДЗипр-1м, 2021-ГФ-ГиДЗкгин-1б, 2021-ГФ-ПГинж.г-1с, \
                                               2021-ГФ-ПГинж.г-2с, 2021-ГФ-ПГинж.г-3с, 2021-ГФ-ПГинж.г-4с)): '))
        elif str(kurs).strip() == '3':
            group = str(input('Введите группу (2020-ГФ-ГиДЗакс-1б, 2020-ГФ-ГиДЗг-1б, 2020-ГФ-ГиДЗипр-1б, 2020-ГФ-ГиДЗкгин-1б, 2020-ГФ-ПГинж.г-1с, 2020-ГФ-ПГинж.г-2с, \
                                               2020-ГФ-ПГинж.г-3с, 2020-ГФ-ПГинж.г-4с, 2020-ГФ-ПГинж.г-5с)): '))
        elif str(kurs).strip() == '4':
            group = str(input('Введите группу (2019-ГФ-ГиДЗакс-1б, 2019-ГФ-ГиДЗг-1б, 2019-ГФ-ГиДЗипр-1б, 2019-ГФ-ГиДЗкгин-1б, 2019-ГФ-ПГинж.г-1с, \
                                               2019-ГФ-ПГинж.г-2с, 2019-ГФ-ПГинж.г-3с, 2019-ГФ-ПГинж.г-4с, 2019-ГФ-ПГинж.г-5с)): '))
        elif str(kurs).strip() == '5':
            group = str(input('Введите группу (2018-ГФ-ПГинж.г-1с, 2018-ГФ-ПГинж.г-2с, 2018-ГФ-ПГинж.г-3с)): '))
        else:
            print('Неверный ввод')

    elif fak.strip().lower() == 'кф':
        kurs = str(input('Введите курс (1, 2, 3, 4, 5)): '))
        fak = 'КФ'
        if str(kurs).strip() == '1':
            group = str(input('Введите группу (2022-КФ-ГК-1асп, 2022-КФ-КиГ-1б, 2022-КФ-КиГ-1м, 2022-КФ-КиГ-2б, 2022-КФ-КиГ-2м, 2022-КФ-КиГ-3б, 2022-КФ-КиГ-4б)): '))
        elif str(kurs).strip() == '2':
            group = str(input('Введите группу (2021-КФ-К-1асп, 2021-КФ-КиГ-1б, 2021-КФ-КиГ-1м, 2021-КФ-КиГ-2б, 2021-КФ-КиГ-3б, 2021-КФ-КиГ-4б)): '))
        elif str(kurs).strip() == '3':
            group = str(input('Введите группу (2020-КФ-КиГ-1б, 2020-КФ-КиГ-2б, 2020-КФ-КиГ-3б, 2020-КФ-КиГ-4б)): '))
        elif str(kurs).strip() == '4':
            group = str(input('Введите группу (2019-КФ-КиГ-1б, 2019-КФ-КиГ-2б, 2019-КФ-КиГ-3б, 2019-КФ-КиГ-4б)): '))
        else:
            print('Неверный ввод')

    elif fak.strip().lower() == 'фаг':
        kurs = str(input('Введите курс (1, 2, 3, 4)): '))
        fak = 'ФАГ'
        if str(kurs).strip() == '1':
            group = str(input('Введите группу (2022-ФАиГ-АРХ-1б, 2022-ФАиГ-АРХ-1м, 2022-ФАиГ-АРХ-2м, 2022-ФАиГ-Градо-1б)): '))
        elif str(kurs).strip() == '2':
            group = str(input('Введите группу (2021-ФАиГ-АРХ-1б, 2021-ФАиГ-АРХ-1м, 2021-ФАиГ-Градо-1б)): '))
        elif str(kurs).strip() == '3':
            group = str(input('Введите группу (2020-ФАиГ-АРХ-1б, 2020-ФАиГ-АРХ-2б)): '))
        elif str(kurs).strip() == '4':
            group = str(input('Введите группу (2019-ФАиГ-АРХ-1б, 2019-ФАиГ-АРХ-2б)): '))
        elif str(kurs).strip() == '5':
            group = str(input('Введите группу (2018-ФАиГ-АРХ-1б, 2018-ФАиГ-АРХ-2б)): '))        
        else:
            print('Неверный ввод')

    elif fak.strip().lower() == 'фоп':
        kurs = str(input('Введите курс (1, 2, 3, 4, 5)): '))
        fak = 'ФОП'
        if str(kurs).strip() == '1':
            group = str(input('Введите группу (2022-ФОП-ЛТиЛТ-1б, 2022-ФОП-ОПТ-1б, 2022-ФОП-ОПТ-1м, 2022-ФОП-ОПТ-2м, 2022-ФОП-ОЭП-1асп, 2022-ФОП-ЭиОЭПиССН-1)): '))
        elif str(kurs).strip() == '2':
            group = str(input('Введите группу (2021-ФОП-ЛТиЛТ-1б, 2021-ФОП-ОПТ-1б, 2021-ФОП-ОПТ-1м, 2021-ФОП-ОЭПиС-1асп, 2021-ФОП-ЭиОЭПиССН-1)): '))
        elif str(kurs).strip() == '3':
            group = str(input('Введите группу (2020-ФОП-ЛТиЛТ-1б, 2020-ФОП-ОПТ-1б, 2020-ФОП-ЭиОЭПиССН-1)): '))
        elif str(kurs).strip() == '4':
            group = str(input('Введите группу (2019-ФОП-ЛТиЛТ-1б, 2019-ФОП-ОПТ-1б, 2019-ФОП-ЭиОЭПиССН-1)): '))
        elif str(kurs).strip() == '5':
            group = str(input('Введите группу (2018-ФОП-ЭиОЭПиССН-1)): '))
        else:
            print('Неверный ввод')

    elif fak.strip().lower() == 'фут':
        kurs = str(input('Введите курс (1, 2, 3, 4)): '))
        fak = 'ФУТ'
        if str(kurs).strip() == '1':
            group = str(input('Введите группу (2022-ФУТ-ЗиКзио-1б, 2022-ФУТ-ЗиКзио-1м, 2022-ФУТ-ЗиКкн-1б, 2022-ФУТ-ЗиКунирт-1м, 2022-ФУТ-ЗиКупр-1б, 2022-ФУТ-ЗКиМЗ-1асп, 2022-ФУТ-САиУ-1б, 2022-ФУТ-УК-1б)): '))
        elif str(kurs).strip() == '2':
            group = str(input('Введите группу (2021-ФУТ-ЗиКзио-1б, 2021-ФУТ-ЗиКзио-1м, 2021-ФУТ-ЗиКкн-1б, 2021-ФУТ-ЗиКунирт-1м, 2021-ФУТ-ЗиКупр-1б, 2021-ФУТ-ЗК-1асп (зо, 2021-ФУТ-ЗК-1асп (оч)): '))
        elif str(kurs).strip() == '3':
            group = str(input('Введите группу (2020-ФУТ-ЗиКзио-1б, 2020-ФУТ-ЗиКкн-1б, 2020-ФУТ-ЗиКупр-1б)): '))
        elif str(kurs).strip() == '4':
            group = str(input('Введите группу (2019-ФУТ-ЗиКзио-1б, 2019-ФУТ-ЗиКкн-1б, 2019-ФУТ-ЗиКупр-1б)): '))
        else:
            print('Неверный ввод')

    elif fak.strip().lower() == 'фгииб':
        kurs = str(input('Введите курс (1, 2, 3, 4)): '))
        fak = 'ФГиИБ'
        if str(kurs).strip() == '1':
            group = str(input('Введите группу (2022-ФГиИБ-ИБ-1б, 2022-ФГиИБ-ИБ-1м, 2022-ФГиИБ-ИБ-2б, 2022-ФГиИБ-ИСиТ-1б, 2022-ФГиИБ-ИСиТ-2б, 2022-ФГиИБ-ИСиТ-3б, \
                               2022-ФГиИБ-ИСиТиб ик, 2022-ФГиИБ-ПИ-1б, 2022-ФГиИБ-ПИ-2б, 2022-ФГиИБ-ПИабпд-1м)): '))
        elif str(kurs).strip() == '2':
            group = str(input('Введите группу (2021-ФГиИБ-Геоинф-1а, 2021-ФГиИБ-ИБ-1б, 2021-ФГиИБ-ИБ-2б, 2021-ФГиИБ-ИСиТ-1б, 2021-ФГиИБ-ИСиТ-2б, \
                                               2021-ФГиИБ-ИСиТгсит-, 2021-ФГиИБ-ИСиТиб ик, 2021-ФГиИБ-ПИ-1б)): '))
        elif str(kurs).strip() == '3':
            group = str(input('Введите группу (2020-ФГиИБ-ИБ-1б, 2020-ФГиИБ-ИБ-2б, 2020-ФГиИБ-ИСиТ-1б, 2020-ФГиИБ-ИСиТ-2б, 2020-ФГиИБ-ПИ-1б)): '))
        elif str(kurs).strip() == '4':
            group = str(input('Введите группу (2019-ФГиИБ-ИБ-1б, 2019-ФГиИБ-ИБ-2б, 2019-ФГиИБ-ИСиТ-1б, 2019-ФГиИБ-ИСиТ-2б, 2019-ФГиИБ-ПИ-1б)): '))
        else:
            print('Неверный ввод')
    else:
            print('Неверный ввод')
        

# def insert_db(data, fak, kurs, grup):
#     # global day, lesson, week, p_group, subject, teacher, aud, subj_type, comment
#     faculty = fak
#     course = kurs
#     group = grup
#     day = []
#     lesson = []
#     week = []
#     p_group = []
#     subject = []
#     teacher = []
#     aud = []
#     subj_type = []
#     comment = []

#     for element in data:
#         if len(element) <= 2:
#             del element

#         day.append(element[0])
#         lesson.append(element[1])
#         week.append(element[2])
#         p_group.append(element[3])
#         subject.append(element[4])
#         teacher.append(element[5])
#         aud.append(element[6])
#         subj_type.append(element[7])
#         comment.append(element[8])

#     # return print(f'Факультет {faculty} {len(faculty)} \n Курс {course} {len(course)} \n Группа {group} {len(group)} \nДень {day} {len(day)} \n Пары {lesson} {len(lesson)} \n Неделя {week} {len(week)} \n Подгруппа {p_group} {len(p_group)} \n Предмет {subject} {len(subject)} \n Препод {teacher} {len(teacher)} \n Аудитория {aud} {len(aud)} \n Тип {subj_type} {len(subj_type)} \n Коммент {comment} {len(comment)} \n')
#     # connection = sqlite3.connect('e_journal.db')
#     # cursor = connection.cursor()
#     # cursor.execute(""" 
#     #   INSERT INTO parse_schedule (faculty, course, full_group, week, day, number_lesson, subject, teacher, aud, subj_type, p_group)
#     #   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     # """, (faculty, course, group, week, day, lesson, subject, teacher, aud, subj_type, p_group))


if __name__ == '__main__':
    main_parser()