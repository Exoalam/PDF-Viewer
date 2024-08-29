import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QToolBar, 
                             QStatusBar, QFileDialog, QVBoxLayout, QWidget, 
                             QFontComboBox, QSpinBox, QPushButton)
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt
from pdf_operations import PDFOperations

class PDFReaderWriter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_ops = PDFOperations()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI-Powered PDF Reader/Writer")
        self.setGeometry(100, 100, 800, 600)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createToolBar()
        self.createMenuBar()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def createToolBar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

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
        self.textEdit.setCurrentFont(font)

    def changeFontSize(self, size):
        self.textEdit.setFontPointSize(size)

    def toggleBold(self):
        font = self.textEdit.currentFont()
        font.setBold(not font.bold())
        self.textEdit.setCurrentFont(font)

    def toggleItalic(self):
        font = self.textEdit.currentFont()
        font.setItalic(not font.italic())
        self.textEdit.setCurrentFont(font)

    def toggleUnderline(self):
        font = self.textEdit.currentFont()
        font.setUnderline(not font.underline())
        self.textEdit.setCurrentFont(font)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "PDF Files (*.pdf)")
        if fileName:
            try:
                text = self.pdf_ops.read_pdf(fileName)
                self.textEdit.setPlainText(text)
                self.statusBar.showMessage(f"Opened {fileName}")
            except Exception as e:
                self.statusBar.showMessage(f"Error: {str(e)}")

    def saveFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)")
        if fileName:
            try:
                text = self.textEdit.toPlainText()
                self.pdf_ops.save_pdf(fileName, text)
                self.statusBar.showMessage(f"File saved as {fileName}")
            except Exception as e:
                self.statusBar.showMessage(f"Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    ex = PDFReaderWriter()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
