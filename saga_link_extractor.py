from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
import random
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


profile_path = '/Users/javier/Library/Application Support/Google/Chrome/Profile 1'

# Initialize Chrome options
options = Options()
options.add_argument(f'--user-data-dir={profile_path}')

# Initialize the service object with ChromeDriverManager
service = Service(ChromeDriverManager().install())  # Create a Service object

# Initialize the driver with the service and options
driver = webdriver.Chrome(service=service, options=options)

def saga():
  driver.get("https://www.falabella.com.pe/falabella-pe")
  driver.set_window_size(1440, 802)
  time.sleep(5)
  #driver.find_element(By.CLASS_NAME, 'airship-html-prompt-shadow').click()


  driver.set_window_size(1440, 802)
      # 3 | click | css=.airship-html-prompt-shadow | 
  try:
    driver.find_element(By.CSS_SELECTOR, ".airship-html-prompt-shadow").click()
        # 4 | click | css=.airship-html-prompt-shadow | 
    driver.find_element(By.CSS_SELECTOR, ".airship-html-prompt-shadow").click()
        # 5 | click | id=testId-modal-close | 
    driver.find_element(By.ID, "testId-modal-close").click()
  except:
    pass

  driver.find_element(By.CSS_SELECTOR, ".MarketplaceHamburgerBtn-module_icon__YC2PL").click()
  print("pasa aqui peirmeo")
  time.sleep(1)
  driver.find_element(By.CLASS_NAME, "FirstLevelCategories-module_categoryTitle__1PTiQ").click()


  cat = driver.find_elements(By.XPATH,'//*[@id="scrollable-content"]/div/div[2]/div/div[2]/div/div[2]/div/ul[1]/li[1]')

  for i in cat:
     print(i.text())

 


  # elements = driver.find_elements(By.CLASS_NAME, "SecondLevelCategories-module_secondLevelCategory__")

  # //*[@id="scrollable-content"]/div/div[2]/div/div[2]/div/div[2]/div/ul[1]
  # //*[@id="scrollable-content"]/div/div[2]/div/div[2]/div/div[2]/div/ul[2]




  for i in elements:
 
    print(i)
     #print(i.find_element(By.TAG_NAME,"a").get_attribute('href'))
  # Extract URLs
  # urls = [element.get_attribute('href') for element in elements]

  # # Output URLs
  # for url in urls:
  #     print(url)




  # elements = driver.find_elements(By.CLASS_NAME, "SecondLevelCategories-module_secondLevelCategory__3SPXi")

  # for i in elements:
  #    print(i.text())
# # Collect href attributes from each element
#   urls = []
#   for element in elements:
#       # Assuming each element contains an <a> tag
#       anchor = element.find_element(By.TAG_NAME, 'a')
#       urls.append(anchor.get_attribute('href'))

#   # Now 'urls' contains all the hrefs collected from the elements
#   print(urls)


  # <div class="FirstLevelCategories-module_categoryTitle__1PTiQ">Tecnología</div>



  # driver.find_element(By.XPATH, '//*[@id="testId-HamburgerBtn-toggle"]/div[1]').click()
  # driver.find_element(By.CSS_SELECTOR, ".SecondLevelCategories-module_secondLevelCategory__3SPXi:nth-child(1) > .SecondLevelCategories-module_thirdLevelCategory__2ZQFF:nth-child(3) > a").click()


  # element = driver.find_element(By.CSS_SELECTOR, "body")
  # actions = ActionChains(driver)
  # actions.move_to_element(element, 0, 0).perform()
  # driver.find_element(By.CSS_SELECTOR, ".SecondLevelCategories-module_secondLevelCategory__3SPXi:nth-child(1) > .SecondLevelCategories-module_thirdLevelCategory__2ZQFF:nth-child(3) > a").click()
  # element = driver.find_element(By.LINK_TEXT, "Apple")
  # actions = ActionChains(driver)
  # actions.move_to_element(element).perform()
  # element = driver.find_element(By.CSS_SELECTOR, "body")
  # actions = ActionChains(driver)
  # actions.move_to_element(element, 0, 0).perform()

try:
  saga()
except NoSuchElementException:
    print("Error: The element could not be found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Don't forget to close the driver
    driver.quit()