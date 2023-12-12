from pdf.pdf_extractor import PDFExtractor
from pdf.pdf_layout import PDFLayout

from data.database import create_sqlite_database

if __name__ == '__main__':
    pdf_path = 'data/pdf/Vade_mecum_2023.pdf'

    extractor = PDFExtractor(pdf_path)
    lines = extractor.extract_text()

    builder = PDFLayout(lines)
    titles = builder.build()

    create_sqlite_database(titles)
