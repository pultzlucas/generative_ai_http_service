from entities.chat_controller import ChatController
from entities.chat_setup import ChatSetup
from chats.gpt.tokenizer import GptTokenizer
from chats.gpt.setup import GptSetup


class GptController(ChatController):
    def __init__(self, chat: ChatSetup) -> None:
        super().__init__(chat, GptTokenizer())