from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
chrome_driver_path = "//Users//javier//GIT//scrapy_saga//sele-urls//chromedriver"

# Create a new instance of the Firefox driver
#driver = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path), options=options)


# Step 1
driver.get("https://simple.ripley.com.pe/")

# Step 2
driver.set_window_size(1680, 947)

# Step 3
driver.find_element(By.CSS_SELECTOR, ".menu-button__icon").click()

# Step 4
driver.find_element(By.CSS_SELECTOR, ".category-item-tecnologia").click()

# Step 5
element = driver.find_element(By.XPATH, "//a[@id='tv_todas']").click
time.sleep(10)
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Step 6
element = driver.find_element(By.CSS_SELECTOR, "body")
actions = ActionChains(driver)
actions.move_to_element(element, 0, 0).perform()

# Step 7
driver.find_element(By.ID, "tv_todas").click()

# Step 8
driver.find_element(By.CSS_SELECTOR, ".menu-button__icon").click()

# Step 9
driver.find_element(By.CSS_SELECTOR, ".category-item-tecnologia").click()

# Step 10
element = driver.find_element(By.CSS_SELECTOR, ".category-item-tecnologia")
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Step 11
element = driver.find_element(By.CSS_SELECTOR, "body")
actions = ActionChains(driver)
actions.move_to_element(element, 0, 0).perform()

# Step 12
driver.find_element(By.CSS_SELECTOR, ".category-tree-container-expanded__main-category-link use").click()

# Step 13
driver.find_element(By.ID, "home_theaters_tv_tec").click()

# Step 14
driver.find_element(By.CSS_SELECTOR, ".menu-button").click()

# Step 15
driver.find_element(By.ID, "streaming_tv").click()

# Step 16
element = driver.find_element(By.LINK_TEXT, "Smart Home")
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Step 17
element = driver.find_element(By.CSS_SELECTOR, "body")
actions = ActionChains(driver)
actions.move_to_element(element, 0, 0).perform()

# Step 18
driver.find_element(By.CSS_SELECTOR, ".menu-button").click()

# Step 19
driver.find_element(By.ID, "accesorios_tv").click()

# Step 20
driver.find_element(By.CSS_SELECTOR, ".menu-button").click()

# Step 21
driver.find_element(By.ID, "racks").click()

# Step 22
driver.find_element(By.CSS_SELECTOR, ".menu-button").click()

# Step 23
driver.find_element(By.ID, "Scanners_proyectores").click()

# Step 24
element = driver.find_element(By.CSS_SELECTOR, "#llamado-2enlaces > .cint-der")
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Step 25
element = driver.find_element(By.CSS_SELECTOR, "body")
actions = ActionChains(driver)
actions.move_to_element(element, 0, 0).perform()

# Close the browser window
driver.quit()
