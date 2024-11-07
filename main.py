import ray
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from Functions.image_preprocessing import preprocess_image
from Functions.text_preprocessing import preprocess_text
from Functions.ocr_correction import TextModelActor
from Functions.audio_generation import AudioModelActor
from config import *

if __name__ == "__main__":

    # Load ray to set up different actors
    ray.init()

    # load book and split into pages
    path = book_path
    pages = convert_from_path(path)

    # Initialize text variable that will be used to create '.txt' file
    text = ''

    # Create the text model actor
    text_model_actor = TextModelActor.options(num_gpus=1).remote()


    # Read text from each page
    for page in pages:

        # Image preprocessing to clean OCR image
        page = preprocess_image(page)

        # Read text using pytesseract
        page_text = pytesseract.image_to_string(page, lang='ara')

        # # Preprocess text, currently doesn't improve performance, need to investigate different methods
        # page_text = preprocess_text(page_text)

        # Split text into paragraphs
        paragraphs = page_text.split('\n\n')
        for paragraph in paragraphs:

            if len(paragraph) < 2:
                continue

            # Correct paragraphs using the text model actor
            corrected_paragraph = ray.get(text_model_actor.correct_text.remote(paragraph))
            text += corrected_paragraph + "\n\n"

        # # Optional page separator
        # text += separator

    # Kill the text model actor to free memory
    ray.kill(text_model_actor)

    # Save the extracted text
    with open(generated_text_path, 'w', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')

    # Create the audio model actor
    audio_model_actor = AudioModelActor.options(num_gpus=1).remote()

    # Generate and save the audio file
    audio_data = ray.get(audio_model_actor.generate_audio.remote(text))

    # Kill the audio model actor to free memory
    ray.kill(audio_model_actor)




