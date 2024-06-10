from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response

class ServiceException(HTTPException):
    code = 0
    http_code = 500
    description = ''

    def get_response(self) -> Response:
        return dict(
            code=self.code,
            error=self.description
        ), self.http_code


class AllScrapersWorkingException(ServiceException):
    code = 1
    http_code = 503
    description = 'Todos os nossos trabalhadores estão ocupados trabalhando, tente novamente mais tarde. ⛏(>.<)'

class AllScrapersBlockedException(ServiceException):
    code = 2
    http_code = 423
    description = 'Todos os nossos trabalhadores estão em repouso, tente novamente mais tarde. (-.-)zZz'

class UnprocessablePromptException(ServiceException):
    code = 3
    http_code = 422
    description = 'Não foi possível processar o prompt. (×_×)'

class ScraperFailureException(ServiceException):
    code = 4
    http_code = 500
    description = 'Desculpe! Houve um problema interno com um dos nossos scrapers. (*~*)'

class InvalidImageFileException(ServiceException):
    code = 5
    http_code = 422
    description = 'Arquivo inválido.'
    def __init__(self, message = None) -> None:
        super().__init__()
        if message:
            self.description = message

class FileNotFoundException(ServiceException):
    code = 6
    http_code = 404
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.description = f'O arquivo "{filename}" não foi encontrado nos uploads.'