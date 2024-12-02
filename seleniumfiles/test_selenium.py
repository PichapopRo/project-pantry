"""Using Selenium WebDriver to navigate to website when running."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


service = Service(log_path="NUL")
options = webdriver.ChromeOptions()
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://project-pantry-rose.vercel.app/")
print("Webpage opened successfully...")

button = driver.find_element(By.ID, "login-btn")
button.click()


try:
    while driver.window_handles:
        pass
except KeyboardInterrupt:
    print("Exiting script...")
finally:
    driver.quit()
