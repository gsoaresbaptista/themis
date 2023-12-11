from utils import Section, Title, Article, Chapter, ConstitutionParser


class PDFLayout:
    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    def build(self) -> list[Section]:
        sections = []

        for text, font_size, references in self._lines:
            if font_size == 28:
                section = Section()
                section.set_name(text)
                sections.append(section)
                print('SET SECTION NAME:', text)

            elif font_size == 11:
                if text.startswith('CAPÍTULO'):
                    chapter = Chapter()
                    chapter.set_name(text)
                    sections[-1].add_chapter(chapter)
                    print('SET CHAPTER NAME:', text)

                elif text.startswith('TÍTULO') or text.startswith('Preâmbulo'):
                    title = Title()
                    title.set_name(text)
                    sections[-1].add_title(title)
                    print('SET TITLE NAME:', text)

                else:
                    print(f'* Unhandled case: [{text}] ({font_size})')
                    exit()

            elif font_size == 9.5:
                articles = ConstitutionParser.parse_articles(text)

                articles = (
                    [Article(content) for content in articles]
                    if articles
                    else [Article(text)]
                )

                for article in articles:
                    sections[-1].add_article(article)

                print('SET ARTICLE CONTENT')

            # elif font_size == 4.1 or font_size == 7.0:
            #     continue

            else:
                print(f'Unhandled case: [{text}] ({font_size})')
                exit(0)

        return sections
