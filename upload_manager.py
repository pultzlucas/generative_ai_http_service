from werkzeug.datastructures import FileStorage
import time
from error_handlers import InvalidImageFileException, FileNotFoundException
import os

class UploadManager:
    def __init__(self) -> None:
        self.accepted_mimetypes = ['jpg','jpeg','png','webp']
        self.upload_folder = f"{os.getcwd()}/upload"

    def get_path(self, filename: str):
        return os.path.join(self.upload_folder, filename)
        
    def add_file(self, file: FileStorage):
        filename = str(abs(hash(file.filename + str(time.time())))) 
        extension = file.mimetype.split('/')[1]
        filename += f'.{extension}'

        if not extension in self.accepted_mimetypes:
            raise InvalidImageFileException(f"Arquivo inválido, aceitamos apenas imagens com extensões como: {', '.join(self.accepted_mimetypes)}.")
    
        file.save(f'upload/{filename}')
        return filename
    
    def file_exists(self, filename):
        return os.path.exists(self.get_path(filename))
    
    def remove_file(self, filename: str):
        os.remove(self.get_path(filename))
