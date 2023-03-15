import acesso

import time
import shutil
import sys

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("disable-extensions")
#options.add_argument("headless")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(acesso.URL)

driver.find_element("id", "ctl00_ContentPlaceHolder1_cxt_matricula_usuario").send_keys(acesso.USER)
driver.find_element("id", "ctl00_ContentPlaceHolder1_cxt_senha").send_keys(acesso.PASS + Keys.RETURN)

driver.get(acesso.URL + "/ocorrencia.aspx")

driver.find_element("name", "ctl00$ContentPlaceHolder1$bt_procurar").click()

driver.find_element("name", "ctl00$ContentPlaceHolder1$cxt_data_ini").clear()
driver.find_element("name", "ctl00$ContentPlaceHolder1$cxt_data_ini").send_keys("01/01/2020")
driver.find_element("name", "ctl00$ContentPlaceHolder1$bt_procurar").click()

driver.find_element("id", "ctl00_ContentPlaceHolder1_lnk_export").click()

driver.execute_script("window.open()")
driver.switch_to.window(driver.window_handles[-1])
driver.get('chrome://downloads')
espera_download = time.time() + 180
while True:
    try:
        downloadPercentage = driver.execute_script(
            "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
        if downloadPercentage == 100:
            nome_arquivo = driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
            break
    except:
        pass
    
    if time.time() > espera_download:
        sys.exit("Download demorou muito\nSaindo...")

time.sleep(3)

arquivo_downloads = str(Path.home() / "Downloads" / nome_arquivo)

shutil.move(arquivo_downloads, acesso.DESTINO)

driver.close()