from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ChromeOptions
import os
import time
import logging
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from dotenv import load_dotenv
from login_page import LoginPage
from profile_interaction_page import ProfileInteractionPage
from dismiss_request import DismissRequests

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

#create selenium user_profile
user_data_dir = os.path.join(os.getcwd(), 'chrome_profile')

#store profile info in specified directory
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')


from utils import setup_logger, LOGS_DIR

# Call this once to get your logger object

class TinderAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.WEB_URL = 'https://tinder.com'
        self.logger = setup_logger(LOGS_DIR)
        self.wait = WebDriverWait(self.driver, 10)

        #initiate the browser to open url
        self.driver.get(self.WEB_URL)

        #page object instances
        self.login_page = LoginPage(self.driver, self.logger)
        self.profile_interaction = ProfileInteractionPage(self.driver, self.logger)
        self.dismiss_requests = DismissRequests(self.driver, self.logger)


    def get_new_window(self, base_window):
        for handle in self.driver.window_handles:
            if handle != base_window:
                return handle
        return None

    def like_sequence(self):
        return True

    def teardown(self):
        pass

    def dismiss_all_popups(self):
        pass

    def run_dating_automation(self, user_name, pass_word):
        base_window = self.driver.window_handles[0]

        is_logged_in = self.login_page.is_on_tinder()

        if not is_logged_in:
            if not self.login_page.navigate_to_login():
                self.logger.critical('Initial login button Failed, Aborting')
                return False

            fb_window = self.get_new_window(base_window)
            if not fb_window:
                self.logger.warning('Facebook window pop up did not appear')
                return False

            self.logger.info('Attempting to switch to facebook window')
            self.driver.switch_to.window(fb_window)

            if not self.login_page.enter_credentials(user_name, pass_word):
                self.logger.critical('Failed to enter credentials')
                return False

            self.driver.switch_to.window(base_window)
            self.logger.info('Successfully switched back to tinder home page')

        return True



# dating_automation = TinderAutomation()
# dating_automation.run_dating_automation(username, password)
