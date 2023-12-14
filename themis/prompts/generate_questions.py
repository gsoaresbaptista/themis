import asyncio
import pandas as pd
from time import sleep
import g4f
import re
import sqlite3
from io import StringIO
import csv
from freeGPT import Client
from datetime import datetime, timedelta
from undetected_chromedriver import Chrome, ChromeOptions

options = ChromeOptions()
options.add_argument('--incognito')
webdriver = Chrome(options=options, headless=True, browser_executable_path='/usr/bin/chromium', driver_executable_path='/tmp/chromedriver')


responses = []
errors = []


def get_response(data):
    prompt = (
        'Dado o texto abaixo, crie uma pergunta com a resposta e retorne APENAS uma linha contendo '
        'a pergunta e resposta separadas por ;. Dê respostas completas e referencie o artigo que foi '
        'fornecido. Artigo: "'
        f'{data}\n"\n'
        '"'
    )

    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{'role': 'user', 'content': prompt}],
        webdriver=webdriver,
    )

    return response


def save_csv(response):
    responses.extend(response.split('\n'))

    # save to csv
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file, delimiter=';')

    for line in responses:
        csv_writer.writerow(line.split(';'))

    with open(csv_file_name, 'w', newline='') as file:
        file.write(csv_file.getvalue())


if __name__ == '__main__':
    csv_file_name = 'questions.csv'

    conn = sqlite3.connect('./data/sqlite/vade_mecum.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM codes')

    method = 'freegpt'

    for row in list(cursor)[::-1]:
        try:
            data = '\n'.join(
                [element for element in row[1:] if element is not None]
            )
            response = get_response(data)

        except KeyboardInterrupt as error:
            print([row[0] for row in errors])
            exit(0)

        except Exception as exception:
            print(exception)
            print('* Error in:', row)
            errors.append(row)
            webdriver.quit()
            options = ChromeOptions()
            options.add_argument('--incognito')
            webdriver = Chrome(options=options, headless=True, browser_executable_path='/usr/bin/chromium', driver_executable_path='/tmp/chromedriver')

        else:
            if (
                'GPT-3.5' in response
                or 'Claro, aqui está' in response
                or 'API failed' in response
            ):
                errors.append(row)
            else:
                save_csv(response)

    while errors:
        print('ERROR PROCESSING')
        row = errors[0]

        try:
            response = get_response(row)

        except KeyboardInterrupt as error:
            print([row[0] for row in errors])
            exit(0)

        except:
            pass

        else:
            if not (
                'GPT-3.5' in response
                or 'Claro, aqui está' in response
                or 'API failed' in response
            ):
                save_csv(response)
                errors.pop(0)
            else:
                webdriver.quit()
                options = ChromeOptions()
                options.add_argument('--incognito')
                webdriver = Chrome(options=options, headless=True, browser_executable_path='/usr/bin/chromium', driver_executable_path='/tmp/chromedriver')


    cursor.close()
    conn.close()
    webdriver.quit()
