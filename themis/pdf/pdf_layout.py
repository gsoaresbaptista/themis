from utils import (
    MainBlock,
    Title,
    Article,
    Chapter,
    ConstitutionParser,
    Section,
)


class PDFLayout:
    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    def build(self) -> list[MainBlock]:
        book_sections = []

        for text, font_size, references in self._lines:
            if font_size == 28:
                section = MainBlock()
                section.set_name(text)
                book_sections.append(section)
                print('SET MAIN BLOCK NAME:', text)

            elif font_size == 11 or font_size == 18:
                if text.startswith('CAPÍTULO'):
                    chapter = Chapter()
                    chapter.set_name(text)
                    book_sections[-1].add_chapter(chapter)
                    print('SET CHAPTER NAME:', text)

                elif (
                    text.startswith('TÍTULO')
                    or text.startswith('Preâmbulo')
                    or text.startswith('Ato')
                    or font_size == 18
                ):
                    title = Title()
                    title.set_name(text)
                    book_sections[-1].add_title(title)
                    print('SET TITLE NAME:', text)

                    if font_size == 18:
                        print('TITLE WITH FONT 18:', text)

                else:
                    print(f'* Unhandled case: [{text}] ({font_size})')
                    exit(0)

            elif font_size == 10:
                if text.startswith('Seção'):
                    section = Section()
                    section.set_name(text)
                    book_sections[-1].add_section(section)
                    print('SET SECTION NAME:', text)

            elif font_size == 9.5:
                articles = ConstitutionParser.parse_articles(text)

                articles = (
                    [Article(content, references) for content in articles]
                    if articles
                    else [Article(text, references)]
                )

                for article in articles:
                    book_sections[-1].add_article(article)

                print('SET ARTICLE CONTENT', text[:50].replace('\n', ''))

            elif font_size == 8:
                print('*Ignoring data:', text)

            elif font_size == 7.0 and (
                text.startswith('Nota do Editor') or text.startswith('NE')
            ):
                notes = text.split('\n')

                for content, indice in zip(notes, references):
                    book_sections[-1].add_reference(indice, content)
                
                print('SET REFERENCES:', references)

            else:
                print(f'Unhandled case: [{text}] ({font_size})')
                exit(0)

        return book_sections
