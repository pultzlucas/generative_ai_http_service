from selenium.webdriver.common.by import By
import os
import base64
from chats.bard.scraper import BardScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from entities.chat_setup import ChatSetup
import threading 
import undetected_chromedriver as uc
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import ctypes

VK_ESCAPE = 0x1B

class BardAccountSetup(threading.Thread):
    def __init__(self, account, driver: uc.Chrome, setup: ChatSetup): 
        threading.Thread.__init__(self) 
        self.account = account
        self.driver = driver
        self.setup = setup
        
    def run(self): 
        if 'https://www.google.com/sorry' in self.driver.current_url:
            wait = WebDriverWait(self.driver, 100000)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.mat-mdc-input-element')))

        self.current_scraper_name = self.account['username']
        self.login(self.account['username'], self.account['password'], self.account['auth_method'])
        self.setup.scrapers.append(BardScraper(self.account['username'], self.driver))

    def login(self, username, password, auth_method):
        self.setup.log_info(f'({self.current_scraper_name}) Logging in using {auth_method} auth.')
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Fazer login"]').click()
            self.driver.implicitly_wait(20)

            if auth_method == 'google':
                self.driver.find_element(
                    By.XPATH, '//input[@class="whsOnd zHQkBf"]').send_keys(username)
                self.driver.find_element(
                    By.XPATH, '//div[@id="identifierNext"]').click()
                self.driver.find_element(
                    By.XPATH, '//input[@autocomplete="current-password"]').send_keys(password)
                self.driver.find_element(
                    By.XPATH, '//div[@id="passwordNext"]').click()
               
            (WebDriverWait(self.driver, 1000)
             .until(EC.presence_of_element_located((By.CSS_SELECTOR, '#upload-local-image-button'))).click())
            
            time.sleep(1)

            pyautogui.press('esc')
            
        except:
            self.setup.log_info(f'({self.current_scraper_name}) Error: Error when logging in.')
            exit(1)

class BardSetup(ChatSetup):
    def __init__(self):
        super(BardSetup, self).__init__(
            chat_url='https://bard.google.com/chat?hl=pt', 
            accounts_file_path=os.path.join(os.path.dirname(__file__), 'bard.accounts.json'), 
            setup_account=BardAccountSetup
        )