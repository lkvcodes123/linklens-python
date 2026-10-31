"""Run with: python3 app.py"""
from pathlib import Path
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from analyzer import analyze

app = Flask(__name__, static_folder=str(Path(__file__).parent / 'static'), static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024


@app.get('/')
def index():
    return app.send_static_file('index.html')


@app.post('/api/check')
def check():
    if not request.is_json:
        return jsonify(error='Send a JSON object with a url field.'), 415
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            raise ValueError('Send a JSON object with a url field.')
        return jsonify(analyze(data.get('url')))
    except (ValueError, BadRequest) as error:
        message = str(error) if isinstance(error, ValueError) else 'Invalid JSON.'
        return jsonify(error=message), 400


@app.errorhandler(RequestEntityTooLarge)
def too_large(error):
    return jsonify(error='Request is too large.'), 413


@app.after_request
def headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if request.path == '/api/check':
        response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
