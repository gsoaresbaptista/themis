from typing import Optional
import re


class WrapperTextElement:
    def __init__(self) -> None:
        self._name: Optional[str] = None

    def set_name(self, name: str) -> None:
        self._name = name


class Note:
    def __init__(self, id: int) -> None:
        self._id: int = id
        self._content: str

    def add_content(self, content: str) -> None:
        self._content = content


class Article:
    def __init__(
        self, content: str = '', references: list[int] = list()
    ) -> None:
        self._content: str = content
        self._references = references

    def get_references(self) -> list[Note]:
        return self._references

    def set_content(self, content: str) -> None:
        self._content = content

    def __repr__(self) -> str:
        return self._content


class SubSection(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._articles: list[Article] = list()

    def add_article(self, article: Article) -> None:
        self._articles.append(article)


class Section(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._sub_sections: list[SubSection] = list()

    def add_article(self, article: Article) -> None:
        if not self._sub_sections:
            self._sub_sections.append(SubSection())
        self._sub_sections[-1].add_article(article)


class Chapter(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._sections: list[Section] = list()

    def add_article(self, article: Article) -> None:
        if not self._sections:
            self._sections.append(Section())
        self._sections[-1].add_article(article)

    def add_section(self, section: Section) -> None:
        self._sections.append(section)


class SubTitle(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._chapters: list[Chapter] = list()

    def add_chapter(self, chapter: Chapter) -> None:
        self._chapters.append(chapter)

    def add_article(self, article: Article) -> None:
        if not self._chapters:
            self._chapters.append(Chapter())
        self._chapters[-1].add_article(article)

    def add_section(self, section: Section) -> None:
        self._chapters[-1].add_section(section)


class Title(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._sub_titles: list[SubTitle] = list()

    def add_chapter(self, chapter: Chapter) -> None:
        if not self._sub_titles:
            self._sub_titles.append(SubTitle())
        self._sub_titles[-1].add_chapter(chapter)

    def add_article(self, article: Article) -> None:
        if not self._sub_titles:
            self._sub_titles.append(SubTitle())
        self._sub_titles[-1].add_article(article)

    def add_section(self, section: Section) -> None:
        self._sub_titles[-1].add_section(section)

    def add_subtitle(self, subtitle: SubTitle) -> None:
        self._sub_titles.append(subtitle)


class Book(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._titles: list[Title] = list()

    def add_title(self, title: Title) -> None:
        self._titles.append(title)

    def add_subtitle(self, subtitle: SubTitle) -> None:
        if not self._titles:
            self._titles.append(Title())
        self._titles[-1].add_subtitle(subtitle)

    def add_article(self, article: Article) -> None:
        if not self._titles:
            self._titles.append(Title())
        self._titles[-1].add_article(article)

    def add_chapter(self, chapter: Chapter) -> None:
        self._titles[-1].add_chapter(chapter)

    def add_section(self, section: Section) -> None:
        self._titles[-1].add_section(section)


class MainBlock(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._books: list[Book] = list()
        self._notes: list[Note] = list()

    def add_chapter(self, chapter: Chapter) -> None:
        self._books[-1].add_chapter(chapter)

    def add_title(self, title: Title) -> None:
        if not self._books:
            self._books.append(Book())
        self._books[-1].add_title(title)

    def add_subtitle(self, subtitle: SubTitle) -> None:
        if not self._books:
            self._books.append(Book())
        self._books[-1].add_subtitle(subtitle)

    def add_article(self, article: Article) -> None:
        if not self._books:
            self._books.append(Book())
        self._books[-1].add_article(article)

    def add_section(self, section: Section) -> None:
        self._books[-1].add_section(section)

    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def add_reference(self, id: int, content: str) -> None:
        note = Note(id)
        note.add_content(content)
        self._notes.append(note)


class ConstitutionParser:
    @staticmethod
    def parse_articles(text):
        pattern = re.compile(r'(Art\. \d+o.*?)\n(?=Art\. \d+o|$)', re.DOTALL)
        matches = re.findall(pattern, text)
        return matches
