import json
import os

from ids_gather import gather_data
from crawler import Crawler
from telegram_connect import write_token, read_token


if __name__ == '__main__':
    if not os.path.exists('OLX_DATA'):
        os.mkdir('OLX_DATA')

    print('''
///////////////////////////////////////////////////////////////////
_   _ ______ _____ _   _ _  _   __  __       _______ _____ _____ 
| \ | |  ____|_   _| \ | | || | |  \/  |   /\|__   __|_   _/ ____|
|  \| | |__    | | |  \| | || |_| \  / |  /  \  | |    | || |     
| . ` |  __|   | | | . ` |__   _| |\/| | / /\ \ | |    | || |     
| |\  | |____ _| |_| |\  |  | | | |  | |/ ____ \| |   _| || |____ 
|_| \_|______|_____|_| \_|  |_| |_|  |_/_/    \_\_|  |_____\_____|

///////////////////////////////////////////////////////////////////
    ''')
    print('''
CITY CODE:
1 -> ABAYSKAYA OBLAST
2 -> AKMOLINSKAYA OBLAST
3 -> AKTUBINSKAYA OBLAST
4 -> ALMATINSKAYA OBLAST
5 -> ATYRAUSKAYA OBLAST
6 -> VOSTOCHNO-KAZAHSTANSKAYA OBLAST
7 -> JAMBYLSKAYA OBLAST
8 -> JETISUSKAYA OBLAST
9 -> ZAPADNO-KAZAHSTANSKAYA OBLAST
10 -> KARAGANDINSKAYA OBLAST
11 -> KOSTANAYSKAYA OBLAST
12 -> KYZYLORDINSKAYA OBLAST
13 -> MANGISTAUSKAYA OBLAST
14 -> PAVLODARSKAYA OBLAST
15 -> SEVERO-KAZAHSTANSKAYA OBLAST
16 -> TURKESTANSKAYA OBLAST 
17 -> ULYTAUSKAYA OBLAST
    ''')
    current_city = input('CHOOSE CURRENT CITY TO PARSE: ')
    match current_city:
        case '1':
            current_city = 'abay'
        case '2':
            current_city = 'akm'
        case '3':
            current_city = 'akt'
        case '4':
            current_city = 'alm'
        case '5':
            current_city = 'atr'
        case '6':
            current_city = 'vko'
        case '7':
            current_city = 'zhm'
        case '8':
            current_city = 'zhetisu'
        case '9':
            current_city = 'zko'
        case '10':
            current_city = 'kar'
        case '11':
            current_city = 'kus'
        case '12':
            current_city = 'kyz'
        case '13':
            current_city = 'man'
        case '14':
            current_city = 'pav'
        case '15':
            current_city = 'sko'
        case '16':
            current_city = 'uko'
        case '17':
            current_city = 'ulytau'
        case _:
            print('[ERROR] CITY NOT FOUND')
            exit()

    print('''
    SELECT CATEGORY:
    1 -> USLUGI
    2 -> STROITELSTVO
    3 -> ARENDA
    4 -> NEDVIZHIMOST
    5 -> ELECTRONIKA
    6 -> DOM I SAD
    7 -> RABOTA
    8 -> MODA
    9 -> DETSKII MIR
    10 -> HOBBY
    11 -> TRANSPORT
    12 -> ZHIVOTNIE
    13 -> OTDAM DAROM
        ''')

    current_category = input('CHOOSE CATEGORY TO PARSE: ')

    match current_category:
        case '1':
            current_category = 'uslugi'
        case '2':
            current_category = 'stroitelstvo-remont'
        case '3':
            current_category = 'prokat-tovarov'
        case '4':
            current_category = 'nedvizhimost'
        case '5':
            current_category = 'elektronika'
        case '6':
            current_category = 'dom-i-sad'
        case '7':
            current_category = 'rabota'
        case '8':
            current_category = 'moda-i-stil'
        case '9':
            current_category = 'detskiy-mir'
        case '10':
            current_category = 'hobbi-otdyh-i-sport'
        case '11':
            current_category = 'transport'
        case '12':
            current_category = 'zhivotnye'
        case '13':
            current_category = 'otdam-darom'
        case _:
            print('[ERROR] CATEGORY NOT FOUND')
            exit()

    try:
        with open(f'OLX_IDS/{current_category}_{current_city}.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    except json.decoder.JSONDecodeError:
        json_data = ''
    except FileNotFoundError:
        json_data = ''

    if len(json_data) < 1:
        gather_data(current_city, current_category)
    else:
        print(f'[INFO] {current_category.upper()}_{current_city.upper()}.JSON IS EXIST CONTINUE GET DATA FROM FILE')

    crawler = Crawler(current_category, current_city)
    crawler.get_data()
