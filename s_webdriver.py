from selenium import webdriver


def main():
    driver = webdriver.Chrome()
    driver.get("https://project-pantry.onrender.com/")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        driver.quit()


if __name__ == "__main__":
    main()
