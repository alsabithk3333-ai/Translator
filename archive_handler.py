import os
import zipfile
from typing import List

class ArchiveHandler:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.supported_extensions = ['.zip', '.cbz']
        self.validate_input()

    def validate_input(self):
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file {self.input_file} not found")
        
        ext = os.path.splitext(self.input_file)[1].lower()
        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {ext}")

    def extract_images(self) -> List[str]:
        temp_dir = os.path.join(os.path.dirname(self.input_file), 'temp_extract')
        os.makedirs(temp_dir, exist_ok=True)

        with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
            image_files = [
                f for f in zip_ref.namelist() 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
            ]
            image_files.sort()  # Maintain reading order

            for img in image_files:
                zip_ref.extract(img, temp_dir)

        return [os.path.join(temp_dir, img) for img in image_files]

    def save_translated_archive(self, translated_images: List[str], output_file: str):
        with zipfile.ZipFile(output_file, 'w') as zipf:
            for img in translated_images:
                zipf.write(img, os.path.basename(img))
