from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from base_page import BasePage


class DismissRequests(BasePage):

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

        self.LOCATION_LOCATOR = (By.XPATH, '//div[text()="Allow"]')
        self.NOTIFICATION_LOCATOR = (By.XPATH, '//div[text()="I’ll miss out"]')
        # self.COOKIES_LOCATOR = (By.XPATH, )

        self.locators_list = [
            {'locator': self.LOCATION_LOCATOR, 'description': 'allow for locator popup'},
            {'locator': self.NOTIFICATION_LOCATOR, 'description': 'not interested for notification popup'},
            # {'locator': self.COOKIES_LOCATOR, 'description': 'I accept for cookies popup'},
        ]

    def dismiss_requests(self,locator, description):

        try:
            request = self.wait.until(
                ec.presence_of_element_located(locator)
            )

            request.click()
            self.logger.info(f'Clicked {description} ')
            return True, f'Clicked {description} '

        # except NoSuchElementException:
        #     self.logger.error(f'{description} Not found, skipping element')
        #     return True, f'{description} Not found, skipping element'

        except TimeoutException:
            self.logger.error(f'Timeout while trying to click {description}, skipping element')
            return True, f'Timeout while trying to click {description}, skipping element'

        except Exception as e:
            self.logger.error(e)
            return False, f'Unexpected error while trying to click element {description}'


    def dismiss_all_pop_up_requests(self):
        for item in self.locators_list:
            locator = item['locator']
            description = item['description']
            is_request_dismissed, message = self.dismiss_requests(locator, description)

            if not is_request_dismissed:
                raise ValueError(message)








