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

    def is_on_tinder(self):
        try:
            self.wait.until(ec.url_contains(self.expected_page_url))
            self.logger.info(f'Url verification Successful for {self.expected_page_url}')
            return  True

        except TimeoutException:
            self.logger.warning("URL verification failed: Timed out waiting for the correct page.")
            return False

        except Exception as e:
            self.logger.error(f'Unexpected error during URL check: {e}')
            return False

    def navigate_to_login(self):
        is_on_tinder_site = self.is_on_tinder()

        if not is_on_tinder_site:
            try:
                self.click_tinder_login()
                self.click_tinder_fb_login_btn()
                return True

            except TimeoutException:
                self.logger.warning("Timed out while navigating to login page")
                return False

            except StaleElementReferenceException:
                logging.warning("Login button not fully loaded while navigating to login page")
                return False


        self.is_logged_in = is_on_tinder_site
        return False



    def run_dating_automation(self):

        is_navigate_login = self.navigate_to_login()

        if  is_navigate_login:
            self.login_to_tinder.login_fb(is_navigate_login)

        if self.is_logged_in:
            self.dismiss_requests.dismiss_all_pop_up_requests()
            while True:
                is_hit = self.profile_interaction.hit_like_btn()
                if not is_hit:
                    break

dating_automation = TinderAutomation()
dating_automation.run_dating_automation()




