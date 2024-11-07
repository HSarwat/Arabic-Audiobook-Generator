import re

def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    return re.sub(arabic_diacritics, '', text)


def correct_common_ocr_errors(text):
    corrections = {
        '0': '٠', '1': '١', '2': '٢', '3': '٣',
        '4': '٤', '5': '٥', '6': '٦', '7': '٧',
        '8': '٨', '9': '٩',
        # Add more corrections as needed
    }
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    return text

def remove_tatweel(text):
    return text.replace('ـ', '')

def remove_extra_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()


def preprocess_text(text):
    # Additional custom preprocessing
    text = remove_diacritics(text)
    text = correct_common_ocr_errors(text)
    text = remove_tatweel(text)
    text = remove_extra_spaces(text)
    return text






