"""Using Selenium WebDriver to navigate to website when running."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from decouple import config
import subprocess
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("sWebdriver")
LINK_URL = config('LINK_URL', default=None)

if LINK_URL is None:
    logger.info("Starting Django development server.")
    subprocess.Popen(['python', 'manage.py', 'runserver'])
    LINK_URL = 'http://127.0.0.1:8000/recipes/'
    time.sleep(5)

service = Service()
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)
driver.get(LINK_URL)
logger.info("Webpage opened successfully.")

try:
    while driver.window_handles:
        pass
finally:
    driver.quit()
    logger.info("Quit successfully.")
