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


responses = []
errors = []


def get_response(data, webdriver):
    prompt = (
        'Dado o texto abaixo, crie uma pergunta de múltipla escolha com 5 letras, de A até E. '
        'Também retorne a resposta comentada da questão, indicando porque foi escolhido aquela letra. '
        'Não faça perguntas sobre títulos. Artigo: "'
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
    with open(csv_file_name, 'a', newline='') as file:
        csv_writer = csv.writer(file, delimiter=';')
        for line in response.split('\n'):
            csv_writer.writerow(line.split(';'))


if __name__ == '__main__':
    csv_file_name = 'multi_choice_questions.csv'

    options = ChromeOptions()
    options.add_argument('--incognito')
    webdriver = Chrome(options=options, headless=True, browser_executable_path='/usr/bin/chromium', driver_executable_path='/tmp/chromedriver')

    conn = sqlite3.connect('./data/sqlite/vade_mecum.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM codes')

    method = 'freegpt'

    for row in list(cursor)[::-1]:
        try:
            data = '\n'.join(
                [element for element in row[1:] if element is not None]
            )
            response = get_response(data, webdriver)

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
                or 'VoiGPT.com' in response
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
            response = get_response(row, webdriver)

        except KeyboardInterrupt as error:
            print([row[0] for row in errors])
            exit(0)

        except:
            pass

        else:
            if not (
                'GPT-3.5' in response
                or 'VoiGPT.com' in response
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
