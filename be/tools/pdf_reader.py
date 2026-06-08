import fitz


def read_pdf(file_path):

    document = fitz.open(file_path)

    text = ""

    for page in document:

        text += page.get_text()

    return text[:12000]