from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging

class DismissRequests:
    def __init__(self, driver):
        self.driver = driver
        self.LOCATION_LOCATOR = ''
        self.NOTIFICATION_LOCATOR = ''
        self.COOKIES_LOCATOR = ''

        self.locators_list = [
            {'locator': self.LOCATION_LOCATOR, 'description': 'allow for locator popup'},
            {'locator': self.NOTIFICATION_LOCATOR, 'description': 'not interested for notification popup'},
            {'locator': self.COOKIES_LOCATOR, 'description': 'I accept for cookies popup'},
        ]

        self.wait = WebDriverWait(driver, 10)
        self.logging = logging.getLogger('DatingAutomationLogger')
        self.request_description = None


    def dismiss_requests(self,locator, description):

        try:
            request = self.wait.until(
                ec.presence_of_element_located(*locator)
            )
            self.request_description = request.text

            request.click()
            self.logging.info(f'Clicked {description} ')
            return True, f'Clicked {description} '

        except TimeoutException:
            self.logging.error(f'Timeout while trying to click {description}')
            return False, f'Timeout while trying to click {description}'

    def dismiss_all_pop_up_requests(self):
        for item in self.locators_list:
            locator = item['locator']
            description = item['description']
            is_request_dismissed, message = self.dismiss_requests(locator, description)

            if not is_request_dismissed:
                raise ValueError(message)








