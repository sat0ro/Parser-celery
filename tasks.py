import requests
import re
from bs4 import BeautifulSoup
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')
publish_date_pattern = r"<publishDTInEIS>(.+)<\/publishDTInEIS>"

base_url = 'https://zakupki.gov.ru'
headers = {'User-Agent': 'Mozilla/5.0'}


@app.task
def collect_links(page_url):
    links = []
    response = requests.get(page_url, headers=headers)
    if response.status_code != 200:
        print(f'Ошибка при получении html страницы {response.status_code}')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    find_a_link = soup.find_all('a', {'href': re.compile(r"/view.html\?regNumber")})

    for link in find_a_link:
        link_href = f'{base_url}{link.get("href")}'
        link_xml = link_href.replace('view.html', 'viewXml.html')
        links.append(link_xml)

    return links


@app.task
def parse_xml_form(xml_link):
    response = requests.get(xml_link, headers=headers)
    if response.status_code != 200:
        print(f'Ошибка {response.status_code} для {xml_link}')
        return f'{xml_link} - None'

    publish_date = re.findall(publish_date_pattern, response.text)

    if len(publish_date) > 0:
        return f'{xml_link} - {publish_date[0]}'
    else:
        return f'{xml_link} - None'