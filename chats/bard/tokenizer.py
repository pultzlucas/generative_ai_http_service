from entities.chat_tokenizer import ChatTokenizer
import re
from bs4 import BeautifulSoup

class BardTokenizer(ChatTokenizer):
    def __init__(self) -> None:
        super(BardTokenizer, self).__init__()

    def tokenize(self, text: str) -> list:
        res_text = BeautifulSoup(text, 'html.parser').text
        return len(re.findall(r"\w+|^\w+|[^\w\s]", res_text))