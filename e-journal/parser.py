import requests
from bs4 import BeautifulSoup
import datetime
import config

#получаем список факультетов
def get_facultet():
    """получаем список факультетов из выпадающего списка"""
    data = requests.get(url=config.url_site, headers=config.headers)
    soup = BeautifulSoup(data.text, 'lxml')
    items = soup.select('[name=fak] option[value]')
    list_fak = [item.get('value') for item in items]
    #list_fak_text = [item.text for item in items]
    del list_fak[0]
    return list_fak

#получаем список курсов
def get_kurs(facultet:str):
    """получаем список курсов из выпадающего списка"""
    data = requests.post(url=config.url_site, data={'fak':facultet}, headers = config.headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    items = soup.select('[name=kurs] option[value]')
    list_kurs = [item.get('value') for item in items]
    #list_kurs = [item.text for item in items]
    del list_kurs[0]
    return list_kurs

#получаем список групп
def get_group(facultet:str, kurs:str):
    """получаем список групп из выпадающего списка"""
    data = requests.post(url=config.url_site, data={'fak':facultet, "kurs":kurs}, headers = config.headers)
    soup = BeautifulSoup(data.text, 'lxml')
    items = soup.select('[name=grup] option[value]')
    list_group = [item.get('value') for item in items]
    #list_kurs = [item.text for item in items]
    del list_group[0]
    return list_group

#получаем неделю(верх/низ)
def get_week():
    data = requests.get(url=config.url_site, headers=config.headers)
    soup = BeautifulSoup(data.text, 'lxml')
    items =str(soup.find_all("td", attrs={"class":"left-content"}))
    index = items.find("неделя: ")
    week = items[index+8:index+16].replace(' ', '').lower()
    return week

def get_schedule(facultet:str, kurs:str, group:str):
    """Получаем всё расписанятий целиком без форматирования (вся табличка в html)
    Args:
        facultet - шифр факультета
        kurs - номер курса (в str)
        group - шифр группы
    """
    data = requests.post(url=config.url_site, data={'fak':facultet, 'kurs':kurs, 'grup':group}, headers = config.headers)
    soup = BeautifulSoup(data.text, 'lxml')

    """ Читаем разметку таблицы по строкам - пишем строки в list """
    schedule=[]
    for table in soup.find('table',attrs={"class":"t"}).find_all('tr'):
        rows = [row.text for row in table.find_all('td')]
        schedule.append(rows)
    return schedule
