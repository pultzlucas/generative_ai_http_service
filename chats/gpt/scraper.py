import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from entities.chat_scraper import ChatScraper
from selenium.common.exceptions import TimeoutException, JavascriptException
from error_handlers import ScraperFailureException
import time

class GptScraper(ChatScraper):
    def __init__(self, username: str, driver: uc.Chrome):
        super(GptScraper, self).__init__(username, driver)
        self.tries = 0
        self.text_input_selector = 'textarea#prompt-textarea'
        self.send_button_selector = 'button[data-testid="send-button"]'

    def write_prompt(self, prompt: str):
        prompt = prompt.replace('`', '')

        try:
            WebDriverWait(self.driver, 10)\
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, self.send_button_selector)))
        except TimeoutException:
            self.tries += 1
            if self.tries >= 5:
                raise ScraperFailureException()
            self.refresh()
            self.write_prompt(prompt)
            return

        try:
            self.driver.execute_script(f"""
                const input = document.querySelector('{self.text_input_selector}')
                input.value = `{prompt}`
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                setTimeout(() => {{
                    document.querySelector('{self.send_button_selector}').click()
                }}, 200)
            """)
        except JavascriptException:
            raise ScraperFailureException()

    def get_prompt_result(self):
        all_responses = self.driver.find_elements(By.CSS_SELECTOR, '.markdown.prose.w-full')
        try:
            return all_responses[-1].get_attribute('innerHTML')
        except:
            return None

    def open_new_chat(self):
        self.driver.refresh()
        # self.driver.find_element(By.CSS_SELECTOR, ".text-ellipsis.text-sm.text-token-text-primary").click()
        # try:
        #     self.driver.execute_script("document.querySelectorAll('div[role=\"dialog\"] button')[1].click()")
        # except:
        #     pass
        # self.driver.find_element(By.CSS_SELECTOR, self.send_button_selector)

    def is_processing(self):
        selector = 'svg[stroke="currentColor"]'
        is_processing = self.driver.execute_script(f"return document.body.contains(document.querySelector('{selector}'))")
        selector = '.icon-xl.text-token-text-primary'
        is_writing = self.driver.execute_script(f"return document.body.contains(document.querySelector('{selector}'))")
        return is_processing or is_writing

    def is_blocked(self):
        return self.driver.execute_script("return document.body.contains(document.querySelector('.border-red-500'))")
    
    def is_processable(self):
        return True
        # block_href = self.driver.execute_script("return document.querySelector('.py-2.px-3.border.text-gray-600').querySelector('a') ? document.querySelector('.py-2.px-3.border.text-gray-600').querySelector('a').href : null")
        # return not (block_href and 'usage-policies' in block_href)
                


