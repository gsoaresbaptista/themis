import asyncio
import pandas as pd
from time import sleep
from freeGPT import AsyncClient

async def make_request(prompt):
    try:
        resp = await AsyncClient.create_completion('gpt3', prompt)
        return resp
    except Exception as e:
        return f'🤖: {e}'


def main():
    responses = []
    prompt = (
        'Me dê 10 variações de instruções para um modelo de LLM '
        'responder uma questão de múltipla escolha. Retorne apenas '
        'as instruções sem enumerá-las. '
        'Separe-as utilizando quebra de linha (\n).'
    )

    for i in range(1):
        response = asyncio.run(make_request(prompt))
        sleep(3)
        responses.append(response)

        # save to csv
        df = pd.DataFrame({'Prompt': responses.split(',')})
        df.to_csv('responses.csv', index=False)

if __name__ == '__main__':
    main()
