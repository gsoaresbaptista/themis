import sqlite3
from themis.pdf.utils import MainBlock


def create_sqlite_database(
    blocks: list[MainBlock], name: str = 'vade_mecum'
) -> None:
    conn = sqlite3.connect(f'{name}.db')
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS codes (
        id INTEGER PRIMARY KEY,
        code TEXT,
        book TEXT,
        title TEXT,
        subtitle TEXT,
        chapter TEXT,
        section TEXT,
        subsection TEXT,
        articles TEXT,
        notes TEXT
    )
    """
    )

    for block in blocks:
        for book in block._books:
            for title in book._titles:
                for subtitle in title._sub_titles:
                    for chapter in subtitle._chapters:
                        for section in chapter._sections:
                            for subsection in section._sub_sections:
                                for article in subsection._articles:
                                    notes = [
                                        block._notes[index - 1]._content
                                        for index in article._references
                                        if len(block._notes) > index - 1
                                    ]

                                    articles = artigos = [f"Art.{art}" for art in article._content.split("Art.") if art.strip()]


                                    for article_text in articles:
                                        cursor.execute(
                                            """
                                            INSERT INTO codes (
                                                code, book, title, subtitle,
                                                chapter, section, subsection,
                                                articles, notes)
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                            """,
                                            (
                                                block._name,
                                                book._name,
                                                title._name,
                                                subtitle._name,
                                                chapter._name,
                                                section._name,
                                                subsection._name,
                                                article_text,
                                                '\n'.join(notes) if notes else '',
                                            ),
                                        )

    conn.commit()
    cursor.close()
    conn.close()
