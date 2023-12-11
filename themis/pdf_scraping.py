from pdf_extractor import PDFExtractor


if __name__ == '__main__':
    pdf_path = 'data/pdf/Vade_mecum_2023.pdf'
    extractor = PDFExtractor(pdf_path)
    result = extractor.extract_text()

    # with open("data.txt", "w") as outfile:
    #     outfile.write("\n".join(result))

    for text in result:
        print(text)
        print('-' * 100)
