from flask import Flask, send_from_directory, redirect, url_for
from flask_cors import CORS
import os

# Set a custom Flask app name
app = Flask('Trinidad & Tobago News')
CORS(app)  # Enable CORS for all routes

# Redirect from / to /articles
@app.route('/')
def redirect_to_articles():
    return redirect(url_for('serve_html'))  # Redirect root to /articles

@app.route('/article_list.json')
def serve_json():
    file_path = 'article_list.json'
    if os.path.exists(file_path):
        return send_from_directory('.', file_path)
    else:
        return "File not found", 404  # Return 404 if the file doesn't exist

@app.route('/articles')
def serve_html():
    file_path = 'article_list.html'
    if os.path.exists(file_path):
        return send_from_directory('.', file_path)  # Serve the HTML file at /articles
    else:
        return "File not found", 404  # Return 404 if the file doesn't exist

if __name__ == '__main__':
    # Running the app with the custom name, now should show Trinidad&Tobago News
    app.run(host='localhost', port=8000)