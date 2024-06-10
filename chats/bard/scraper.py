import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from entities.chat_scraper import ChatScraper
import os
import time

class BardScraper(ChatScraper):
    def __init__(self, username: str, driver: uc.Chrome):
        super(BardScraper, self).__init__(username, driver)

    def upload_image(self, filename: str):
        file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(self.upload.get_path(filename))

    def write_prompt(self, prompt: dict):
        prompt_text = prompt.get('text').replace('`', '')
        filename = prompt.get('image')

        if 'image' in prompt:
            self.upload_image(filename)

        self.driver.execute_script(f"""
            const input = document.querySelector('.textarea > p')
            input.textContent = `{prompt_text}`
        """)

        self.log_info('Waiting image upload...')
        while True:
            send_button = self.driver.find_element(By.CSS_SELECTOR, 'button.send-button')
            if send_button.get_attribute('aria-disabled') == 'false':
                self.upload.remove_file(filename)
                send_button.click()
                break
            time.sleep(0.1)

    def get_prompt_result(self):
        all_responses = self.driver.find_elements(By.CSS_SELECTOR, 'response-container')
        try:
            return all_responses[len(all_responses) - 1].get_attribute('innerHTML')
        except:
            return None

    def open_new_chat(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, 'button.new-conversation')
        if btn.get_attribute('disabled') != 'true':
            btn.click()
            WebDriverWait(self.driver, 500).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.mat-mdc-input-element'))
                and 
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.send-button'))
            )

    def is_processing(self):
        return self.driver.execute_script("""
            const logos = Array.from(document.querySelectorAll('.logo'))
            const lastLogo = logos[logos.length - 1]
            return String(lastLogo.src).includes('sparkle_thinking')
        """)

    def is_blocked(self):
        return self.driver.execute_script("return document.body.contains(document.querySelector('div.mat-mdc-snack-bar-label'))")

