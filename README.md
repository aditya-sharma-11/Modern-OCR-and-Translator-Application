# Modern OCR and Translator Application

This is a Python-based GUI application that uses Optical Character Recognition (OCR) to extract text from images and provides translation functionality. The application features a modern user interface with customizable font styles, sizes, colors, and supports both dark and light modes.

## Features
- **OCR Text Extraction**: Extracts text from images using Tesseract OCR.
- **Text Translation**: Supports translating extracted text into different languages using Google Translate.
- **Customizable UI**: Allows users to change font styles, colors, and sizes.
- **Dark/Light Mode**: Toggle between dark and light modes for the interface.
- **Image Preview**: Displays the selected image for OCR extraction.

## Technologies Used
- **Python**
- **PyQt5**: For building the GUI.
- **pytesseract**: For text extraction (OCR).
- **googletrans**: For translation.
- **Tesseract-OCR**: Open-source OCR engine.

## Installation
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your-repo-name
    ```
3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On MacOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Ensure that Tesseract-OCR is installed on your machine. You can download and install it from [here](https://github.com/tesseract-ocr/tesseract).
   - For Windows, add the path of the `tesseract.exe` file to your environment variables.
   - For MacOS/Linux, install it using `brew` or `apt`:
     ```bash
     brew install tesseract
     ```
     ```bash
     sudo apt-get install tesseract-ocr
     ```

6. Run the application:
    ```bash
    python main.py
    ```

## Usage
1. Click on the **Browse Image** button to upload an image.
2. The app will automatically process the image and extract text using OCR.
3. You can then modify the extracted text and translate it using the **Translate** button.
4. Customize the text’s appearance using the provided options: font style, size, color, etc.
5. Toggle between **Dark Mode** and **Light Mode** using the button at the bottom.

## Screenshots
![OCR and Translator Screenshot](path/to/screenshot.png)

## Requirements
- Python 3.6+
- PyQt5
- pytesseract
- googletrans

## To-Do
- Add support for more image formats.
- Enhance translation performance for large text blocks.
- Improve UI customization.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

