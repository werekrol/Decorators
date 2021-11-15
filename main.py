import datetime
import json
import requests
import time
import os

def logger(log_path):
    def decorator(search_countries):
        def new_search_countries(*args, **kwargs):
            date_today = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
            start = time.time()
            result = search_countries(*args, **kwargs)
            finish = time.time() - start
            with open(log_path, 'a', encoding='utf-8') as ouf:

                ouf.write(f'Дата и время вызова функции - {date_today}' + '\n')
                ouf.write(f'Аргументы функции - {args}, {kwargs}' + '\n')
                ouf.write(f'Результат - {result}' + '\n')
                ouf.write(f'Время работы функции - {finish}' + '\n')
                ouf.write(f'Путь к логам - {os.path.abspath(log_path)}')
            return result
        return new_search_countries
    return decorator


@logger('logs.txt')
def search_countries(file_path, search):
    country_dict = {}
    with open(file_path, encoding='utf-8') as f:
        json_data = json.load(f)
        country_list = [country["name"]["common"] for country in json_data]
        for country in country_list:
            if search in country:
                url = 'https://en.wikipedia.org/wiki/' + '_'.join(country.split(' '))
                r = requests.head(url)
                if r.status_code == 200:
                    country_dict[country] = url
                else:
                    print(f'{country} - Ошибка')

    return country_dict

search_countries('countries.json', 'Islands')