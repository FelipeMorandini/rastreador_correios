import requests
from bs4 import BeautifulSoup
from captcha.captcha import preprocess_image, apply_ocr

def obter_dados_request():
    session = requests.Session()
    url = "https://rastreamento.correios.com.br/app/index.php"
    print("Obtendo imagem de captcha e dados de sessão...")
    response = session.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    captcha_image_url = "https://rastreamento.correios.com.br/" + soup.find("img", id="captcha_image")['src'].replace("..", "")
    
    max_attempts = 30
    confidence_threshold = 0.3
    for attempt in range(max_attempts):
        print(f"Tentativa {attempt+1}:")
        print("Baixando imagem de captcha...")
        captcha_image_path = download_image(session, captcha_image_url)
        
        print("Aplicando preprocessamento na imagem captcha...")
        preprocessed_image_path = preprocess_image(captcha_image_path)
        print("Aplicando OCR na imagem captcha...")
        captcha_text, confidence = apply_ocr(preprocessed_image_path)

        print(f"Tentativa {attempt + 1}: Texto detectado: {captcha_text} Com rating de confiança: {confidence}")

        if captcha_text and confidence >= confidence_threshold:
            print(f"Captcha quebrado com o texto: {captcha_text} e rating de confiança: {confidence}")
            data = {
                "captcha": captcha_text,
                "session": session
            }
            return data
        else:
            print(f"Rating de confiança {confidence} está abaixo do limite arbiitrado em {confidence_threshold}. Tentando novamente...")
            print("Obtendo imagem de captcha e dados de sessão...")
            response = session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            captcha_image_url = "https://rastreamento.correios.com.br/" + soup.find("img", id="captcha_image")['src'].replace("..", "")

    print(f"Falha na quebra do captcha após {max_attempts} tentativas.")
    return None

def download_image(session, url):
    response = session.get(url)
    image_path = 'captcha/original_img/downloaded_image.png'
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path


if __name__ == "__main__":
    obter_dados_request()