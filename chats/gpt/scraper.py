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
        self.send_button_selector = 'button.mb-1'

    def write_prompt(self, prompt: str):
        prompt = prompt.replace('`', '')

        try:
            self.driver.execute_script(f"""
                const input = document.querySelector('{self.text_input_selector}')
                input.value = `{prompt}`
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                setTimeout(() => {{
                    document.querySelector('{self.send_button_selector}').click()
                }}, 300)
            """)
        except JavascriptException:
            raise ScraperFailureException()

    def get_prompt_result(self):
        all_responses = self.driver.find_elements(By.CSS_SELECTOR, '.markdown.prose.w-full.break-words')
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
        selector = 'button[data-testid="fruitjuice-stop-button"'
        is_processing = self.driver.execute_script(f"return document.body.contains(document.querySelector('{selector}'))")
        return is_processing

    def is_blocked(self):
        return self.driver.execute_script("return document.body.contains(document.querySelector('.text-token-text-error'))")
    
    def is_processable(self):
        return True
                


