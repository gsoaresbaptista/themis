from pdf_extractor import PDFExtractor
from pdf_layout import PDFLayout


if __name__ == '__main__':
    pdf_path = 'data/pdf/Vade_mecum_2023.pdf'

    extractor = PDFExtractor(pdf_path)
    lines = extractor.extract_text()

    for line in lines[:10]:
        print(line)
        print('-' * 100)
    exit(0)

    builder = PDFLayout(lines)
    titles = builder.build()

    # print(titles)

    # with open("data.txt", "w") as outfile:
    #     outfile.write("\n".join([f'[{line[0]}]' for line in lines]))
