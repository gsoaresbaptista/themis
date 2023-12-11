from typing import Optional
import re


class WrapperTextElement:
    def __init__(self) -> None:
        self._name: Optional[str] = None

    def set_name(self, name: str) -> None:
        self._name = name


class Article:
    def __init__(self, content: str = '') -> None:
        self._content: str = content

    def set_content(self, content: str) -> None:
        self._content = content

    def __repr__(self) -> str:
        return self._content


class Chapter(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._articles: list[Article] = list()

    def add_article(self, article: Article) -> None:
        self._articles.append(article)


class Title(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._chapters: list[Chapter] = list()

    def add_chapter(self, chapter: Chapter) -> None:
        self._chapters.append(chapter)

    def add_article(self, article: Article) -> None:
        if not self._chapters:
            self._chapters.append(Chapter())
        self._chapters[-1].add_article(article)


class Section(WrapperTextElement):
    def __init__(self) -> None:
        super().__init__()
        self._titles: list[Title] = list()

    def add_chapter(self, chapter: Chapter) -> None:
        self._titles[-1].add_chapter(chapter)

    def add_title(self, title: Title) -> None:
        self._titles.append(title)

    def add_article(self, article: Article) -> None:
        self._titles[-1].add_article(article)


class ConstitutionParser:
    @staticmethod
    def parse_articles(text):
        pattern = re.compile(r'(Art\. \d+o.*?)\n(?=Art\. \d+o|$)', re.DOTALL)
        matches = re.findall(pattern, text)
        return matches
