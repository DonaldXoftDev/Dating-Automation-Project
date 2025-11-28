from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import logging

from base_page import BasePage
class ProfileInteractionPage(BasePage):

    def __init__(self, driver, logger):
        super().__init__(driver,logger)

        self.LIKE_BTN_LOCATOR = (By.XPATH, '//span[text()="Nope"]')
        self.BACK_TO_TINDER_LOCATOR = ()
        self.like_count = 0

    def hit_like_btn(self):

        try:
            like_btn_element = self.wait.until(
                ec.presence_of_element_located(*self.LIKE_BTN_LOCATOR)
            )

            like_btn_element.click()
            self.like_count += 1

            time.sleep(1)
            self.logging.info(f'Successfully liked on profile {self.like_count}')
            return True

        except NoSuchElementException:
            self.logging.error(f"Couldn't find like button on this page. Not fully loaded in DOM")
            return False

        except ElementClickInterceptedException:
            self.logging.info('A pop up is obstructing the like btn, Attempting to click the  Back to tinder page')
            try:
                bck_to_tinder_btn = self.wait.until(
                    ec.presence_of_element_located(*self.BACK_TO_TINDER_LOCATOR)

                )
                bck_to_tinder_btn.click()
                self.logging.info('Successfully clicked back to tinder page')
                return True

            except NoSuchElementException:
                self.logging.Warning('Back to tinder page btn not the popup interrupting the script')
                return False

            except TimeoutException:
                self.logging.error(f"Couldn't click back to tinder page. Not fully loaded")
                return False


