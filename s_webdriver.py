from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def main():
    service = Service(log_path="NUL")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://project-pantry.onrender.com/")

    try:
        while driver.window_handles:
            pass
    except KeyboardInterrupt:
        print("Exiting script...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
