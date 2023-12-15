import g4f
import sqlite3
import csv
from undetected_chromedriver import Chrome, ChromeOptions
import random


responses = []
errors = []


def get_response(data, webdriver):
    prompt = (
        'Com base no texto fornecido, elabore uma pergunta de múltipla escolha com 5 opções (letras A a E). '
        'Além disso, forneça uma resposta comentada explicando por que a opção escolhida está correta. '
        'Evite perguntas sobre títulos. Artigo: "'
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
    webdriver = Chrome(options=options, headless=True)

    conn = sqlite3.connect('./data/sqlite/vade_mecum.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM codes')

    articles = list(cursor)
    random.shuffle(articles)

    for row in articles:
        try:
            data = '\n'.join(
                [element for element in row[1:] if element is not None]
            )
            response = get_response(data, webdriver)

        except KeyboardInterrupt:
            print([row[0] for row in errors])
            exit(0)

        except Exception as exception:
            print(exception)
            print('* Error in:', row)
            errors.append(row)
            webdriver.quit()
            options = ChromeOptions()
            options.add_argument('--incognito')
            webdriver = Chrome(options=options, headless=True)

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

        except KeyboardInterrupt:
            print([row[0] for row in errors])
            exit(0)

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
                webdriver = Chrome(options=options, headless=True)

    cursor.close()
    conn.close()
    webdriver.quit()
