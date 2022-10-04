import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture()
def driver():
    driver_srvice = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(servise=driver_srvice)
    driver.maximize_window()

    yield driver

    driver.quit()


