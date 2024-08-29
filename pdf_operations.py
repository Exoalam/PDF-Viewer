import fitz  # PyMuPDF
from PyQt6.QtGui import QImage, QPixmap

class PDFOperations:
    def __init__(self):
        self.doc = None
        self.current_page = 0

    def open_pdf(self, file_path):
        try:
            self.doc = fitz.open(file_path)
            self.current_page = 0
            return True
        except Exception as e:
            raise Exception(f"Error opening PDF: {str(e)}")

    def close_pdf(self):
        if self.doc:
            self.doc.close()
            self.doc = None
            self.current_page = 0

    def save_pdf(self, file_path):
        if not self.doc:
            raise Exception("No document open")
        try:
            self.doc.save(file_path)
        except Exception as e:
            raise Exception(f"Error saving PDF: {str(e)}")

    def get_page_count(self):
        return len(self.doc) if self.doc else 0

    def get_page_text(self, page_num):
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return ""
        page = self.doc[page_num]
        return page.get_text()

    def replace_page_text(self, page_num, new_text):
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return
        page = self.doc[page_num]
        
        # Create a new PDF page with the same dimensions
        new_page = self.doc.new_page(width=page.rect.width, height=page.rect.height)
        
        # Copy all non-text elements from the old page to the new page
        new_page.show_pdf_page(new_page.rect, self.doc, page_num)
        
        # Remove all text from the new page
        for img in new_page.get_images():
            new_page.insert_image(img["bbox"], filename=img["name"])
        
        # Insert the new text
        new_page.insert_text((50, 50), new_text)
        
        # Replace the old page with the new page
        self.doc.delete_page(page_num)
        self.doc.insert_page(page_num, new_page)

    def get_page_pixmap(self, page_num, scale=2):
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return None
        page = self.doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img = pix.tobytes("ppm")
        qimg = QImage.fromData(img)
        return QPixmap.fromImage(qimg)

    def next_page(self):
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            return True
        return False

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            return True
        return False