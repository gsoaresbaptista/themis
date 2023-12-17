import sqlite3
import random

if __name__ == '__main__':
    questions = [
        lambda number, code: f'O que diz o Artigo {number} do(a) {code}?',
        lambda number, code: f'Qual é a informação presente no Artigo {number} do(a) {code}?',
        lambda number, code: f'Explique o conteúdo do Artigo {number} do(a) {code}.',
        lambda number, code: f'Comente sobre o Artigo {number} do(a) {code}.',
        lambda number, code: f'Descreva o que está no Artigo {number} do(a) {code}.',
        lambda number, code: f'Discorra sobre o teor do Artigo {number} do(a) {code}.',
        lambda number, code: f'Peço informações sobre o Artigo {number} do(a) {code}.',
        lambda number, code: f'Gostaria de saber mais sobre o Artigo {number} do(a) {code}.',
        lambda number, code: f'Qual é o conteúdo presente no Artigo {number} do(a) {code}?',
        lambda number, code: f'Apresente os detalhes do Artigo {number} do(a) {code}.',
        lambda number, code: f'O Artigo {number} do(a) {code} trata de qual tema?',
        lambda number, code: f'Pode explicar o que consta no Artigo {number} do(a) {code}?',
        lambda number, code: f'Gostaria de entender o que está previsto no Artigo {number} do(a) {code}.',
        lambda number, code: f'Informe-me sobre o Artigo {number} do(a) {code}.',
        lambda number, code: f'Discuta as informações presentes no Artigo {number} do(a) {code}.',
        lambda number, code: f'No Artigo {number} do(a) {code}, qual é a disposição principal?',
        lambda number, code: f'Explique o conteúdo normativo presente no Artigo {number} do(a) {code}.',
        lambda number, code: f'O que se pode extrair do Artigo {number} do(a) {code}?',
        lambda number, code: f'Forneça uma análise do Artigo {number} do(a) {code}.',
        lambda number, code: f'Destaque as principais informações do Artigo {number} do(a) {code}.',
    ]

    db_path = 'data/sqlite/vade_mecum.db'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # execute a SELECT query
    query = f"SELECT * FROM codes"

    # execute the query and fetch all rows
    cursor.execute(query)
    rows = cursor.fetchall()

    # iterate over the rows
    tuples = []

    for row in rows:
        _, code, _, title, _, _, _, _, articles, notes  = row

        if title != 'Preâmbulo':
            article_number = articles.split(' ')[:2]

            if article_number[0] == 'Art.':
                number = article_number[1][:-1] if article_number[-1] == '.' else article_number[1]
                prompt = questions[random.choice(range(len(questions)))](number, code)
                tuples.append((prompt, f'{articles.strip()}\n{notes.strip()}'))

    # close the cursor and the connection
    cursor.close()
    connection.close()

    conn = sqlite3.connect(f'questions.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question TEXT,
            answer TEXT
        );
        """
    )

    for row in tuples:
        cursor.execute(
            'INSERT INTO questions (question, answer) VALUES (?, ?)',
            row
        )

    conn.commit()
    cursor.close()
    conn.close()
