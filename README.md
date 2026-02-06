## Script Python para envio automático de mensagens pelo WhatsApp Web

Este documento descreve o script Python para enviar mensagens automáticas para uma lista de números usando Selenium.

---

### Requisitos

* Python 3.x
* Pacotes Python:

  * pandas
  * selenium
* Navegador Chromium
* Chromedriver compatível com a versão do Chromium

---

### Estrutura do Excel

O arquivo `dados.xlsx` deve ter duas colunas:

| Numero    | Mensagem            |
| --------- | ------------------- |
| 123456789 | "Sua mensagem aqui" |
| 123456789 | "Sua mensagem aqui" |
| ...       | ...                 |

> Observação: A coluna `Numero` deve conter apenas os números do celular sem DDD ou símbolos. O DDD `81` e o código do Brasil `+55` são adicionados pelo script.

---

### Código Python

```python
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import urllib

# Carregar contatos
contatos_df = pd.read_excel('dados.xlsx')
print(contatos_df)

# Configuração do Chrome
chrome_options = Options()
chrome_options.binary_location = '/usr/bin/chromium-browser'
service = Service('/usr/bin/chromedriver')
navegador = webdriver.Chrome(service=service, options=chrome_options)

# Abrir WhatsApp Web
navegador.get("https://web.whatsapp.com/")

# Esperar carregar a página inicial
while len(navegador.find_elements(By.ID, 'side')) < 1:
    time.sleep(1)

# Loop para enviar mensagens
for i, mensagem in enumerate(contatos_df['Mensagem']):
    numero = contatos_df.loc[i, 'Numero']
    texto = urllib.parse.quote(f'{mensagem}')
    link = f'https://web.whatsapp.com/send?phone=+5581{numero}&text={texto}'
    navegador.get(link)

    try:
        # Esperar carregar o chat ou aviso de número inválido
        WebDriverWait(navegador, 10).until(
            lambda d: d.find_elements(By.ID, 'side') or d.find_elements(By.XPATH, '//div[contains(text(), "não é um número válido")]')
        )

        # Verificar se número inválido
        try:
            erro_numero = navegador.find_element(By.XPATH, '//div[contains(text(), "não é um número válido")]')
            print(f"Número inválido: {numero}, pulando...")
            continue
        except NoSuchElementException:
            pass

        # Campo de mensagem
        campo_msg = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//footer//div[@contenteditable="true"]'))
        )
        time.sleep(2)  # Espera extra para estabilidade
        campo_msg.send_keys(Keys.ENTER)
        print(f"Mensagem enviada para {numero}")

    except TimeoutException:
        print(f"Erro ao acessar o número {numero}, pulando...")
        continue

    time.sleep(5)  # Delay entre envios

input("Pressione ENTER para fechar o navegador...")
```

---

### Observações

* Escaneie o QR code do WhatsApp Web antes do envio.
* Evite enviar muitas mensagens rapidamente para não ser bloqueado temporariamente.
* Certifique-se de que o Chromedriver é compatível com sua versão do Chromium.
* Todos os números devem ser válidos e estar no formato correto, caso contrário o script pula automaticamente.
