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

LOGS_DIR = "logs"

def setup_logger(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the full file path
    log_filename = datetime.datetime.now().strftime("automation_%Y%m%d_%H%M%S.log")
    full_path = os.path.join(directory, log_filename)

    # Configure the basic settings
    logging.basicConfig(
        # Save messages to the defined file
        filename=full_path,
        # Set the minimum level to save: DEBUG means save everything
        level=logging.DEBUG,
        # Define the format of the log message
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )
    #  Get the main logger object you'll use everywhere
    return logging.getLogger('DatingAutomationLogger')


# Call this once to get your logger object

class TinderAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.WEB_URL = 'https://tinder.com'
        self.logger = setup_logger(LOGS_DIR)
        self.wait = WebDriverWait(self.driver, 10)

        #initiate the browser to open url
        self.driver.get(self.WEB_URL)
        self.is_logged_in = False

        self.expected_page_url = "/app/recs"

        #page object instances
        self.login_to_tinder = LoginPage(self.driver,self.logger)
        self.profile_interaction = ProfileInteractionPage(self.driver, self.logger)
        self.dismiss_requests = DismissRequests(self.driver, self.logger)

        #navigation locators
        self.NAVIGATE_TO_LOGIN_BTN = (By.XPATH, '//div[text()="Log in"]')
        self.FB_1ST_LOGIN_BTN_LOCATOR = (By.XPATH, '//div[text()="Log in with Facebook"]')

    def click_tinder_fb_login_btn(self):
        fb_login_element = self.wait.until(
            ec.presence_of_element_located(self.FB_1ST_LOGIN_BTN_LOCATOR)
        )
        fb_login_element.click()

    def click_tinder_login(self):
        tinder_login_element = self.wait.until(
            ec.presence_of_element_located(self.NAVIGATE_TO_LOGIN_BTN)
        )
        tinder_login_element.click()

    def navigate_to_login(self):
        self.driver.get(self.WEB_URL)

        is_on_tinder_site = True if self.wait.until(ec.url_contains(self.expected_page_url)) else False

        if not is_on_tinder_site:
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
        else:
            self.is_logged_in = is_on_tinder_site



    def run_dating_automation(self):

        is_navigate_login = self.navigate_to_login()
        self.login_to_tinder.login_fb(is_navigate_login)

        if self.is_logged_in:
            self.dismiss_requests.dismiss_all_pop_up_requests()
            while True:
                is_hit = self.profile_interaction.hit_like_btn()
                if not is_hit:
                    break





