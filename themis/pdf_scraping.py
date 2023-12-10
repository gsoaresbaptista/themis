from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextLineHorizontal, LTTextContainer, LTChar

IGNORED_PAGES = [
    *range(16),
    # title pages
    120,
    126,
    272,
    400,
    406,
    458,
    468,
    544,
    570,
    574,
    582,
    632,
    654,
    700,
    716,
    728,
    750,
    784,
    796,
    850,
    862,
    # summary pages
    119,
    120,
    121,
    *range(127, 138),
    *range(273, 282),
    401,
    405,
    *range(407, 412),
    *range(459, 462),
    *range(470, 474),
    *range(545, 548),
    569,
    571,
    *range(575, 578),
    581,
    *range(584, 586),
    631,
    *range(633, 636),
    653,
    *range(655, 658),
    *range(701, 704),
    *range(717, 720),
    *range(729, 732),
    749,
    *range(751, 756),
    *range(785, 788),
    *range(797, 800),
    *range(851, 854),
    861,
    *range(863, 866),
    *range(885, 888),
]

ALLOW_SPACE = (',', ')', '\'', '"', '”', '%', '–')
ALLOW_LINE_BREAK = (':', ';', '?')
ALLOW_CONTINUE = ('\n', '/')


def join_lines(lines: list[str]):
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
                print(f'[{text}]', f'[{line}]')
                exit(0)
        else:
            line = text

        if line[-1] == '.':
            line += '\n'

    # remove last line break
    if line[-1] == '\n':
        line = line[:-1]

    return line


def aggregate_by_fonts(lines):
    book = []
    current_lines, current_font = [], lines[0][1]

    current_id = 0

    while current_id < len(lines):
        if lines[current_id][1] == current_font:
            current_lines.append(lines[current_id][0])
        else:
            current_line = join_lines(current_lines)
            book.append(current_line)

            if current_id + 1 >= len(lines):
                break

            current_lines = [lines[current_id][0]]
            current_font = lines[current_id][1]

        current_id += 1

    if len(current_lines) > 0:
        current_line = join_lines(current_lines)
        book.append(current_line)

    return book


def extract_text(pdf_path):
    lines = []

    for page_number, page_layout in enumerate(extract_pages(pdf_path)):
        if page_number in IGNORED_PAGES:
            continue

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
                            font_name == 'ASSXNX+BarlowSemiCondensed-Medium'
                            and font_size == 14.0
                        ):
                            lines.append((text.replace('\t', ' ').strip(), font_size))

    lines = aggregate_by_fonts(lines)

    return lines


if __name__ == '__main__':
    pdf_path = 'data/pdf/Vade_mecum_2023.pdf'
    result = extract_text(pdf_path)

    with open("data.txt", "w") as outfile:
        outfile.write("\n".join(result))

    # for text in result:
    #     print(text)
    #     print('-' * 100)
