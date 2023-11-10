import os
import cv2
import easyocr

download_folder = 'captcha/original_img'
preprocessed_folder = 'captcha/preprocessed_img'

def apply_ocr(image_path):
    reader = easyocr.Reader(['en'])  # Specify the language(s)
    results = reader.readtext(image_path, allowlist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    best_text = ""
    best_confidence = 0.0

    for (bbox, text, prob) in results:
        if prob > best_confidence:
            best_text = text
            best_confidence = prob

    return best_text, best_confidence

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    _, thresh = cv2.threshold(image, 190, 210, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
    
    preprocessed_file = os.path.join(preprocessed_folder, 'preprocessed_image.png')
    cv2.imwrite(preprocessed_file, thresh)
    
    print("Imagem preprocessada salva com sucesso...")
    
    return preprocessed_file

def save_image(image, folder, file_name):
    if not os.path.exists(folder):
        os.makedirs(folder)
    image_path = os.path.join(folder, file_name)
    image.save(image_path)
    return image_path
