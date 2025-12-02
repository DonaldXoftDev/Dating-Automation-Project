from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self,driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(self.driver, 15)


