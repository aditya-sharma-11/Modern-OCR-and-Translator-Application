import sys
import pytesseract
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QTextEdit, QComboBox, QSplitter, QHBoxLayout, QColorDialog, QFontComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QSize
from googletrans import Translator, LANGUAGES

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Widgets
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Extracted Text")
        self.text_edit.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for input text

        self.browse_button = QPushButton(QIcon('folder.png'), 'Browse Image', self)
        self.browse_button.clicked.connect(self.browse_image)
        self.browse_button.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for buttons

        self.translate_button = QPushButton(QIcon('translate.png'), 'Translate', self)
        self.translate_button.clicked.connect(self.translate_text)
        self.translate_button.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for buttons

        self.language_selector = QComboBox(self)
        self.language_selector.addItems(LANGUAGES.values())
        self.language_selector.setCurrentText('en')  # Set default language to English
        self.language_selector.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for dropdown

        self.font_combobox = QFontComboBox(self)
        self.font_combobox.currentFontChanged.connect(self.change_font)
        self.font_combobox.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for dropdown

        self.increase_font_button = QPushButton('+', self)
        self.increase_font_button.clicked.connect(self.increase_font_size)
        self.increase_font_button.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for buttons

        self.decrease_font_button = QPushButton('-', self)
        self.decrease_font_button.clicked.connect(self.decrease_font_size)
        self.decrease_font_button.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for buttons

        self.color_button = QPushButton('Color', self)
        self.color_button.clicked.connect(lambda: self.change_font_color(self.text_edit))
        self.color_button.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for buttons

        self.font_size_label = QLabel('Font Size: 12', self)
        self.font_size_label.setStyleSheet('color: #2c3e50;')  # Styling for font size label

        # Dark mode button
        self.dark_mode_button = QPushButton('Dark Mode', self)
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.dark_mode_button.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for buttons
        self.dark_mode_button.setIcon(QIcon('dark_mode_icon.png'))
        self.dark_mode_button.setIconSize(QSize(20, 20))

        # App icon
        self.setWindowIcon(QIcon('app_icon.png'))

        # Spacer to push the Dark Mode button to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Splitter for resizing from above
        self.splitter_top = QSplitter(Qt.Vertical)
        self.splitter_top.addWidget(self.browse_button)
        self.splitter_top.addWidget(self.text_edit)
        self.splitter_top.addWidget(self.language_selector)
        self.splitter_top.addWidget(self.font_combobox)

        # Create layouts for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.increase_font_button)
        button_layout.addWidget(self.decrease_font_button)
        button_layout.addWidget(self.color_button)  # Add the color button here

        # Add the button layout to the top splitter
        self.splitter_top.setLayout(button_layout)  # Add button layout here
        self.splitter_top.addWidget(self.font_size_label)
        self.splitter_top.addWidget(self.dark_mode_button)
        button_layout.addItem(spacer)  # Add the spacer to the layout

        # Splitter for resizing from below
        self.splitter_bottom = QSplitter(Qt.Vertical)
        self.splitter_bottom.addWidget(self.splitter_top)
        self.splitter_bottom.addWidget(self.translate_button)

        # Splitter for horizontal orientation
        self.splitter_horizontal = QSplitter(Qt.Horizontal)
        self.splitter_horizontal.addWidget(self.image_label)
        self.splitter_horizontal.addWidget(self.splitter_bottom)

        # Set stretch factors to allow translation section to extend more
        self.splitter_bottom.setStretchFactor(0, 1)
        self.splitter_bottom.setStretchFactor(1, 2)

        # Apply some styling
        self.setStyleSheet('background-color: #ecf0f1; color: #2c3e50;')  # Set background color

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter_horizontal)

        self.setWindowTitle('OCR with Translation')
        self.setGeometry(100, 100, 800, 600)

        self.centerOnScreen()  # Center the application on the screen

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
        # Use Tesseract to perform OCR
        text = pytesseract.image_to_string(file_name)
        pixmap = QPixmap(file_name)

        # Add a border to the selected image
        pixmap_with_border = QPixmap(pixmap.size() + QSize(4, 4))
        pixmap_with_border.fill(Qt.black)  # Change the border color to black
        painter = QPainter(pixmap_with_border)
        painter.drawPixmap(2, 2, pixmap)
        painter.end()

        # Display the image and extracted text
        self.image_label.setPixmap(pixmap_with_border)

        # Set a border for the text result
        self.text_edit.setPlainText(text)
        self.text_edit.setStyleSheet('border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;')  # Styling for input text

    def translate_text(self):
        text_to_translate = self.text_edit.toPlainText()
        target_language = self.language_selector.currentText()

        # Translate to the selected language using googletrans
        translator = Translator()
        translated_text = translator.translate(text_to_translate, dest=target_language).text

        # Update the text edit with the translated text
        self.text_edit.setPlainText(translated_text)

    def increase_font_size(self):
        font = self.text_edit.font()
        font_size = font.pointSize() + 2
        font.setPointSize(font_size)
        self.text_edit.setFont(font)
        self.update_font_size_label()

    def decrease_font_size(self):
        font = self.text_edit.font()
        font_size = max(8, font.pointSize() - 2)  # Ensure the minimum font size is 8
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
            # Switch to dark mode
            self.setStyleSheet('background-color: #2c3e50; color: white;')
            self.dark_mode_button.setText('Light Mode')

            # Change border color to red
            border_color = 'border: 2px solid #e74c3c; color: white; background-color: #2c3e50;'
            button_color = 'border: 2px solid #e74c3c; color: white; background-color: #2c3e50;'
            text_edit_border = 'border: 2px solid #e74c3c; color: white; background-color: #2c3e50;'
        else:
            # Switch to light mode
            self.setStyleSheet('background-color: #ecf0f1; color: #2c3e50;')
            self.dark_mode_button.setText('Dark Mode')

            # Change border color back to blue
            border_color = 'border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;'
            button_color = 'border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;'
            text_edit_border = 'border: 2px solid #3498db; color: #2c3e50; background-color: #ecf0f1;'

        # Apply the new border color to specific widgets
        self.browse_button.setStyleSheet(button_color)
        self.translate_button.setStyleSheet(button_color)
        self.language_selector.setStyleSheet(button_color)
        self.font_combobox.setStyleSheet(button_color)
        self.increase_font_button.setStyleSheet(button_color)
        self.decrease_font_button.setStyleSheet(button_color)
        self.color_button.setStyleSheet(button_color)
        self.dark_mode_button.setStyleSheet(button_color)

        # Change the border color of the extracted text box
        self.text_edit.setStyleSheet(text_edit_border)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ocr_app = OCRApp()
    ocr_app.show()
    sys.exit(app.exec_())

