from flask import Flask
from flask_cors import CORS
from flask import request
from chats.gpt.setup import GptSetup
from controllers.gpt import GptController
# from controllers.bard import BardController
# from controllers.bing import BingController
from werkzeug.exceptions import HTTPException

from upload_manager import UploadManager
import time

app = Flask(__name__)
CORS(app)

@app.errorhandler(HTTPException)
def handle_exception(e: HTTPException):
    return e.get_response()

gpt = GptSetup()

gpt.setup_scrapers()

# @app.post('/upload_image')
# def upload_image():
#     image = request.files['image']
#     return UploadManager().add_file(image), 201

# CHAT-GPT

@app.post("/gpt/prompt")
def gpt_prompt():
    return GptController(gpt).prompt(request)

@app.get("/gpt/scrapers")
def gpt_scrapers():
    return GptController(gpt).scrapers(request)

app.run(debug=True, use_reloader=False)