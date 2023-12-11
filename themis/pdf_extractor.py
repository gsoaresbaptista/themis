from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextLineHorizontal, LTTextContainer, LTChar

from constants import (
    ALLOW_SPACE,
    ALLOW_LINE_BREAK,
    ALLOW_CONTINUE,
    IGNORED_PAGES,
)


class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.lines = []

    def _join_lines(self, lines):
        line = ''

        for text in lines:
            if line:
                if line[-1].isalnum() and text.split(' ')[0] in [
                    'TÍTULO',
                    'CAPÍTULO',
                ]:
                    line += f'\n{text}'

                elif line[-1].isalnum() or line[-1] in ALLOW_SPACE:
                    line += f' {text}'

                elif line[-1] == '-':
                    line = line[:-1] + text

                elif line[-1] in ALLOW_LINE_BREAK:
                    line += f'\n\t{text}'

                elif line[-1] in ALLOW_CONTINUE:
                    line += text

                else:
                    print(
                        f'Unhandled case: [{text}]', f'Current line: [{line}]'
                    )
                    exit(0)
            else:
                line = text

            if line[-1] == '.':
                line += '\n'

        # remove the last line break, if present
        if line[-1] == '\n':
            line = line[:-1]

        return line

    def _aggregate_by_fonts(self, lines):
        book = []
        current_lines, current_font = [], lines[0][1]

        current_id = 0

        while current_id < len(lines):
            if lines[current_id][1] == current_font:
                current_lines.append(lines[current_id][0])
            else:
                current_line = self._join_lines(current_lines)
                book.append(current_line)

                if current_id + 1 >= len(lines):
                    break

                current_lines = [lines[current_id][0]]
                current_font = lines[current_id][1]

            current_id += 1

        if len(current_lines) > 0:
            current_line = self._join_lines(current_lines)
            book.append(current_line)

        return book

    def extract_text(self):
        for page_number, page_layout in enumerate(
            extract_pages(self.pdf_path)
        ):
            if page_number in IGNORED_PAGES:
                continue

            if page_number > 20:
                break

            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if isinstance(text_line, LTTextLineHorizontal):
                            text = ''
                            font_name = None
                            font_size = None

                            for text_element in text_line:
                                if isinstance(text_element, LTChar):
                                    text += text_element.get_text()
                                    font_name = text_element.fontname
                                    font_size = round(text_element.size, 1)

                            # ignore page number
                            if not (
                                font_name
                                == 'ASSXNX+BarlowSemiCondensed-Medium'
                                and font_size == 14.0
                            ):
                                self.lines.append(
                                    (
                                        text.replace('\t', ' ').strip(),
                                        font_size,
                                    )
                                )

        self.lines = self._aggregate_by_fonts(self.lines)

        return self.lines
