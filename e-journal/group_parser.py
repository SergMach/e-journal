import requests
from bs4 import BeautifulSoup
import sqlite3


def isit1():

    url_site = "http://studydep.miigaik.ru/index.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    dirty_data = list()
    fak = 'ФГиИБ' #str(input('Введите факультет (ГФ, КФ, ФГиИБ, ФАГ, )))
    kurs = '1'  
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
            print(ite)
            for iter in ite:
                one_data.append(iter.strip())
                print(len(one_data))
                if len(one_data) % 9 == 1:
                    day.append(iter)
                if len(one_data) % 9 == 2:
                    lesson.append(iter)
                if len(one_data) % 9 == 3:
                    week.append(iter)
                if len(one_data) % 9 == 4:
                    p_group.append(iter)
                if len(one_data) % 9 == 5:
                    subject.append(iter)
                if len(one_data) % 9 == 6:
                    teacher.append(iter)
                if len(one_data) % 9 == 7:
                    aud.append(iter)
                if len(one_data) % 9 == 8:
                    subj_type.append(iter)
                # if len(one_data) % 9 == 0:
                #     comment.append(iter)
            #print(f'Факультет {fak} {len(fak)} \n Курс {kurs} {len(kurs)} \n Группа {grup} {len(grup)} \nДень {day} {len(day)} \n Пары {lesson} {len(lesson)} \n Неделя {week} {len(week)} \n Подгруппа {p_group} {len(p_group)} \n Предмет {subject} {len(subject)} \n Препод {teacher} {len(teacher)} \n Аудитория {aud} {len(aud)} \n Тип {subj_type} {len(subj_type)} \n Коммент {comment} {len(comment)} \n')
    if len(day)==len(lesson)==len(week)==len(p_group)==len(subject)==len(teacher)==len(aud)==len(subj_type):
        # print(len(day))
        connection = sqlite3.connect('e_journal.db')
        cursor = connection.cursor()
        for num in range(1, len(day)):
            print(f'Факультет {fak}\n Курс {kurs}\n Группа {grup}\nДень {day[num]}\n Пары {lesson[num]}\n Неделя {week[num]}\n Подгруппа {p_group[num]}\n Предмет {subject[num]}\n Препод {teacher[num]}\n Аудитория {aud[num]}\n Тип {subj_type[num]}')
            # cursor.execute(""" 
            #     INSERT INTO parse_schedule (faculty, course, full_group, week, day, number_lesson, subject, teacher, aud, subj_type, p_group)
            #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            # """, (fak, kurs, grup, week, day, lesson, subject, teacher, aud, subj_type, p_group))

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




    return print(one_data)



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
    isit1()