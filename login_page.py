import os
from selenium.common import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import logging

from base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.current_web_title = self.driver.title.lower()

        #credentials

        self.fb_login_title = 'Facebook'
        self.tinder_title = 'Tinder | Match. Chat. Date.'

        #locators

        self.FB_LOGIN_BTN_LOCATOR = (By.NAME, 'login')
        self.EMAIL_LOCATOR = (By.ID, 'email')
        self.PASSWORD_LOCATOR = (By.ID, 'pass')
        self.TEXT_ON_FB_PAGE = (By.ID, "homelink")
        self.CONTINUE_TO_FB_LOCATOR = (By.XPATH, '//span[text()="Continue as Itz IK"]')


    def click_fb_login_btn(self):
        try:
            fb_login_btn = self.wait.until(
                ec.presence_of_element_located(self.FB_LOGIN_BTN_LOCATOR)
            )
            fb_login_btn.click()
            self.logger.info("FB login button clicked")
            return True

        except TimeoutException:
            self.logger.info('Failed to click the facebook login button. Script timed out')
            return False

    def enter_user_name(self, username):
        try:
            email_element = self.driver.find_element(*self.EMAIL_LOCATOR)
            email_element.send_keys(username)
            self.logger.info('Entering email')
            return True
        except NoSuchElementException:
            self.logger.warning('Email element not found ')
            return False


    def enter_password(self,password):
        try:
            password_element = self.driver.find_element(*self.PASSWORD_LOCATOR)
            password_element.send_keys(password)
            self.logger.info('Entering password')
            return True

        except NoSuchElementException:
            self.logger.warning('Password element not found ')
            return False


    def click_continue_to_fb(self):
        try:
            continue_btn = self.wait.until(
                ec.presence_of_element_located(self.CONTINUE_TO_FB_LOCATOR)
            )
            continue_btn.click()
            self.logger.info('Successfully clicked Continue button')
            return True

        except TimeoutException:
            self.logger.info('Failed to click Continue button')
            return False

