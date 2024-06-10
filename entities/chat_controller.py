from flask import Request
from entities.chat_setup import ChatSetup
from entities.chat_tokenizer import ChatTokenizer
from error_handlers import AllScrapersBlockedException
from entities.chat_scraper import ScraperBlockedException

class ChatController():
    def __init__(self, chat: ChatSetup, tokenizer: ChatTokenizer) -> None:
        self.chat = chat
        self.tokenizer = tokenizer

    def prompt(self, request: Request):
        req: dict = request.get_json()

        prompts = req.get('prompts')

        while True:
            for scraper in self.chat.scrapers:    
                if scraper.available():
                    try:
                        responses = scraper.run(prompts)
                    except ScraperBlockedException: 
                        break

                    return dict(
                        meta=dict(req.items()).get('meta', None),
                        prompts=list(map(lambda p: dict(content=p, tokens=self.tokenizer.tokenize(p['prompt']) if self.tokenizer else None), prompts)),
                        responses=list(map(lambda r: dict(content=r, tokens=self.tokenizer.tokenize(r) if self.tokenizer else None), responses))
                    ), 200    
                
            if len(list(filter(lambda s: not s.blocked, self.chat.scrapers))) == 0:
                raise AllScrapersBlockedException()
            
    
    def scrapers(self, request: Request):
        scrapers_state = list()
        for s in self.chat.scrapers:
            s.available()
            scrapers_state.append(dict(username=s.username, processing=s.processing, blocked=s.blocked))
        return scrapers_state