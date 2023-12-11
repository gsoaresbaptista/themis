from freeGPT import AsyncClient
from asyncio import run


async def main():
    while True:
        prompt = input('👦: ')
        try:
            resp = await AsyncClient.create_completion('gpt3', prompt)
            print(f'🤖: {resp}')
        except Exception as e:
            print(f'🤖: {e}')


run(main())
