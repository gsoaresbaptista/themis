import sqlite3

if __name__ == '__main__':
    db_path = 'data/sqlite/oab_provas.db'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    table_name = 'oab_provas'

    # execute a SELECT query
    query = f"SELECT * FROM {table_name}"

    # execute the query and fetch all rows
    cursor.execute(query)
    rows = cursor.fetchall()

    # iterate over the rows
    tuples = []

    for row in rows:
        _, _, _, enum, a, b, c, d, correct, just = row
        tuples.append((f'{enum}\nA) {a}\nB) {b}\nC) {c}\nD) {d}', f'{correct}\n{just}'))

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
