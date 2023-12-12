import sqlite3
import pandas as pd

def roman_to_decimal(roman: str):
    roman = roman.upper()
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    decimal = 0
    prev_value = 0

    for i in reversed(roman):
        int_val = roman_numerals[i]
        if int_val < prev_value:
            decimal -= int_val
        else:
            decimal += int_val
        prev_value = int_val

    return decimal

def create_database_and_insert_data(csv_file, db_file):
    # Connect to a SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a table with an additional 'id' column as the primary key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS oab_provas (
            id INTEGER PRIMARY KEY,
            Prova INTEGER,
            Numero_Questao INTEGER,
            Enunciado TEXT,
            Alternativa_A TEXT,
            Alternativa_B TEXT,
            Alternativa_C TEXT,
            Alternativa_D TEXT,
            Alternativa_Correta TEXT,
            Justificativa TEXT
        );
    ''')

    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Convert 'Prova' column from Roman to Decimal
    data['Prova'] = data['Prova'].apply(roman_to_decimal)

    # Insert data into the table
    data.to_sql('oab_provas', conn, if_exists='append', index=False, index_label='id')

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Usage
csv_file_path = 'oab_provas.csv'
db_file_path = 'oab_provas.db'

create_database_and_insert_data(csv_file_path, db_file_path)
