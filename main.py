import sys
import os
from typing import List, Tuple

from archive_handler import ArchiveHandler
from batch_processor import BatchProcessor
from ocr import OCRProcessor
from translator import TranslationService
from image_utils import ImageProcessor

def validate_languages(source_lang: str, target_lang: str) -> bool:
    valid_langs = ['ja', 'ko', 'ch_sim', 'en', 'ml', 'hi', 'fr']
    return source_lang in valid_langs and target_lang in valid_langs

def main():
    # CLI argument handling
    if len(sys.argv) != 3:
        print("Usage: python main.py input.cbz output.zip")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Interactive language selection
    print("Select Source Language:")
    print("1. Japanese (ja)")
    print("2. Korean (ko)")
    print("3. Chinese Simplified (ch_sim)")
    print("4. English (en)")
    source_lang = input("Enter source language code: ").lower()

    print("\nSelect Target Language:")
    print("1. English (en)")
    print("2. Malayalam (ml)")
    print("3. Hindi (hi)")
    print("4. French (fr)")
    target_lang = input("Enter target language code: ").lower()

    # Validate language selection
    if not validate_languages(source_lang, target_lang):
        print("Invalid language selection. Exiting.")
        sys.exit(1)

    # Initialize services
    archive_handler = ArchiveHandler(input_file)
    ocr_processor = OCRProcessor(source_lang)
    translator = TranslationService()
    image_processor = ImageProcessor()
    batch_processor = BatchProcessor(
        archive_handler, 
        ocr_processor, 
        translator, 
        image_processor,
        target_lang
    )

    # Process manga/comic
    translated_images = batch_processor.process_archive()

    # Save output
    archive_handler.save_translated_archive(translated_images, output_file)
    print(f"Translation complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
