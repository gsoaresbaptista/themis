import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextLineHorizontal, LTTextContainer, LTChar

from .constants import (
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
        current_lines, current_font, current_ref = (
            [],
            lines[0][1],
            lines[0][2],
        )

        current_id = 0

        while current_id < len(lines):
            if lines[current_id][1] == current_font and not (
                current_font == 11.0
                and (
                    lines[current_id][0].startswith('CAPÍTULO')
                    or lines[current_id][0].startswith('TÍTULO')
                )
            ):
                current_lines.append(lines[current_id][0])

                if lines[current_id][2] not in current_ref:
                    current_ref.extend(lines[current_id][2])

            # check if there is a note in the middle
            elif (
                lines[current_id][1] != current_font
                and lines[current_id][1] == 7.0
            ):
                start_reference_id = current_id
                reference_content = []
                reference_indices = []

                while (
                    start_reference_id < len(lines)
                    and lines[start_reference_id][1] == 7.0
                ):
                    reference_content.append(lines[start_reference_id][0])
                    reference_indices.extend(lines[start_reference_id][2])
                    start_reference_id += 1

                reference_content = self._join_lines(reference_content)
                book.insert(-1, (reference_content, 7.0, reference_indices))
                current_id = start_reference_id - 1

            else:
                current_line = self._join_lines(current_lines)
                book.append((current_line, current_font, current_ref))

                if current_id + 1 >= len(lines):
                    break

                current_lines = [lines[current_id][0]]
                current_font = lines[current_id][1]
                current_ref = lines[current_id][2]

            current_id += 1

        if len(current_lines) > 0:
            current_line = self._join_lines(current_lines)
            book.append((current_line, current_font, current_ref))

        return book

    def extract_text(self):
        for page_number, page_layout in enumerate(
            extract_pages(self.pdf_path)
        ):
            if page_number in IGNORED_PAGES:
                continue

            text_elements = []

            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if isinstance(text_line, LTTextLineHorizontal):
                            text_elements.append(text_line)

            # fix elements positions based on x coords
            changed = True

            while changed:
                curr_id = 0
                changed = False

                while curr_id < len(text_elements) - 1:
                    if (
                        text_elements[curr_id].x0
                        - text_elements[curr_id + 1].x0
                        > 100
                    ):
                        new_pos_id = curr_id + 1

                        while new_pos_id < len(text_elements) and (
                            text_elements[curr_id].x0
                            - text_elements[new_pos_id].x0
                            > 100
                        ):
                            new_pos_id += 1

                        new_pos_id -= 1

                        element = text_elements.pop(curr_id)
                        text_elements.insert(new_pos_id, element)
                        changed = True

                    curr_id += 1

            # process texts
            for element in text_elements:
                text = ''
                note_ref = ''
                last_font = None
                font_name = None
                font_size = None

                for text_element in element:
                    if isinstance(text_element, LTChar):
                        content = text_element.get_text()

                        # get note reference
                        if round(text_element.size, 1) in [
                            4.1,
                            5.5,
                        ]:
                            if content.isnumeric():
                                if last_font == text_element.size:
                                    note_ref += content
                                else:
                                    note_ref += '-' + content

                        elif font_size is None:
                            font_name = text_element.fontname
                            font_size = round(text_element.size, 1)
                            text += content

                        else:
                            text += content

                        last_font = text_element.size

                # ignore page number and not used titles
                if not (
                    font_name == 'ASSXNX+BarlowSemiCondensed-Medium'
                    and font_size == 14.0
                ) and not (
                    font_size == 11.0
                    and text in ['PARTE GERAL', 'PARTE ESPECIAL']
                ):
                    self.lines.append(
                        (
                            text.replace('\t', ' ').strip(),
                            font_size,
                            []
                            if note_ref == ''
                            else [
                                int(ref)
                                for ref in note_ref.split('-')
                                if ref != ''
                            ],
                        )
                    )

        self.lines = self._aggregate_by_fonts(self.lines)

        return self.lines
