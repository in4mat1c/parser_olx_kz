import json
import os
import requests

from bs4 import BeautifulSoup


def gather_data(city, category):
    print('[INFO] START GATHER ID FUNCTION:')
    links_counter = 1
    links = []
    if not os.path.exists('OLX_IDS'):
        os.mkdir('OLX_IDS')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    }

    # Raise When Problem With Internet Connection
    try:
        url = f'https://www.olx.kz/{category}/{city}/'
        url_response = requests.get(url=url, headers=headers)
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] YOU HAVE BAD INTERNET CONNECTION")
        exit()

    # Raise When Category is Empty
    try:
        soup = BeautifulSoup(url_response.text, 'lxml')
        inner_url_links = soup.find('ul', {'data-testid': 'category-count-links'}).find_all('li')
    except AttributeError:
        print(f"[ERROR] CATEGORY {category.upper()} IN {city.upper()} DON'T HAVE ANY DATA")
        exit()

    for inner_url_link in inner_url_links:
        inner_url = 'https://www.olx.kz' + inner_url_link.find('a').get('href')
        inner_url_response = requests.get(url=inner_url, headers=headers)
        soup = BeautifulSoup(inner_url_response.text, 'lxml')

        # If Pagination Not Find We Use Only First Page To Gather Data
        try:
            page_count = (soup.find_all('li', {'data-testid': 'pagination-list-item'}))[-1].text
        except IndexError:
            page_count = 1

        for page_index in range(1, int(page_count) + 1):
            inner_page_url = inner_url + '?page=' + str(page_index)
            inner_page_url_response = requests.get(url=inner_page_url, headers=headers)
            soup = BeautifulSoup(inner_page_url_response.text, 'lxml')
            cards = soup.find_all('div', {'data-cy': 'l-card'})

            for card in cards:
                # Try To Collect Only Ids From Grid
                try:
                    if int(card.get('id')):
                        links.append(
                            {
                                'url': card.find('a').get('href'),
                                'id': card.get('id')
                            }
                        )
                except (TypeError, ValueError):
                    pass

        print(f'[COMPLETE] {links_counter} | {len(inner_url_links)}')
        links_counter += 1

    with open(f'OLX_IDS/{category}_{city}.json', 'w', encoding='utf-8') as json_file:
        json.dump(links, json_file, indent=4, ensure_ascii=False)

    print(f'[FULL COMPLETE] IDS IN {category.upper()} IS GATHER')
