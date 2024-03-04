import csv
import json
import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from telegram_connect import bot_send_message


class Crawler:

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    # Basic Initial For Crawler
    def __init__(self, current_category, current_city):
        self.current_category = current_category
        self.current_city = current_city

    @classmethod
    def get_authorization_token(cls):
        token = ''
        while token == '':
            options = Options()
            options.add_argument('log-level=3')
            options.add_argument('--headless')
            options.page_load_strategy = 'normal'
            driver = webdriver.Edge(options=options)
            driver.get('https://www.olx.kz/')
            element = WebDriverWait(driver, 10).until(lambda driver: driver.execute_script
                                                                     ("return document.readyState") == "complete")
            time.sleep(10)
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'a_access_token':
                    token = cookie['value']
            driver.quit()
            # Check If Token Not Exist Raise False Expression
            if token != '':
                return token

    # Work With OLX API Server And Get Mobile Phone
    @classmethod
    def get_data_from_offer(cls, offer, apikey, bearer_token):
        params = {
            'url': f"https://www.olx.kz/api/v1/offers/{offer}/limited-phones/",
            'apikey': apikey,
            'custom_headers': 'true',
        }
        headers = {
            'Authorization': f'Bearer {bearer_token}',
        }
        response = requests.get('https://api.zenrows.com/v1/', params=params, headers=headers)
        return response.json()

    # Fetch Username and Location From OLX
    @classmethod
    def get_user_data(cls, url):
        options = Options()
        options.add_argument('log-level=3')
        options.add_argument('--headless')
        driver = webdriver.Edge(options=options)
        driver.get(f'https://www.olx.kz{url}')

        try:
            close_note = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'css-spwpto')))
            close_note.click()
        except Exception:
            pass
        try:
            close_note = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="dismiss-cookies-overlay"]')))
            close_note.click()
        except Exception:
            pass
        try:
            username_element = driver.find_element(By.CLASS_NAME, 'css-1lcz6o7')
            username = username_element.text
        except Exception:
            username = 'NOT FOUND'
        try:
            city_element = driver.find_element(By.CLASS_NAME, 'css-1cju8pu')
            city = city_element.text.replace(',', '')
        except Exception:
            city = 'NOT FOUND'

        return username, city

    def get_data(self):
        id_counter = 1
        bearer_token_counter = 1

        if not os.path.exists(f"OLX_DATA/{self.current_category}_{self.current_city}.csv"):
            with open(f'OLX_DATA/{self.current_category}_{self.current_city}.csv', 'w', encoding='utf-8', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(['NAME', 'CITY', 'PHONE NUMBER'])

        with open(f'OLX_IDS/{self.current_category}_{self.current_city}.json', 'r', encoding='utf-8') as json_file:
            offers = json.load(json_file)

        bearer_token = self.get_authorization_token()
        api = input('ENTER YOUR ZENROWS API KEY: ')

        for offer_index in range(0, len(offers)):

            phone_data = self.get_data_from_offer(offers[offer_index]['id'], api, bearer_token)

            try:
                while phone_data['code'] == 'AUTH002':
                    print('YOU ENTER NOT CORRECT ZENROWS API KEY')
                    api = input('ENTER YOUR ZENROWS API KEY: ')
                    phone_data = self.get_data_from_offer(offers[offer_index]['id'], api, bearer_token)
            except Exception as e:
                pass

            if bearer_token_counter > 30:
                bearer_token = self.get_authorization_token()
                bearer_token_counter = 0

            try:
                name, city = self.get_user_data(offers[offer_index]['url'])
                phone = phone_data['data']['phones'][0]

                # Write Data To CSV FILE
                with open(f'OLX_DATA/{self.current_category}_{self.current_city}.csv', 'a', encoding='utf-8',
                          newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow([name, city, phone])
            except Exception as e:
                print(f"[OLX API ERROR] ERROR IN GET NUMBER PROCESS")

            with open(f'OLX_IDS/{self.current_category}_{self.current_city}.json', 'w', encoding='utf-8') as json_file:
                json.dump(offers[offer_index:], json_file, indent=4, ensure_ascii=False)

            print(f'[COMPLETE] {id_counter} | {len(offers)}')
            bearer_token_counter += 1
            id_counter += 1