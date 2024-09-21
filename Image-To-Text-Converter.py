import sys
import pytesseract
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QTextEdit, QComboBox, QHBoxLayout, QColorDialog, QFontComboBox
)
from PyQt5.QtGui import QPixmap, QIcon, QColor, QFont, QPainter, QPen
from PyQt5.QtCore import Qt
from googletrans import Translator, LANGUAGES

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Modern Color Palette
        self.bg_color = '#1e272e'
        self.text_color = '#ffffff'
        self.button_color = '#00a8ff'
        self.button_hover_color = '#007bb5'
        self.text_edit_bg = '#2f3640'
        self.text_edit_border = '#00a8ff'

        # Main Window Style
        self.setStyleSheet(f'background-color: {self.bg_color}; color: {self.text_color};')

        # Widgets
        self.title_label = QLabel("OCR & Translator", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #f5f6fa;')

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #00a8ff; padding: 20px;")

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Extracted Text")
        self.text_edit.setStyleSheet(f'border: 2px solid {self.text_edit_border}; color: {self.text_color}; background-color: {self.text_edit_bg};')
        self.text_edit.setMinimumHeight(200)  # Set minimum height


        self.browse_button = QPushButton(QIcon('folder.png'), 'Browse Image', self)
        self.browse_button.clicked.connect(self.browse_image)
        self.browse_button.setStyleSheet(self.button_style())

        self.translate_button = QPushButton(QIcon('translate.png'), 'Translate', self)
        self.translate_button.clicked.connect(self.translate_text)
        self.translate_button.setStyleSheet(self.button_style())

        self.language_selector = QComboBox(self)
        self.language_selector.addItems(LANGUAGES.values())
        self.language_selector.setCurrentText('en')
        self.language_selector.setStyleSheet('background-color: #353b48; color: white; border-radius: 5px; padding: 5px;')

        self.font_combobox = QFontComboBox(self)
        self.font_combobox.currentFontChanged.connect(self.change_font)
        self.font_combobox.setStyleSheet('background-color: #353b48; color: white; border-radius: 5px; padding: 5px;')

        self.increase_font_button = QPushButton('+', self)
        self.increase_font_button.clicked.connect(self.increase_font_size)
        self.increase_font_button.setStyleSheet(self.button_style())

        self.decrease_font_button = QPushButton('-', self)
        self.decrease_font_button.clicked.connect(self.decrease_font_size)
        self.decrease_font_button.setStyleSheet(self.button_style())

        self.color_button = QPushButton('Color', self)
        self.color_button.clicked.connect(lambda: self.change_font_color(self.text_edit))
        self.color_button.setStyleSheet(self.button_style())

        self.font_size_label = QLabel('Font Size: 12', self)
        self.font_size_label.setStyleSheet('color: white; font-size: 14px;')

        self.dark_mode_button = QPushButton('Dark Mode', self)
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.dark_mode_button.setStyleSheet(self.button_style())

        # App icon
        self.setWindowIcon(QIcon('app_icon.png'))

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.increase_font_button)
        button_layout.addWidget(self.decrease_font_button)
        button_layout.addWidget(self.color_button)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.text_edit)
        main_layout.addWidget(self.browse_button)
        main_layout.addWidget(self.language_selector)
        main_layout.addWidget(self.font_combobox)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.font_size_label)
        main_layout.addWidget(self.dark_mode_button)
        main_layout.addWidget(self.translate_button)

        self.setLayout(main_layout)

        self.setWindowTitle('Modern OCR with Translation')
        self.setGeometry(100, 100, 900, 650)
        self.centerOnScreen()

    def centerOnScreen(self):
        resolution = QApplication.desktop().screenGeometry()
        self.move(int((resolution.width() / 2) - (self.frameSize().width() / 2)),
                  int((resolution.height() / 2) - (self.frameSize().height() / 2)))

    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        if file_name:
            self.process_image(file_name)

    def process_image(self, file_name):
        text = pytesseract.image_to_string(file_name)
        pixmap = QPixmap(file_name)
        self.image_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.text_edit.setPlainText(text)

    def translate_text(self):
        text_to_translate = self.text_edit.toPlainText()
        target_language = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.language_selector.currentText())]

        translator = Translator()
        translated_text = translator.translate(text_to_translate, dest=target_language).text

        self.text_edit.setPlainText(translated_text)

    def increase_font_size(self):
        font = self.text_edit.font()
        font_size = font.pointSize() + 2
        font.setPointSize(font_size)
        self.text_edit.setFont(font)
        self.update_font_size_label()

    def decrease_font_size(self):
        font = self.text_edit.font()
        font_size = max(8, font.pointSize() - 2)
        font.setPointSize(font_size)
        self.text_edit.setFont(font)
        self.update_font_size_label()

    def update_font_size_label(self):
        font_size = self.text_edit.font().pointSize()
        self.font_size_label.setText(f'Font Size: {font_size}')

    def change_font_color(self, target_edit):
        color = QColorDialog.getColor()
        if color.isValid():
            target_edit.setTextColor(color)

    def change_font(self, font):
        self.text_edit.setCurrentFont(font)

    def toggle_dark_mode(self):
        if self.dark_mode_button.text() == 'Dark Mode':
            self.setStyleSheet('background-color: #2c3e50; color: white;')
            self.text_edit.setStyleSheet('border: 2px solid #3498db; color: white; background-color: #2f3640;')
            self.dark_mode_button.setText('Light Mode')
        else:
            self.setStyleSheet(f'background-color: {self.bg_color}; color: {self.text_color};')
            self.text_edit.setStyleSheet(f'border: 2px solid {self.text_edit_border}; color: {self.text_color}; background-color: {self.text_edit_bg};')
            self.dark_mode_button.setText('Dark Mode')

    def button_style(self):
        return f"""
        QPushButton {{
            background-color: {self.button_color};
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid {self.button_hover_color};
        }}
        QPushButton:hover {{
            background-color: {self.button_hover_color};
        }}
    """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ocr_app = OCRApp()
    ocr_app.show()
    sys.exit(app.exec_())

