"""Using Selenium WebDriver to navigate to website when running."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from decouple import config

LINK_URL = config('LINK_URL', default='http://127.0.0.1:8000/recipes/')

service = Service(log_path="NUL")
options = webdriver.ChromeOptions()
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=service, options=options)
driver.get(LINK_URL)
print("Webpage opened successfully...")

try:
    while driver.window_handles:
        pass
except KeyboardInterrupt:
    print("Exiting script...")
finally:
    driver.quit()
