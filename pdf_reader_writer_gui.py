import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QToolBar, QStatusBar, QFileDialog, QPushButton, QScrollArea, 
                             QTextEdit, QSplitter, QFontComboBox, QSpinBox)
from PyQt6.QtGui import QAction, QPixmap, QPainter, QFont
from PyQt6.QtCore import Qt, QSize
from pdf_operations import PDFOperations

class PDFViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = None
        self.scale = 1.0

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        if self.pixmap:
            painter = QPainter(self)
            scaled_pixmap = self.pixmap.scaled(self.size() * self.scale, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)

    def sizeHint(self):
        if self.pixmap:
            return QSize(self.pixmap.width(), self.pixmap.height())
        return super().sizeHint()

class PDFReaderWriter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_ops = PDFOperations()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI-Powered PDF Reader/Writer")
        self.setGeometry(100, 100, 1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # PDF Viewer
        self.scroll_area = QScrollArea()
        self.pdf_viewer = PDFViewer()
        self.scroll_area.setWidget(self.pdf_viewer)
        self.scroll_area.setWidgetResizable(True)

        # Text Editor
        self.text_edit = QTextEdit()

        # Splitter to allow resizing
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.scroll_area)
        splitter.addWidget(self.text_edit)
        splitter.setSizes([600, 400])  # Set initial sizes

        main_layout.addWidget(splitter)

        self.createToolBar()
        self.createMenuBar()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def createToolBar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        prev_button = QPushButton("Previous")
        prev_button.clicked.connect(self.prev_page)
        toolbar.addWidget(prev_button)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_page)
        toolbar.addWidget(next_button)

        zoom_in_button = QPushButton("Zoom In")
        zoom_in_button.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in_button)

        zoom_out_button = QPushButton("Zoom Out")
        zoom_out_button.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out_button)

        fontCombo = QFontComboBox()
        fontCombo.currentFontChanged.connect(self.changeFont)
        toolbar.addWidget(fontCombo)

        fontSize = QSpinBox()
        fontSize.setRange(8, 72)
        fontSize.setValue(12)
        fontSize.valueChanged.connect(self.changeFontSize)
        toolbar.addWidget(fontSize)

        boldAction = QAction("Bold", self)
        boldAction.triggered.connect(self.toggleBold)
        toolbar.addAction(boldAction)

        italicAction = QAction("Italic", self)
        italicAction.triggered.connect(self.toggleItalic)
        toolbar.addAction(italicAction)

        underlineAction = QAction("Underline", self)
        underlineAction.triggered.connect(self.toggleUnderline)
        toolbar.addAction(underlineAction)

    def createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)

    def changeFont(self, font):
        self.text_edit.setCurrentFont(font)

    def changeFontSize(self, size):
        self.text_edit.setFontPointSize(size)

    def toggleBold(self):
        font = self.text_edit.currentFont()
        font.setBold(not font.bold())
        self.text_edit.setCurrentFont(font)

    def toggleItalic(self):
        font = self.text_edit.currentFont()
        font.setItalic(not font.italic())
        self.text_edit.setCurrentFont(font)

    def toggleUnderline(self):
        font = self.text_edit.currentFont()
        font.setUnderline(not font.underline())
        self.text_edit.setCurrentFont(font)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "PDF Files (*.pdf)")
        if fileName:
            try:
                self.pdf_ops.open_pdf(fileName)
                self.show_page()
                self.statusBar.showMessage(f"Opened {fileName}")
            except Exception as e:
                self.statusBar.showMessage(f"Error: {str(e)}")

    def saveFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)")
        if fileName:
            try:
                # Replace the text on the current page
                new_text = self.text_edit.toPlainText()
                self.pdf_ops.replace_page_text(self.pdf_ops.current_page, new_text)
                self.pdf_ops.save_pdf(fileName)
                self.statusBar.showMessage(f"File saved as {fileName}")
            except Exception as e:
                self.statusBar.showMessage(f"Error: {str(e)}")

    def show_page(self):
        pixmap = self.pdf_ops.get_page_pixmap(self.pdf_ops.current_page)
        if pixmap:
            self.pdf_viewer.setPixmap(pixmap)
            self.pdf_viewer.adjustSize()

            # Update text editor with page content
            text = self.pdf_ops.get_page_text(self.pdf_ops.current_page)
            self.text_edit.setPlainText(text)

            self.statusBar.showMessage(f"Page {self.pdf_ops.current_page + 1} of {self.pdf_ops.get_page_count()}")

    def prev_page(self):
        if self.pdf_ops.prev_page():
            self.show_page()

    def next_page(self):
        if self.pdf_ops.next_page():
            self.show_page()

    def zoom_in(self):
        self.pdf_viewer.scale *= 1.2
        self.pdf_viewer.update()

    def zoom_out(self):
        self.pdf_viewer.scale /= 1.2
        self.pdf_viewer.update()

def main():
    app = QApplication(sys.argv)
    ex = PDFReaderWriter()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()