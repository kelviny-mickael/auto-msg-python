# ------------------------------ Válido 2 ----------------------------------------- #

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
    # pessoa = contatos_df.loc[i, 'Pessoa']
    numero = contatos_df.loc[i, 'Numero']
    texto = urllib.parse.quote(f'{mensagem}')
    link = f'https://web.whatsapp.com/send?phone=+5581{numero}&text={texto}'
    navegador.get(link)

    try:
        # Esperar carregar o chat ou o aviso de número inválido
        WebDriverWait(navegador, 10).until(
            lambda d: d.find_elements(By.ID, 'side') or d.find_elements(By.XPATH, '//div[contains(text(), "não é um número válido")]')
        )

        # Verificar se número inválido
        try:
            erro_numero = navegador.find_element(By.XPATH, '//div[contains(text(), "não é um número válido")]')
            print(f"Número inválido: {numero}, pulando...")
            continue  # pula para o próximo contato
        except NoSuchElementException:
            pass

        # Campo de mensagem
        campo_msg = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//footer//div[@contenteditable="true"]'))
        )
        campo_msg.send_keys(Keys.ENTER)
        print(f"Mensagem enviada para {numero}")

    except TimeoutException:
        print(f"Erro ao acessar o número {numero}, pulando...")
        continue

    time.sleep(5)

input("Pressione ENTER para fechar o navegador...")