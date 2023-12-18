import sqlite3
import re

if __name__ == '__main__':
    tuples = []

    for i in range(11):
        if i != 2:
            with open(f'cleaned/questions{i+1}_tratado.csv', 'r') as file:
                for j, line in enumerate(file):
                    try:
                        qa_pairs = re.split(r'\?\;', line)
                        tuples.append(((qa_pairs[0] + '?').replace('\'', '"').strip('"'), qa_pairs[1].replace('\'', '"').strip('"')))
                    except IndexError:
                        print(f'Error in line {j + 1}, file: {i + 1}')

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
