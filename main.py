

import requests # нужен запросы, обращаться сайт, статус и т.п
from bs4 import BeautifulSoup # парсинг, собрирать данные и многое другое
import csv # таблица данных, лучше чем в терминале))


# Resources [https://codeby.net/resources/categories/brending-codeby.11/]
# Domain [https://codeby.net/]
# Block Resource(test): DIV structItem structItem--resource is-prefix2  js-inlineModContainer js-resourceListItem-896
# All block resources: structItem-cell structItem-cell--icon structItem-cell--iconExpanded

CSV = 'resources.csv'
HOST = "https://codeby.net/"
URL = "https://codeby.net/resources/categories/brending-codeby.11/"
pages = requests.get(URL)
# User-Agent Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0
# ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
HEADERS = {

    "accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
}

# подключение к странице
def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# полученные html элементы: парсим с bs4
def get_content(html):
    soup = BeautifulSoup(pages.text, 'html.parser')
    items = soup.find_all("div", class_="structItem")
    resources = [] # место где добавляются ресурсы


# цикл: перебираем все данные ресурса включая:(Название ресурса, автор, дата создание)
    for item in items:
        resources.append(
            {

                "title":item.find("div", class_="structItem-title").get_text(), # название ресурса
                "author": item.find("a", class_="username").get_text(), # автор ресурса
                "time": item.find("time", class_="u-dt").get_text(), # дата создание ресурса
                "desc": item.find("div", class_="structItem-resourceTagLine").get_text() # описание ресурса
            }

        )

    return resources


def save_documents_csv(items, path):
    with open(path, "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(['Название ресурсов', "Автор ресурсов", "Дата создание ресурсов", "Описание"])
        resources = []

        for item in items:
            writer.writerow([item['title'], item["author"], item["time"], item["desc"]])

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        resource = []
        resource.extend(get_content(html.text))
        save_documents_csv(resource, CSV)
    #print(get_content(html))
    #save_documents_csv(CSV)
parser()

