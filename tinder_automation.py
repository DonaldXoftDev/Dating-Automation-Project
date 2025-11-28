from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ChromeOptions
import os
import time
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




import logging
import datetime


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
LOGGER = setup_logger(LOGS_DIR)


class TinderAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.WEB_URL = 'https://tinder.com'
        self.logger = setup_logger(LOGS_DIR)

        #initiate the browser to open url
        self.driver.get(self.WEB_URL)
        self.is_logged_in = False
        self.login_to_tinder = LoginPage(self.driver)
        self.profile_interaction = ProfileInteractionPage(self.driver)
        self.dismiss_requests = DismissRequests(self.driver)
