from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service


# Ruta al ChromeDriver local en tu máquina
chrome_driver_path = "/Users/javier/GIT/scrapy_saga/chromedriver"


service = Service(executable_path="/Users/javier/GIT/scrapy_saga/chromedriver")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Abrir la página de Falabella Perú
    driver.get("https://www.falabella.com.pe/falabella-pe")
    time.sleep(5)  # Esperar 5 segundos para que la página cargue completamente

  # Esperar hasta que el elemento del popup esté presente en el DOM
    popup_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.airship-html-prompt-shadow'))
    )

    # Obtener el Shadow Root del elemento popup
    shadow_root_script = 'return arguments[0].shadowRoot'
    shadow_root = driver.execute_script(shadow_root_script, popup_element)

    # Encontrar el elemento dentro del Shadow DOM que queremos cerrar
    close_button = shadow_root.find_element(By.CSS_SELECTOR, 'div.airship-alert-buttons button.airship-btn-deny')

    # Hacer clic en el botón para cerrar el popup
    close_button.click()



    # Esperar unos segundos para ver el resultado del clic
 

  # Esperar hasta que el elemento esté presente y visible en el DOM
    element_menu = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Menú")]'))
    )

    # Hacer clic en el elemento
    element_menu.click()

    print("le dio click al carrito")

    time.sleep(5)  # Esperar 5 segundos para ver el resultado del clic

      # Localizar el elemento "Tecnología" y hacer clic
    tecnologia_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.FirstLevelCategories-module_categoryTitle__1PTiQ"))
    )
    tecnologia_element.click()

    time.sleep(5)  # Esperar 5 segundos para ver el resultado del clic

     # Esperar un momento para que cargue la nueva sección
    scroll_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'SecondLevelCategories-module_secondLevelMenuItemsBox__2i00Y'))
        
    )

    links = driver.find_element(By.CLASS_NAME,"SecondLevelCategories-module_secondLevelMenuItemsBox__2i00Y")

    print(links.text)
    time.sleep(30)
    urls = links.find_elements(By.TAG_NAME, 'li')

    for li in urls :
        link_elements = li.find_elements(By.TAG_NAME, 'a')
        for link in link_elements:
            href = link.get_attribute('href')
            print(href)

    # print(scroll_container)
    # time.sleep(100)

    # # Encontrar todos los elementos <li> dentro del contenedor de scroll
    # li_elements = scroll_container.find_elements(By.TAG_NAME, 'li')

    # # Lista para almacenar los enlaces
    # links = []

    # # Iterar sobre cada <li> y encontrar los enlaces <a> dentro de ellos
    # for li in li_elements:
    #     link_elements = li.find_elements(By.TAG_NAME, 'a')
    #     for link in link_elements:
    #         href = link.get_attribute('href')
    #         print(href)
    #         if href:
    #             links.append(href)

    # Imprimir los enlaces encontrados
    #print(links)

finally:
    # Cerrar el navegador
    driver.quit()