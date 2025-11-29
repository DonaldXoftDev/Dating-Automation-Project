from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import logging

from base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.current_web_title = self.driver.title.lower()

        #credentials

        self.fb_login_title = 'Facebook'
        self.tinder_title = 'Tinder | Match. Chat. Date.'

        #locators

        self.FB_LOGIN_BTN_LOCATOR = (By.NAME, 'login')
        self.EMAIL_LOCATOR = (By.ID, 'email')
        self.PASSWORD_LOCATOR = (By.ID, 'pass')
        self.TEXT_ON_FB_PAGE = (By.ID, "homelink")
        self.CONTINUE_TO_FB_LOCATOR = (By.XPATH, '//span[text()="Continue as Itz IK"]')

        self.expected_page_url = "/app/recs"

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

    def navigation_sequence(self):
        is_on_tinder_site = self.is_on_tinder()

        if not is_on_tinder_site:
            if not self.navigate_to_login():
                self.logger.warning("Login sequence failed")
                return False

            if not self.click_fb_login_btn():
                self.logger.warning("Login sequence failed")
                return False

        return True


    def click_fb_login_btn(self):
        try:
            fb_login_btn = self.wait.until(
                ec.presence_of_element_located(self.FB_LOGIN_BTN_LOCATOR)
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
                ec.presence_of_element_located(self.CONTINUE_TO_FB_LOCATOR)
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

    def click_tinder_fb_login_btn(self):
        try:
            fb_login_element = self.wait.until(
                ec.presence_of_element_located(self.FB_1ST_LOGIN_BTN_LOCATOR)
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
                ec.presence_of_element_located(self.NAVIGATE_TO_LOGIN_BTN)
            )
            tinder_login_element.click()
            self.logger.debug('Clicking Tinder Login Button ...')
            return True

        except TimeoutException:
            self.logger.debug('Tinder Login Button was not found.')
            return False

    def is_on_tinder(self):
        try:
            self.wait.until(ec.url_contains(self.expected_page_url))
            self.logger.info(f'Url verification Successful for {self.expected_page_url}')
            return True

        except TimeoutException:
            self.logger.warning("URL verification failed: Timed out waiting for the correct page.")
            return False


        except StaleElementReferenceException:
            logging.warning("Login button not fully loaded while navigating to login page")
            return False
