## Project Summary

A Python application that takes scanned arabic books in pdf format, converts them into text and outputs an audio file.

## How to Run

1. **Install the Required Dependencies**

   - Use pip to install the packages listed in `requirements.txt`:

     ```bash
     pip install -r requirements.txt
     ```

2. **Modify `config.py`**

   - Set the `book_path` variable in `config.py` to the path of the scanned PDF file you wish to process.

     ```python
     # config.py
     book_path = 'path/to/your/book.pdf'
     ```

3. **Run `main.py`**

   - Execute the main script to start the conversion process.

     ```bash
     python main.py
     ```

4. **Optional: Test Different Models**

   - To experiment with different open-source models, modify `model_config.py` and specify the desired models.

     ```python
     # model_config.py
     text_model_id = 'your-preferred-text-model-id'
     speech_model_id = 'your-preferred-tts-model-id'
     ```
## Current Models Used

- **Text Correction Model:** [Silma-AI](https://huggingface.co/silma-ai/SILMA-9B-Instruct-v1.0)

- **Text-to-Speech Model:** [Facebook MMS ara](https://huggingface.co/facebook/mms-tts-ara)

## Known Bugs

- `pytesseract` sometimes skips the last few words in a paragraph if they are at a new line.
- The OCR process does not read numbers accurately.
- The generated speech does not include appropriate pauses, resulting in a monotonous audio output.

## Future Work

- Implement additional processing to correct obvious mistakes in the OCR text output.
- Test different TTS models to improve the quality and naturalness of the generated speech.
- Apply semantic encoding techniques to the generated audio for an enhanced listening experience.
