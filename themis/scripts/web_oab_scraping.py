from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import WebDriverException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    '--disable-notifications'
)  # Para desabilitar notificações, se necessário
chrome_options.add_argument(
    '--disable-popup-blocking'
)  # Para desabilitar o bloqueio de pop-ups

driver = webdriver.Chrome(options=chrome_options)


provas = [
    'xxxv',
    'xxxiv',
    'xxxiii',
    'xxxii',
    'xxxi',
    'xxx',
    'xxix',
    'xxviii',
    'xxvii',
    'xxvi',
    'xxv',
    'xxiv',
    'xxiii',
    'xxii',
    'xxi',
    'xx',
    'xix',
    'xviii',
    'xvii',
    'xvi',
    'xv',
    'xiv',
    'xiii',
]

dict_questions = {
    'Prova': [],
    'Numero_Questao': [],
    'Enunciado': [],
    'Alternativa_A': [],
    'Alternativa_B': [],
    'Alternativa_C': [],
    'Alternativa_D': [],
    'Alternativa_Correta': [],
    'Justificativa': [],
}

for i, prova in enumerate(provas):
    print(
        f'https://vademecumbrasil.com.br/estudo-primeira-fase/oab-exame-{prova}'
    )
    driver.get(
        f'https://vademecumbrasil.com.br/estudo-primeira-fase/oab-exame-{prova}'
    )

    if i == 0:
        try:
            # Encontrar o botão "Aceitar todos os cookies" e clicar nele
            accept_button = driver.find_element(By.CLASS_NAME, 'cc-nb-okagree')
            accept_button.click()
        except Exception as e:
            print(f'Erro ao clicar no botão de aceitar cookies: {str(e)}')
            exit()

    flag = 0
    while True:
        show_answer_bts = driver.find_elements(
            By.CLASS_NAME, 'btn.btn-info.mb-3'
        )

        for i in range(len(show_answer_bts)):
            driver.execute_script(
                'arguments[0].scrollIntoView();', show_answer_bts[i]
            )
            driver.execute_script('arguments[0].click();', show_answer_bts[i])
            sleep(1)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        full_html_questions = soup.find_all('div', {'class': 'rcorners2'})

        for i, question in enumerate(full_html_questions):
            dict_questions['Prova'].append(prova)

            div_justificativa = question.find('div', {'class': 'item-content'})
            dict_questions['Alternativa_Correta'].append(
                div_justificativa.find('span').text
            )
            dict_questions['Justificativa'].append(
                '\n'.join(
                    [item.text for item in div_justificativa.find_all('p')]
                )
            )

            all_spans = question.find_all('span')
            dict_questions['Numero_Questao'].append(all_spans[1].text)

            ps_enunciado = all_spans[2].find_all('p')
            dict_questions['Enunciado'].append(
                '\n'.join([item.text for item in ps_enunciado])
            )

            spans_alternativas = all_spans[3:-1]
            alternativa_options = [
                'Alternativa_A',
                'Alternativa_B',
                'Alternativa_C',
                'Alternativa_D',
            ]

            for alternativa, nome_coluna in zip(
                spans_alternativas, alternativa_options
            ):
                dict_questions[nome_coluna].append(
                    alternativa.find_next('p').text
                )

        if flag == 9:
            break

        paginate_button = driver.find_element(
            By.CLASS_NAME, 'paginate_button.next'
        )
        driver.execute_script(
            'arguments[0].scrollIntoView();', paginate_button
        )
        sleep(1)

        paginate_button.click()
        flag += 1


if __name__ == '__main__':
    csv_file_path = 'oab_provas.csv'
    db_file_path = 'oab_provas.db'

    df = pd.DataFrame(dict_questions)
    df.to_csv(csv_file_path, index=False)
    create_database_and_insert_data(csv_file_path, db_file_path)
