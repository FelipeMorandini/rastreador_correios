# Rastreador de Pacotes dos Correios

Este projeto consiste em um script Python que automatiza a consulta de rastreamento de pacotes no site dos Correios do Brasil, superando o desafio do CAPTCHA apresentado durante o processo.

## Configuração do Ambiente

Para executar este projeto, é recomendável criar um ambiente virtual para isolar as dependências. Para isso, siga os passos abaixo:

1. Instale o Python em seu sistema, se ainda não estiver instalado.
2. Abra um terminal e navegue até o diretório do projeto.
3. Execute o seguinte comando para criar um ambiente virtual:

```bash
python -m venv venv
```

4. Ative o ambiente virtual.

No Windows, use:

```bash
.\venv\Scripts\Activate.ps1
```

No Linux ou macOS, use:

```bash
source venv/bin/activate
```

5. Com o ambiente virtual ativado, instale as dependências do projeto com o comando:

```bash
pip install -r requirements.txt
```

# Uso do Programa

Para rastrear um pacote, execute o script consulta_encomenda.py com o código de rastreamento como argumento:

```bash
python consulta_encomenda.py <codigo_de_rastreamento>
```

Por exemplo:

```bash
python consulta_encomenda.py LB571181225HK
```

# Como o Programa Funciona

O script faz uma requisição inicial para obter os dados de sessão e a imagem do CAPTCHA. Em seguida, aplica técnicas de pré-processamento de imagem e OCR (Reconhecimento Óptico de Caracteres) para extrair o texto do CAPTCHA.
Após isso, é feita uma requisição GET diretamente à API dos correios, retornando o JSON com o rastreamento do pacote.

# Bibliotecas Utilizadas:

requests: Para fazer requisições HTTP e manter a sessão com o servidor.
BeautifulSoup: Para analisar o HTML da página e extrair a URL da imagem do CAPTCHA.
PIL (Pillow): Para manipulação de imagens.
cv2 (OpenCV): Para pré-processamento de imagens.
easyocr: Para reconhecimento de texto na imagem do CAPTCHA.

# Limiar de Confiança do OCR:

O OCR nem sempre é capaz de reconhecer o texto corretamente devido a ruídos e distorções na imagem do CAPTCHA. Por isso, o script utiliza um limiar de confiança: se a confiança no texto reconhecido for baixa, o script tenta novamente, baixando uma nova imagem de CAPTCHA e repetindo o processo. Este limiar de confiança é ajustável no código e pode ser modificado conforme necessário.

# Contribuições

Contribuições para o projeto são bem-vindas. Sinta-se à vontade para clonar, enviar PRs ou abrir issues com sugestões e melhorias.

# Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.




