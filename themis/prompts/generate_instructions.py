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
webdriver = Chrome(options=options, headless=True)


responses = []
errors = []


def get_response():
    prompt = (
        'Me dê uma lista com 10 frases enumeradas de instruções para um modelo de '
        'LLM que pedem para o  modelo responder uma questão '
        ' de múltipla escolha com a resposta correta. Exemplo: "Qual a alternativa correta? " '
        'Ou "Me responda a questao: " . A lista deve contar apenas as frases de prompts.'
    )

    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{'role': 'user', 'content': prompt}],
        webdriver=webdriver,
    )

    return response


def save_csv(response):
    responses.extend(response)

    with open(csv_file_name, 'a', newline='\n') as file:
        file.write(response)


if __name__ == '__main__':
    csv_file_name = 'instructions.csv'

    for i in range(1000):
        try:
            response = get_response()
    
        except KeyboardInterrupt as error:
            break

        except Exception as exception:
            print(exception)
            print('* Error in:')
            errors.append(0)
            webdriver.quit()
            options = ChromeOptions()
            options.add_argument('--incognito')
            webdriver = Chrome(options=options, headless=True)

        else:
            if (
                'GPT-3.5' in response
                or 'Claro, aqui está' in response
                or 'API failed' in response
            ):
                errors.append(0)
            else:
                print(i)
                save_csv(response)

    while errors:
        print('ERROR PROCESSING')
        row = errors[0]

        try:
            response = get_response(row)

        except KeyboardInterrupt as error:
            break

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
                webdriver = Chrome(options=options, headless=True)


    webdriver.quit()
