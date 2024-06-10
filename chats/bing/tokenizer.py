from entities.chat_tokenizer import ChatTokenizer
import tiktoken

class BingTokenizer(ChatTokenizer):
    def __init__(self) -> None:
        super(BingTokenizer, self).__init__()

    def tokenize(self, text: str) -> list:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))