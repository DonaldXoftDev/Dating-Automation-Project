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
#create selenium user_profile
user_data_dir = r"C:\Users\hp\Desktop\ChromeAutomationData"
chrome_options = ChromeOptions()

chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument('--headless=new') # Use 'new' for modern Chrome versions

# 2. Add the clean user data directory
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

# # 3. Add necessary stability flags for headless mode
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

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

    def run_dating_automation(self):
        is_logged_in = self.login_page.is_on_tinder()

        self.logger.info('Dating automation project is starting...')
        if is_logged_in:
            if not self.dismiss_requests.dismiss_all_pop_up_requests():
                self.logger.warning("Couldn't dismiss all pop up request")

            profile_exists = True
            profile_swipe_limit = 100

            self.logger.info('Initiating Like sequence...')
            while profile_exists:
                self.profile_interaction.hit_like_btn()
                profile_swipe_limit -= 1

                if profile_swipe_limit == 0:
                    profile_exists = False
                    self.logger.info('All profiles have been exhausted for the day. Try again tomorrow.')




# dating_automation = TinderAutomation()
# dating_automation.run_dating_automation()
