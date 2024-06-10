import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from error_handlers import UnprocessablePromptException, FileNotFoundException
import os
from upload_manager import UploadManager

class ScraperBlockedException(Exception):
    pass

class ChatScraper():
    def __init__(self, username: str, driver: uc.Chrome):
        self.username = username
        self.driver = driver
        self.processing = False
        self.blocked = False
        self.blocked_start_time = float(0)
        self.unblock_attempt_time = 2 * 60 # seconds
        self.upload = UploadManager()

    def log_info(self, message):
        print(f'[{self.__class__.__name__}] ({self.username}) {message}')

    def refresh(self):
        self.driver.refresh()

    def available(self):
        if int(time.time() - self.blocked_start_time) >= self.unblock_attempt_time:
            self.unblock()
        return not self.processing and not self.blocked
    
    def block(self):
        self.processing = False
        self.blocked = True
        self.blocked_start_time = time.time()

    def unblock(self):
        self.blocked = False
        self.blocked_start_time = float(0)

    def run_single_prompt(self, prompt: dict):
        self.log_info('Sending prompt...')
        prompt_text = prompt['prompt']
        self.write_prompt(prompt_text)
        
        self.log_info('Waiting process start...')
        start = time.time()
        wait_time = 10
        while True:
            if self.is_processing():
                break
            self.log_info(f'Waiting, {time.time() - start:.2f}s/{wait_time}s')
            if int(time.time() - start) >= wait_time:
                return self.run_single_prompt(prompt_text)
            time.sleep(0.1)

        self.log_info('Processing prompt...')

        while True:
            if self.is_blocked():
                self.block()
                self.log_info('Blocked')
                if not self.is_processable():
                    self.log_info('Cannot process prompt')
                    raise UnprocessablePromptException()
                raise ScraperBlockedException()

            if not self.is_processing() and not self.is_blocked():
                self.log_info('Getting prompt response')
                return self.get_prompt_result()

    def run(self, prompts: list[dict]):
        for p in filter(lambda p: 'image' in p, prompts):
            if not self.upload.file_exists(p['image']):
                raise FileNotFoundException(p['image'])

        self.processing = True
        self.responses = list()

        if self.is_blocked():
            self.log_info('Refreshing page...')
            self.refresh()
        else:
            self.log_info('Openning new chat...')
            while True:
                time.sleep(0.1)
                try:
                    self.open_new_chat()
                    break
                except Exception as e:
                    self.log_info('Error when openning new chat: ' + str(e))
                    break

        responses = list(map(self.run_single_prompt, prompts))

        self.processing = False
        return responses

    def upload_image(self, filename: str):
        pass

    def write_prompt(self, prompt: str):
        pass

    def get_prompt_result(self) -> str:
        pass

    def open_new_chat(self):
        pass

    def is_processing(self) -> bool:
        return True

    def is_blocked(self) -> bool:
        return False

    def is_processable(self)-> bool:
        return True