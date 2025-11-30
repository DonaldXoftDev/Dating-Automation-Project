import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import logging
import os


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

#create selenium user_profile
user_data_dir = os.path.join(os.getcwd(), 'chrome_profile')

#store profile info in specified directory
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')


from selenium.webdriver.support.wait import WebDriverWait

from base_page import BasePage
from utils import setup_logger,LOGS_DIR, username, password




class LoginPage(BasePage):
    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.current_web_title = self.driver.title.lower()

        #credentials

        self.fb_login_title = 'Facebook'
        self.tinder_title = 'Tinder | Match. Chat. Date.'

        #locators

        self.FB_LOGIN_BTN_LOCATOR = (By.ID, 'loginbutton')
        self.EMAIL_LOCATOR = (By.ID, 'email')
        self.PASSWORD_LOCATOR = (By.ID, 'pass')
        self.TEXT_ON_FB_PAGE = (By.ID, "homelink")
        self.CONTINUE_TO_FB_LOCATOR = (By.XPATH, '//span[text()="Continue as Itz IK"]')

        self.logged_in_tinder_url = "/app/recs"
        self.fb_window_url = '/login.ph'

        # navigation locators
        self.NAVIGATE_TO_LOGIN_BTN = (By.XPATH, '//div[text()="Log in"]')
        self.FB_1ST_LOGIN_BTN_LOCATOR = (By.XPATH, '//div[text()="Log in with Facebook"]')


    def navigate_to_login(self):

        try:
            self.click_tinder_login()  # there exist a nested try/except block in both methods
            self.click_tinder_fb_login_btn()
            return True

        except TimeoutException:
            self.logger.warning("Timed out while navigating to login page")
            return False


    def click_fb_login_btn(self):
        try:
            fb_login_btn = self.wait.until(
                ec.element_to_be_clickable(self.FB_LOGIN_BTN_LOCATOR)
            )
            fb_login_btn.click()
            self.logger.info("FB login button clicked")
            return True

        except TimeoutException:
            self.logger.info('Failed to click the facebook login button. Script timed out')
            return False

    def enter_user_name(self, username):
        try:
            email_element = self.driver.find_element(*self.EMAIL_LOCATOR)
            email_element.send_keys(username)
            self.logger.info('Entering email')
            return True

        except NoSuchElementException:
            self.logger.warning('Email element not found ')
            return False


    def enter_password(self,password):
        try:
            password_element = self.driver.find_element(*self.PASSWORD_LOCATOR)
            password_element.send_keys(password)
            self.logger.info('Entering password')
            return True

        except NoSuchElementException:
            self.logger.warning('Password element not found ')
            return False


    def click_continue_to_fb(self):
        try:
            continue_btn = self.wait.until(
                ec.element_to_be_clickable(self.CONTINUE_TO_FB_LOCATOR)
            )
            continue_btn.click()
            self.logger.info('Successfully clicked Continue button')
            return True

        except TimeoutException:
            self.logger.info('Failed to click Continue button')
            return False

    def enter_credentials(self,user_name, pass_word):
        self.enter_user_name(user_name)
        self.enter_password(pass_word)
        self.click_fb_login_btn()
        return True

    def click_tinder_fb_login_btn(self):
        try:
            fb_login_element = self.wait.until(
                ec.element_to_be_clickable(self.FB_1ST_LOGIN_BTN_LOCATOR)
            )
            fb_login_element.click()
            self.logger.debug('FB login with tinder button was clicked')
            return True

        except TimeoutException:
            self.logger.warning('FB login with tinder button was not found')
            return False

    def click_tinder_login(self):
        try:
            tinder_login_element = self.wait.until(
                ec.element_to_be_clickable(self.NAVIGATE_TO_LOGIN_BTN)
            )
            tinder_login_element.click()
            self.logger.debug('Clicking Tinder Login Button ...')
            return True

        except TimeoutException:
            self.logger.debug('Tinder Login Button was not found.')
            return False

    def is_on_tinder(self):
        try:
            self.wait.until(ec.url_contains(self.logged_in_tinder_url))
            self.logger.info(f'Url verification Successful for {self.logged_in_tinder_url}')
            return True

        except TimeoutException:
            self.logger.warning("URL verification failed: Attempting Initial login form home page")
            return False


class TestLoginPage:
    def __init__(self):

        self.web_url = 'https://www.tinder.com'
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.web_url)
        self.wait = WebDriverWait(self.driver, 15)
        self.logger = setup_logger(LOGS_DIR)

        self.login_mock = LoginPage(self.driver, self.logger)


    def get_new_window(self, base_window):
        try:
            fb_window = self.wait.until(
                ec.number_of_windows_to_be(2)
            )
            self.logger.info('The fb window handle have been found')

            if fb_window:
                for handle in self.driver.window_handles:
                    if handle != base_window:
                        return handle
                return None

        except TimeoutException:
            self.logger.warning('Failed to find the new window handle')
            return None


    def test_login_page(self, username, password):
        base_window = self.driver.window_handles[0]

        is_logged_in = self.login_mock.is_on_tinder()

        if not is_logged_in:
            if not self.login_mock.navigate_to_login():
                self.logger.critical('Initial login button Failed, Aborting')
                return False

            fb_window = self.get_new_window(base_window)
            if not fb_window:
                self.logger.warning('Facebook window pop up did not appear')
                return False

            self.logger.info('Attempting to switch to facebook window')
            self.driver.switch_to.window(fb_window)

            if not self.login_mock.enter_credentials(username, password):
                self.logger.critical('Failed to enter credentials')
                return False

            self.driver.switch_to.window(base_window)
            self.logger.info('Successfully switched back to tinder home page')

        return True


test_login = TestLoginPage()
test_login.test_login_page(username,password)
