import numpy as np
from PIL import Image
import cv2

image_path = "temp_images\\in.jpg"
out_image='temp_images\\out.jpg'


def resize_and_set_dpi(image, size, dpi=(300, 300)):
    # Resize the image
    resized_image = image.resize(size, Image.LANCZOS)

    # Save with new DPI in memory (not to a file)
    resized_image.info['dpi'] = dpi  # Set the new DPI
    return resized_image

def preprocess_image(page):
    page.save(image_path)
    with Image.open(image_path) as img:
        new_size = (img.width // 2, img.height // 2)  # Example resize
        new_dpi = (300, 300)  # Desired DPI
        updated_image = resize_and_set_dpi(img, new_size, new_dpi)
        updated_image.save(out_image, dpi=new_dpi)
    img = cv2.imread(out_image)
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img