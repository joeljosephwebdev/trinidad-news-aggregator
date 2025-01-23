from flask import Flask, send_from_directory, redirect, url_for
from flask_cors import CORS
import os

app = Flask('Trinidad & Tobago News')
CORS(app)

# Redirect from / to /news
@app.route('/')
def redirect_to_articles():
    return redirect(url_for('serve_html'))  # Redirect root to /news

@app.route('/article_list.json')
def serve_json():
    file_path = 'article_list.json'
    if os.path.exists(file_path):
        return send_from_directory('.', file_path)
    else:
        return "File not found", 404  # Return 404 if the file doesn't exist

@app.route('/news')
def serve_html():
    file_path = 'static/index.html'
    if os.path.exists(file_path):
        return send_from_directory('.', file_path)  # Serve the HTML file at /articles
    else:
        return "File not found", 404  # Return 404 if the file doesn't exist

if __name__ == '__main__':
        port = int(os.environ.get('PORT', 8000))
        app.run(host='0.0.0.0', port=port)