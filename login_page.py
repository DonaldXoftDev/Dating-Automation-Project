import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ChromeOptions
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.WEB_URL = "https://tinder.com"
        self.current_web_title = self.driver.title.lower()

        #credentials
        self.username = os.getenv("YOUR_USERNAME")
        self.password = os.getenv("YOUR_PASSWORD")

        self.wait = WebDriverWait(self.driver, 10)

        #window instances

        #logger instance
        self.logger = logging.getLogger('DatingAutomationLogger')
        self.fb_login_title = 'Facebook'
        self.tinder_title = 'Tinder | Match. Chat. Date.'

        #locators
        self.NAVIGATE_TO_LOGIN_BTN = (By.XPATH, '//div[text()="Log in"]')
        self.FB_1ST_LOGIN_BTN_LOCATOR = (By.XPATH, '//div[text()="Log in with Facebook"]')
        self.FB_LOGIN_BTN_LOCATOR = (By.NAME, 'login')
        self.EMAIL_LOCATOR = (By.ID, 'email')
        self.PASSWORD_LOCATOR = (By.ID, 'pass')
        self.TEXT_ON_FB_PAGE = (By.ID, "homelink")

    def click_tinder_login(self):
        tinder_login_element = self.wait.until(
            ec.presence_of_element_located(self.NAVIGATE_TO_LOGIN_BTN)
        )
        tinder_login_element.click()

    def click_tinder_fb_login_btn(self):
        fb_login_element = self.wait.until(
            ec.presence_of_element_located(self.FB_1ST_LOGIN_BTN_LOCATOR)
        )
        fb_login_element.click()

    def navigate_to_login(self):
        self.driver.get(self.WEB_URL)

        try:
            self.click_tinder_login()
            self.click_tinder_fb_login_btn()
            return True

        except TimeoutException:
            logging.warning("Timed out while navigating to login page")
            return False

        except StaleElementReferenceException:
            logging.warning("Login button not fully loaded while navigating to login page")
            return False

    def click_fb_login_btn(self):
        try:
            fb_login_btn = self.wait.until(
                ec.presence_of_element_located(self.FB_LOGIN_BTN_LOCATOR)
            )
            fb_login_btn.click()

        except TimeoutException:
            logging.info('Failed to click the facebook login button. Script timed out')
            raise Exception("Failed to click the facebook login button. Script timed out")

    def enter_email(self):
        email_element = self.driver.find_element(*self.EMAIL_LOCATOR)
        email_element.send_keys(self.username)
        print(self.username)

    def enter_password(self):
        password_element = self.driver.find_element(*self.PASSWORD_LOCATOR)
        password_element.send_keys(self.password)
        print(self.password)

    def switch_window_and_verify(self, new_window, new_window_title):
        self.driver.switch_to.window(new_window)

        try:
            self.wait.until(
                ec.presence_of_element_located(self.TEXT_ON_FB_PAGE)
            )
            new_window_title = new_window_title.lower()
            print(new_window_title)
            print(self.current_web_title)

            if self.current_web_title == new_window_title:
                pass

        except TimeoutException:
            raise ValueError(f'Page Timed out while switching to {new_window_title}')

        except new_window_title == 'new tab':
            logging.info(f'Failed to switch to {new_window_title}, page still in {self.current_web_title}')
            raise ValueError(f"Failed to switch to {new_window_title},page still in {self.current_web_title}")

    def login_fb(self):
        is_navigate_login = self.navigate_to_login()

        if not is_navigate_login:
            raise ValueError('Login failed due to timeout while navigating to login page')

        if not self.username or not self.password:
            logging.info("No username or password saved in the .env file")
            raise ValueError("No username or password saved to .env file")

        base_window = self.driver.window_handles[0]
        time.sleep(1)
        fb_login_window = self.driver.window_handles[1]

        #switch to fb page
        self.switch_window_and_verify(fb_login_window, self.fb_login_title)

        self.enter_email()
        self.enter_password()
        self.click_fb_login_btn()

        #switch back to tinder page
        self.switch_window_and_verify(base_window, self.tinder_title)
