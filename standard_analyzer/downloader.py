from urllib.request import urlopen
from urllib.parse import urlencode
from re import findall
from time import sleep
from typing import List
import paths

url = 'http://profstandart.rosmintrud.ru/obshchiy-informatsionnyy-blok/natsionalnyy-reestr-professionalnykh-standartov/' \
      'reestr-professionalnykh-standartov/'
url_pages = url + '?PAGEN_1='
url_standards = url + 'wservGenXMLSave.php'
pattern = br'''onclick="downloadXml\('(\d+)'\);"'''
page_count = 55
fresh_standards = []


def get_standard(standard_id: str):
    file = paths.downloaded(standard_id)

    # проверка, не был ли данный стандарт скачан ранее
    if file.exists():
        return

    fresh_standards.append(standard_id)
    sleep(5)  # пауза между запросами, чтобы избежать блокировки
    post_data = urlencode({"fn[]": standard_id}).encode()
    response = urlopen(url_standards, post_data)
    data = response.read()
    response.close()

    file.write(data, 'wb')


def get_list(page: int):
    sleep(5)  # пауза между запросами, чтобы избежать блокировки
    response = urlopen(url_pages + str(page))
    data = response.read()
    response.close()
    for standard_id in findall(pattern, data):
        get_standard(standard_id)


def update() -> List[str]:
    fresh_standards.clear()
    for i in range(1, page_count+1):
        get_list(i)
    return fresh_standards
