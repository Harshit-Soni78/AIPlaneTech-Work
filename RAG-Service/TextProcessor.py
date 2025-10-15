import os
import re
import json
import fitz
import requests
from docx import Document
from bs4 import BeautifulSoup
from uploadValidification import detect_input_type  

class FileConverter:
    def __init__(self, input_data):
        if isinstance(input_data, str):
            input_data = input_data.strip().strip('"')
        self.input_data = input_data

    def convert(self):
        converters = {
            'pdf': self._convert_pdf,
            'docx': self._convert_docx,
            'url': self._convert_url,
            'plain_text': self._convert_plain_text,
            'json': self.convert_json_to_text
        }
        
        # Detect type based on the input data (file path or URL)
        self.input_type = detect_input_type(self.input_data)

        if self.input_type not in converters:
            return f"Unsupported input type: {self.input_type}"

        return converters[self.input_type]()

    def _convert_pdf(self):
        try:
            doc = fitz.open(self.input_data)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            return full_text.strip()
        except Exception as e:
            return f"Error reading PDF: {e}"

    def _convert_docx(self):
        try:
            doc = Document(self.input_data)
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return text.strip()
        except Exception as e:
            return f"Error reading DOCX: {e}"

    def _convert_url(self):
        try:
            response = requests.get(self.input_data, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            [elem.decompose() for elem in soup(["script", "style"])]
            text = ' '.join(chunk.strip() for chunk in soup.get_text(separator=' ').split() if chunk)
            return text.strip()
        except Exception as e:
            return f"Error fetching URL: {e}"

    def convert_json_to_text(self):
        try:
            with open(self.input_data, 'r') as file:
                data = json.load(file)
            return json.dumps(data, indent=4)
        except Exception as e:
            return f"Error reading JSON: {e}"

    def _convert_plain_text(self):
        try:
            if os.path.exists(self.input_data):
                with open(self.input_data, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            return self.input_data.strip()
        except Exception as e:
            return f"Error reading plain text: {e}"
