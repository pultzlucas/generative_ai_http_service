from selenium.webdriver.common.by import By
import os
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from entities.chat_setup import ChatSetup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from chats.bing.scraper import BingScraper
import threading
import undetected_chromedriver as uc

class BingAccountSetup(threading.Thread):
    def __init__(self, account, driver: uc.Chrome, setup: ChatSetup): 
        threading.Thread.__init__(self) 
        self.account = account
        self.driver = driver
        self.setup = setup
        
    def run(self): 
        self.current_scraper_name = self.account['username']
        self.login(self.account['username'], self.account['password'], self.account['auth_method'])
        scraper = BingScraper(self.account['username'], self.driver)
        scraper.remove_popups()
        self.setup.log_info(f'({self.current_scraper_name}) Popups removed.')
        self.setup.scrapers.append(scraper)

    def login(self, username, password, auth_method):
        self.setup.log_info(f'({self.current_scraper_name}) Logging in using {auth_method} auth.')
        
        WebDriverWait(self.driver, 100000).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#b_sydConvCont > cib-serp')))
        self.driver.find_element(By.CSS_SELECTOR, 'input#id_a').click()
        self.driver.implicitly_wait(20)

        self.driver.find_element(By.CSS_SELECTOR, '#i0116').send_keys(username)
        self.driver.find_element(By.CSS_SELECTOR, '#idSIButton9').click()
        WebDriverWait(self.driver, 10000).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#i0118')))
        self.driver.find_element(By.CSS_SELECTOR, '#i0118').send_keys(password)

        while True:
            try:
                WebDriverWait(self.driver, 10000).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.win-button.button_primary')))
                self.driver.find_element(By.CSS_SELECTOR, 'input.win-button.button_primary').click()
                break
            except StaleElementReferenceException:
                continue

        self.driver.find_element(By.CSS_SELECTOR, '#idBtn_Back').click()

class BingSetup(ChatSetup):
    def __init__(self):
        super(BingSetup, self).__init__(
            chat_url='https://www.bing.com/search?q=Bing+AI&showconv=1', 
            accounts_file_path=os.path.join(os.path.dirname(__file__), 'bing.accounts.json'), 
            setup_account=BingAccountSetup
        )