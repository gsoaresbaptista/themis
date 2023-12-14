import asyncio
import pandas as pd
from time import sleep
import g4f
import re


if __name__ == '__main__':
    csv_file_name = 'instructions.csv'
    responses = []
    prompt = (
        'Me dê uma lista com 10 frases enumeradas de instruções para um modelo de '
        'LLM que pedem para o  modelo responder uma questão '
        ' de múltipla escolha com a resposta correta. Exemplo: "Qual a alternativa correta? " '
        'Ou "Me responda a questao: " . A lista deve contar apenas as frases de prompts.'
    )

    pattern = re.compile(r'\d+\.\s*(.*)')

    for i in range(184):
        full_message = ''
        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        for message in response:
            print(message, flush=True, end='')
            full_message += message

        responses.append(pattern.findall(full_message))
        sleep(3)

        # clean data
        responses = [
            [item.replace('"', '') for item in row if item != '']
            for row in responses
        ]

        # save to csv
        df = pd.DataFrame({'prompts': responses})
        df.to_csv(csv_file_name, index=False, header=False)
