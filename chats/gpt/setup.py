from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chats.gpt.scraper import GptScraper
import os
from entities.chat_setup import ChatSetup
import threading

class GptAccountSetup(threading.Thread):
    def __init__(self, account, driver: uc.Chrome, setup: ChatSetup): 
        threading.Thread.__init__(self) 
        self.account = account
        self.driver = driver
        self.setup = setup
        
    def run(self): 
        self.current_scraper_name = self.account['username']
        # self.login(self.account['username'], self.account['password'], self.account['auth_method'])
        scraper = GptScraper(self.account['username'], self.driver)
        # scraper.remove_popups()
        # self.setup.log_info(f'({self.current_scraper_name}) Popups removed.')
        self.setup.scrapers.append(scraper)

    def login(self, username, password, auth_method):
        self.setup.log_info(f'({self.current_scraper_name}) Logging in using {auth_method} auth.')
        self.driver.find_element(By.XPATH, '//button[@class="social-btn"]').click()
        self.driver.implicitly_wait(20)

        if auth_method == 'gpt':
            self.driver.find_element(
                By.XPATH, '//input[@name="username"]').send_keys(username)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            self.driver.find_element(
                By.XPATH, '//input[@name="password"]').send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, '._button-login-password').click()

        if auth_method == 'google':
            self.driver.find_element(
                By.XPATH, '//button[@data-provider="google"]').click()
            self.driver.find_element(
                By.XPATH, '//input[@class="whsOnd zHQkBf"]').send_keys(username)
            self.driver.find_element(
                By.XPATH, '//div[@id="identifierNext"]').click()
            self.driver.find_element(
                By.XPATH, '//input[@autocomplete="current-password"]').send_keys(password)
            self.driver.find_element(
                By.XPATH, '//div[@id="passwordNext"]').click()

class GptSetup(ChatSetup):
    def __init__(self):
        super(GptSetup, self).__init__(
            chat_url='https://chat.openai.com/', 
            accounts_file_path=os.path.join(os.path.dirname(__file__), 'gpt.accounts.json'), 
            setup_account=GptAccountSetup
        )