import requests
from bs4 import BeautifulSoup
import json
import sqlite3

def main():
    faculties = ['ГФ', 'КФ', 'ФАГ', 'ФОП', 'ФУТ', 'ФГиИБ', 'ЗФ']
    courses = ['1', '2', '3', '4', '5', '6']
    groups = ['2022-ГФ-АКС-1асп', '2022-ГФ-Г-1асп', '2022-ГФ-ГиДЗакс-1б', '2022-ГФ-ГиДЗакс-1м', '2022-ГФ-ГиДЗг-1б', '2022-ГФ-ГиДЗг-1м', '2022-ГФ-ГиДЗипр-1б', \
              '2022-ГФ-ГиДЗкгин-1б', '2022-ГФ-ПГинж.г-1с', '2022-ГФ-ПГинж.г-2с', '2022-ГФ-ПГинж.г-3с', '2022-ГФ-ПГинж.г-4с', '2022-ГФ-ПГинж.г-5с']
    # while True:

def insert_db():
    connection = sqlite3.connect('e_journal.db')
    cursor = connection.cursor()
    # cursor.execute(""" 
    #   INSERT INTO parse_schedule (parse_id, faculty, course, full_group, week, day, number_lesson, subject, teacher, aud, subj_type, p_group)
    #   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    # """, ())

if __name__ == '__main__':
    main()


def get_timetable():

    url_site = "http://studydep.miigaik.ru/index.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    # week_list={"1":"Понедельник", "2":"Вторник", "3":"Среда", "4":"Четверг", "5":"Пятница", "6":"Суббота", "7":"Воскресенье"}

    # """Получаем неделю(верх/низ)"""
    # data_week = requests.get(url=url_site, headers=headers)
    # soup_week = BeautifulSoup(data_week.text, 'lxml')
    # items_week = str(soup_week.find_all("td", attrs={"class":"left-content"}))
    # index_week = items_week.find("неделя: ")
    # week = items_week[index_week+8:index_week+16].replace(' ', '').lower()
    data = []
    list_fak = []
    list_kurs = []
    """получаем список факультетов из выпадающего списка"""
    data_fak = requests.get(url=url_site, headers=headers)
    soup_fak = BeautifulSoup(data_fak.text, 'lxml')
    items_fak = soup_fak.select('[name=fak] option[value]')
    del items_fak[0]
    for i in items_fak:
        list_fak.append(i.get('value'))
        #list_fak = [item.get('value') for item in items_fak]
        #list_fak_text = [item.text for item in items]
        #del list_fac[0]
        data.append(i.get('value'))
        #print(list_fak, type(list_fak))


    # return (print(data, '\n\n', data_fak, '\n\n',  soup_fak, '\n\n',  items_fak, '\n\n',  list_fak))
        """получаем список курсов из выпадающего списка"""
        
        for f in list_fak:
            data_kurs = requests.post(url=url_site, data={'fak':f}, headers=headers)
            soup_kurs = BeautifulSoup(data_kurs.text, 'html.parser')
            print(soup_kurs)
            items_kurs = soup_kurs.select('[name=kurs] option[value]')
            del items_kurs[0]
            #for j in range(items_fak.index(i)+1, len(items_kurs)):
            cnt = 0
            for it in items_kurs:
                
                cnt += 1
                #if items_kurs.index(it) > j:
                #print(len(items_kurs))
                print(it.get('value'))
                list_kurs.append(it.get('value'))
                #list_kurs = [item.get('value') for item in items_kurs]
                #list_kurs = [item.text for item in items]
                #data.append(it.get('value'))
                print(data.append(it.get('value')))
                
                print(list_kurs)
                print(list_fak)
                
            print(type(items_kurs))


                

                

    return print(data)

    #     """получаем список групп из выпадающего списка"""
    #     for k in list_kurs:
    #         data_group = requests.post(url=url_site, data={'fak':f, "kurs":k}, headers=headers)
    #         soup_group = BeautifulSoup(data_group.text, 'lxml')
    #         items_group = soup_group.select('[name=grup] option[value]')
    #         list_group = [item.get('value') for item in items_group]
    #         #list_kurs = [item.text for item in items]
    #         del list_group[0]
    #         data.append(list_group)

    #         # Получаем всё расписанятий целиком без форматирования (вся табличка в html)
    #         # Args:
    #         # facultet - шифр факультета
    #         # kurs - номер курса (в str)
    #         # group - шифр группы

    #         for g in list_group:
    #             data_schedule = requests.post(url=url_site, data={'fak':f, 'kurs':k, 'grup':g}, headers=headers)
    #             soup_schedule = BeautifulSoup(data_schedule.text, 'lxml')
    #             """ Читаем разметку таблицы по строкам - пишем строки в list """
    #             schedule=[]
    #             for table_scedule in soup_schedule.find('table',attrs={"class":"t"}).find_all('tr'):
    #                 rows_schedule = [row_schedule.text for row_schedule in table_scedule.find_all('td')]
    #                 schedule.append(rows_schedule)
    #                 data.append(schedule)

    # return data

print(get_timetable())
# get_timetable()