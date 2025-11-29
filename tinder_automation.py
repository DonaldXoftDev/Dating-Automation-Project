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

        self.expected_page_url = "/app/recs"

        #page object instances
        self.login_page = LoginPage(self.driver, self.logger)
        self.profile_interaction = ProfileInteractionPage(self.driver, self.logger)
        self.dismiss_requests = DismissRequests(self.driver, self.logger)

        #navigation locators
        self.NAVIGATE_TO_LOGIN_BTN = (By.XPATH, '//div[text()="Log in"]')
        self.FB_1ST_LOGIN_BTN_LOCATOR = (By.XPATH, '//div[text()="Log in with Facebook"]')

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
            return  True

        except TimeoutException:
            self.logger.warning("URL verification failed: Timed out waiting for the correct page.")
            return False

    def navigate_to_login(self):

        try:
            self.click_tinder_login() # there exist a nested try/except block in both methods
            self.click_tinder_fb_login_btn()
            return True

        except TimeoutException:
            self.logger.warning("Timed out while navigating to login page")
            return False

        except StaleElementReferenceException:
            logging.warning("Login button not fully loaded while navigating to login page")
            return False


    def login_sequence(self,user_name,pass_word):
        is_on_tinder_site = self.is_on_tinder()

        if not is_on_tinder_site:
            if not self.navigate_to_login():
                self.logger.warning("Login sequence failed")
                return False

            if not self.login_page.click_fb_login_btn():
                self.logger.warning("Login sequence failed")
                return False

            has_entered_credentials = (self.login_page.enter_user_name(user_name)
                                       and self.login_page.enter_password(pass_word))

            if not has_entered_credentials:
                self.logger.warning("Login sequence failed")
                return False
        return True




    def get_new_window(self, window_name):
        handle = self.driver.window_handles[1]
        if handle and handle not in self.driver.window_handles:
            self.logger.error(f'The window name {window_name} was not found in list of window handles ')
            return None

        self.driver.switch_to.window(handle)
        self.logger.info(f'Successfully switched to  {window_name} window')
        return handle

    def like_sequence(self):
        return True

    def teardown(self):
        pass

    def dismiss_all_popups(self):
        pass
    def run_dating_automation(self,user_name,pass_word):
        base_window = self.driver.window_handles[0]

        if not self.login_sequence(user_name,pass_word):
            self.logger.warning('Warning: Login sequence failed ')
            raise ValueError('Login sequence failed')

        fb_window = self.get_new_window('Facebook')


        if not fb_window:
            self.logger.warning('Warning: Facebook window was not found ')
            raise ValueError('Facebook window was not found ')

        self.driver.switch_to.window(base_window)
        self.logger.info('Switched back to base window ')

        if not self.like_sequence():
            raise ValueError('Liking sequence failed')

        self.teardown()


username = os.getenv("YOUR_USERNAME")
password = os.getenv("YOUR_PASSWORD")

dating_automation = TinderAutomation()
dating_automation.run_dating_automation(username, password)




