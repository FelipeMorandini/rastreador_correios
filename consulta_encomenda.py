import sys
import json
from obter_dados_request import obter_dados_request

def track_package(tracking_code):
    max_attempts = 10
    attempt = 0
    
    print(f"Iniciando busca para o pacote {tracking_code}...")

    while attempt < max_attempts:
        attempt += 1
        print(f"Tentativa {attempt}:")
        data = obter_dados_request()

        if not data:
            print("Falha na obtenção do captcha. Tentando novamente...")
            continue

        captcha_text = data["captcha"]
        session = data["session"]

        print("Captcha e dados de sessão obtidos. Iniciando busca...")
        
        track_url = f"https://rastreamento.correios.com.br/app/resultado.php?objeto={tracking_code}&captcha={captcha_text}&mqs=S"
        response = session.get(track_url)

        try:
            response_json = response.json()
            if response_json.get('erro') == 'true':
                print(f"Attempt {attempt}: Erro: {response_json.get('mensagem')}. Tentando novamente...")
                continue

            eventos = response_json.get('eventos', [])
            if eventos:
                title = eventos[0].get('descricao', '')
                unidade = eventos[0].get('unidade', {})
                unidadeDestino = eventos[0].get('unidadeDestino', {})
                message = f"{unidade.get('tipo', '')}, {unidade.get('endereco', {}).get('cidade', '')} - {unidade.get('endereco', {}).get('uf', '')}"
                if unidadeDestino:
                    message += f" para {unidadeDestino.get('tipo', '')}, {unidadeDestino.get('endereco', {}).get('cidade', '')} - {unidadeDestino.get('endereco', {}).get('uf', '')}"
                result = {
                    "status": "success",
                    "code": tracking_code,
                    "data": {
                        "title": title,
                        "message": message
                    }
                }
                print(json.dumps(result, ensure_ascii=False))
                break
            else:
                result = {
                    "status": "success",
                    "code": tracking_code,
                    "data": {
                        "title": "Não há eventos para este pacote",
                        "message": "N/A"
                    }
                }
                print(json.dumps(result, ensure_ascii=False))
                break

        except json.JSONDecodeError as e:
            print(f"Tentativa {attempt}: Falha na resposta: {e}. Tentando novamente...")

    if attempt == max_attempts:
        print("Máximo de tentativas alcançado...")
        result = {"status": "error", "code": tracking_code, "data": None}
        print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python consulta_encomenda.py <tracking_code>")
        sys.exit(1)

    tracking_code = sys.argv[1]
    track_package(tracking_code)