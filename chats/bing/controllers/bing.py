from entities.chat_controller import ChatController
from entities.chat_setup import ChatSetup
from chats.bing.tokenizer import BingTokenizer

class BingController(ChatController):
    def __init__(self, chat: ChatSetup) -> None:
        super(BingController, self).__init__(chat, tokenizer=BingTokenizer())