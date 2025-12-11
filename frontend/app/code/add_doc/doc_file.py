import docx
from pypdf import PdfReader
from werkzeug.datastructures import FileStorage
import math

async def convert(file: FileStorage) -> str:
    if file.mimetype == "application/pdf":
        text =  '\n'.join(
            pdf_page.extract_text()
            for pdf_page in PdfReader(file.stream).pages
        )
    elif file.mimetype == "text/plain":
        text = file.read().decode('utf-8')
    elif file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text =  '\n'.join(
            paragraph.text
            for paragraph in docx.Document(file.stream).paragraphs
        )
        
    return text