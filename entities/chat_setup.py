import json
from entities.chat_scraper import ChatScraper
import os
import undetected_chromedriver as uc
import threading
# import chromedriver_autoinstaller
# chromedriver_autoinstaller.install()

class ChatSetup():
    def __init__(self, chat_url, accounts_file_path, setup_account: threading.Thread):
        self.scrapers = list[ChatScraper]()
        self.chat_url = chat_url
        self.accounts_path = accounts_file_path
        self.accounts = list()
        self.setup_account = setup_account
    
    def load_accounts(self):
        try:
            with open(self.accounts_path) as accounts:
                self.accounts = json.loads(accounts.read())
        except:
            self.log_info('Error: Unable to find accounts file.')
            exit(1)

    def setup_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
        self.driver = uc.Chrome(options=options, headless=False, driver_executable_path=r'/home/lucaspultz/Desktop/repositories/Generative AI Service/service/chromedriver')
        self.driver.get(self.chat_url)
        self.driver.implicitly_wait(20)

    def setup_scrapers(self):
        self.load_accounts()

        threads = list[threading.Thread]()
        for account in self.accounts: 
            self.setup_driver()
            t = self.setup_account(account, self.driver, self) 
            t.start() 
            threads.append(t)

        for t in threads: 
            t.join()

    def log_info(self, msg):
        print(f'[{self.__class__.__name__}] {msg}')