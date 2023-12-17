import sqlite3


if __name__ == '__main__':
    tuples = []

    for i in range(3):
        with open(f'cleaned/multi_choice_questions{i+1}.csv', 'r') as file:
            question_lines, answer_lines = '', ''
            question = True

            for line in file:
                if line == '!@#\n':
                    question = False
                    continue

                elif line == ';\n':
                    tuples.append((question_lines, answer_lines))
                    question = True
                    question_lines, answer_lines = '', ''
                    continue

                if question:
                    question_lines += line
                else:
                    answer_lines += line

    conn = sqlite3.connect(f'multiple_choice_questions.db')
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
