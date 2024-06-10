from entities.chat_controller import ChatController
from entities.chat_setup import ChatSetup
from chats.gpt.tokenizer import GptTokenizer

class GptController(ChatController):
    def __init__(self, chat: ChatSetup) -> None:
        super(GptController, self).__init__(chat, tokenizer=GptTokenizer())