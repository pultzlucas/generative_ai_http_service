from entities.chat_controller import ChatController
from entities.chat_setup import ChatSetup
from chats.bard.tokenizer import BardTokenizer

class BardController(ChatController):
    def __init__(self, chat: ChatSetup) -> None:
        super(BardController, self).__init__(chat, tokenizer=BardTokenizer())