import requests
from bs4 import BeautifulSoup
import json

#получаем список факультетов
def get_timetable():

    url_site = "http://studydep.miigaik.ru/index.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    week_list={"1":"Понедельник", "2":"Вторник", "3":"Среда", "4":"Четверг", "5":"Пятница", "6":"Суббота", "7":"Воскресенье"}

    # """Получаем неделю(верх/низ)"""
    # data_week = requests.get(url=url_site, headers=headers)
    # soup_week = BeautifulSoup(data_week.text, 'lxml')
    # items_week = str(soup_week.find_all("td", attrs={"class":"left-content"}))
    # index_week = items_week.find("неделя: ")
    # week = items_week[index_week+8:index_week+16].replace(' ', '').lower()
    data = []
    """получаем список факультетов из выпадающего списка"""
    data_fac = requests.get(url=url_site, headers=headers)
    soup_fac = BeautifulSoup(data_fac.text, 'lxml')
    items_fac = soup_fac.select('[name=fak] option[value]')
    list_fak = [item.get('value') for item in items_fac]
    #list_fak_text = [item.text for item in items]
    del list_fak[0]
    data.append(list_fak)

    """получаем список курсов из выпадающего списка"""
    for f in list_fak:
        data_kurs = requests.post(url=url_site, data={'fak':f}, headers = headers)
        soup_kurs = BeautifulSoup(data_kurs.text, 'html.parser')
        items_kurs = soup_kurs.select('[name=kurs] option[value]')
        list_kurs = [item.get('value') for item in items_kurs]
        #list_kurs = [item.text for item in items]
        del list_kurs[0]
        data.append(list_kurs)

        """получаем список групп из выпадающего списка"""
        for k in list_kurs:
            data_group = requests.post(url=url_site, data={'fak':f, "kurs":k}, headers=headers)
            soup_group = BeautifulSoup(data_group.text, 'lxml')
            items_group = soup_group.select('[name=grup] option[value]')
            list_group = [item.get('value') for item in items_group]
            #list_kurs = [item.text for item in items]
            del list_group[0]
            data.append(list_group)

            """Получаем всё расписанятий целиком без форматирования (вся табличка в html)
            Args:
            facultet - шифр факультета
            kurs - номер курса (в str)
            group - шифр группы"""
            for g in list_group:
                data_schedule = requests.post(url=url_site, data={'fak':f, 'kurs':k, 'grup':g}, headers=headers)
                soup_schedule = BeautifulSoup(data_schedule.text, 'lxml')
                """ Читаем разметку таблицы по строкам - пишем строки в list """
                schedule=[]
                for table_scedule in soup_schedule.find('table',attrs={"class":"t"}).find_all('tr'):
                    rows_schedule = [row_schedule.text for row_schedule in table_scedule.find_all('td')]
                    schedule.append(rows_schedule)
                    data.append(schedule)

    return data

get_timetable()