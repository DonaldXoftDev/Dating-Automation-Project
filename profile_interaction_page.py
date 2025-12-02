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

        self.LIKE_BTN_LOCATOR = (By.XPATH, '//button//span[text()="Nope"]')
        self.BACK_TO_TINDER_LOCATOR = ()
        self.like_count = 0

    def hit_like_btn(self):

        try:
            like_btn_element = self.wait.until(
                ec.element_to_be_clickable(self.LIKE_BTN_LOCATOR)
            )

            like_btn_element.click()
            self.like_count += 1

            time.sleep(1)
            self.logger.info(f'Successfully liked on profile {self.like_count}')
            return True

        except NoSuchElementException:
            self.logger.error(f"Couldn't find like button on this page. Not fully loaded in DOM")
            return False

        except ElementClickInterceptedException:
            self.logger.info('A pop up is obstructing the like btn, Attempting to click the  Back to tinder page')
            try:
                bck_to_tinder_btn = self.wait.until(
                    ec.element_to_be_clickable(self.BACK_TO_TINDER_LOCATOR)

                )
                bck_to_tinder_btn.click()
                self.logger.info('Successfully clicked back to tinder page')
                return True

            except NoSuchElementException:
                self.logger.Warning('Back to tinder page btn not the popup interrupting the script')
                return False

            except TimeoutException:
                self.logger.error(f"Couldn't click back to tinder page. Not fully loaded")
                return False


