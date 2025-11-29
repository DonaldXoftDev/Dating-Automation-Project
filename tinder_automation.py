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

    logging.basicConfig(
        # Save messages to the defined file
        filename=full_path,
        # ... (Keep existing file setup and format) ...
        level=logging.INFO,  # Set your primary app level to INFO (or DEBUG if you need detail)
        # Define the format of the log message
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )

    #  Silence the Noise (Crucial Step!)
    # Set the log level of Selenium's low-level communication to WARNING or higher
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

    # Set the log level of the underlying HTTP connection pool to WARNING
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    #  Return your application logger
    return logging.getLogger('DatingAutomationLogger')  # Use your application's logger name


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

        if not self.navigation_sequence(user_name, pass_word):
            self.logger.warning('Warning: Login sequence failed ')
            return False

        self.logger.info('Attempting to switch to facebook window')
        fb_window = self.get_new_window('Facebook')

        if not fb_window:
            self.logger.warning('Warning: Facebook window did not appear')
            return False

        self.logger.info('Successfully switched to facebook window')

        if not self.login_page.enter_credentials:
            self.logger.warning("Failed to enter user credentials, the fields were not found")
            return False

        self.driver.switch_to.window(base_window)
        self.logger.info('Switching back to Tinder base window ')

        if not self.like_sequence():
            raise ValueError('Liking sequence failed')

        self.teardown()


username = os.getenv("YOUR_USERNAME")
password = os.getenv("YOUR_PASSWORD")

dating_automation = TinderAutomation()
dating_automation.run_dating_automation(username, password)
