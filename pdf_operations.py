import fitz  # PyMuPDF

class PDFOperations:
    @staticmethod
    def read_pdf(file_path):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    @staticmethod
    def save_pdf(file_path, text):
        try:
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((50, 50), text)
            doc.save(file_path)
        except Exception as e:
            raise Exception(f"Error saving PDF: {str(e)}")
