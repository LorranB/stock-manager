from selenium import webdriver
from selenium.webdriver.edge.options import Options

def criar_driver():

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Edge(options=options)

    driver.implicitly_wait(10)

    return driver
