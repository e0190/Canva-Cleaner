# api/index.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# DELETE OR COMMENT OUT THE HOME ROUTE:
# @app.route('/')
# def home():
#     return "API is running..."

@app.route('/api/clean', methods=['POST'])
def clean_site():
    # ... (keep the rest of the cleaning logic here)
    data = request.json
    url = data.get("url")
    if not url: return jsonify({"error": "URL required"}), 400
    
    # [Rest of your cleaning code from before]
    return jsonify({"html": "cleaned_html_here"})
