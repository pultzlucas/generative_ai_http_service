import undetected_chromedriver as uc
from entities.chat_scraper import ChatScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os

class BingScraper(ChatScraper):
    def __init__(self, username: str, driver: uc.Chrome):
        super(BingScraper, self).__init__(username, driver)

    def write_prompt(self, prompt: dict):
        prompt_text = prompt.get('text').replace('`', '')

        self.driver.execute_script(f"""
            const input = document.querySelector("#b_sydConvCont > cib-serp").shadowRoot.querySelector("#cib-action-bar-main").shadowRoot.querySelector("div > div.main-container > div > div.input-row > cib-text-input").shadowRoot.querySelector("#searchbox")
            input.value = `{prompt_text}`
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            setTimeout(() => {{
                document.querySelector("#b_sydConvCont > cib-serp").shadowRoot.querySelector("#cib-action-bar-main").shadowRoot.querySelector("div > div.main-container > div > div.bottom-controls > div.bottom-right-controls > div.control.submit > cib-icon-button").shadowRoot.querySelector("button").click()
            }}, 500)
        """)

    def remove_popups(self):
        WebDriverWait(self.driver, 10000).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#bnp_btn_accept')))
        self.driver.find_element(By.CSS_SELECTOR, '#bnp_btn_accept').click()

    def get_prompt_result(self): 
        response = self.driver.execute_script("""return Array.from(document.querySelector("#b_sydConvCont > cib-serp")
                                              .shadowRoot.querySelector("#cib-conversation-main")
                                              .shadowRoot.querySelectorAll("#cib-chat-main > cib-chat-turn")).slice(-1)[0]
                                              .shadowRoot.querySelector("cib-message-group.response-message-group")
                                              .shadowRoot.querySelector("cib-message")
                                              .shadowRoot.querySelector("cib-shared > div > div > div")""")
        return response.get_attribute('innerHTML').strip()

    def open_new_chat(self):
        self.driver.execute_script('document.querySelector("#b_sydConvCont > cib-serp").shadowRoot.querySelector("#cib-action-bar-main").shadowRoot.querySelector("div > div.outside-left-container > div > button").click()')

    def is_processing(self):
        return self.driver.execute_script("""return !document.querySelector("#b_sydConvCont > cib-serp").shadowRoot.querySelector("#cib-action-bar-main").shadowRoot.querySelector("div > cib-typing-indicator").shadowRoot.querySelector("#stop-responding-button").disabled""")

    def is_blocked(self):
        return self.driver.execute_script("""return document.body.contains(document.querySelector("#b_sydConvCont > cib-serp").shadowRoot.querySelector("#cib-conversation-main").shadowRoot.querySelector("#cib-chat-main > cib-notification-container").shadowRoot.querySelector("div > div > cib-notification"))""")

