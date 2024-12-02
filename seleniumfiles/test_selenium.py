from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decouple import config
import logging

logger = logging.getLogger("testSelenium")
LINK_URL = config('LINK_URL', default='http://127.0.0.1:8000/recipes/')

service = Service()
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)
driver.get(LINK_URL)
logger.info("Webpage opened successfully.")

wait = WebDriverWait(driver, 20)

filter_button = wait.until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        'span.btn-outline-success')))
filter_button.click()
logger.info("Filter button clicked successfully.")

vegan_button = wait.until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        'button[data-diet="Vegan"]')))
vegan_button.click()
logger.info("Vegan button clicked successfully.")

search_button = wait.until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        'button.btn.btn-success.border-start-0.border.rounded-left.form-control.mt-2[type="submit"]')))
search_button.click()
logger.info("Search button clicked successfully.")

recipe = wait.until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        '.row .card:first-child')))
recipe.click()
logger.info("Recipe clicked successfully.")

nutrition = wait.until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        'a.primary.mx-2.nutrients[data-bs-toggle="modal"][data-bs-target="#nutritionModal"]')))
driver.execute_script("arguments[0].scrollIntoView(true);", nutrition)
driver.execute_script("arguments[0].click();", nutrition)
logger.info("Nutrition clicked successfully.")

try:
    while driver.window_handles:
        pass
finally:
    driver.quit()
    logger.info("Quit successfully.")
