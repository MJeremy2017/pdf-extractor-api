from flask import Flask, request, flash, redirect
from werkzeug.utils import secure_filename
import fitz
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

UPLOAD_DIRECTORY = "./data"
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_pdf_text(filepath):
    doc = fitz.open(filepath)
    p = []
    for page in doc:
        s = page.getText("text")
        p.append(s)
    return p


def remove_file(filepath):
    os.remove(filepath)
    app.logger.info('removed file {}'.format(filepath))


@app.route('/', methods=['GET'])
def home():
    return 'This is PDF extractor app'


@app.route('/extract_text', methods=['POST'])
def extract_text():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info('load file {}'.format(filename))
            filepath = os.path.join(UPLOAD_DIRECTORY, filename)
            file.save(filepath)
            app.logger.info('file saved to {}'.format(filepath))

            result = get_pdf_text(filepath)
            remove_file(filepath)
            return {
                'text': result
            }


if __name__ == "__main__":
    app.run()