from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# DO NOT add a route for '/' here. 
# Vercel will handle '/' by serving index.html via the vercel.json above.

@app.route('/api/clean', methods=['POST'])
def clean_site():
    try:
        data = request.json
        url = data.get("url")
        if not url:
            return jsonify({"error": "No URL provided"}), 400
            
        if not url.startswith("http"):
            url = "https://" + url

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove Canva branding
        for selector in ['._1Q9m1w', '[aria-label="Canva"]', '.canva-watermark', 'footer']:
            for el in soup.select(selector):
                el.decompose()

        # Fix assets
        base_tag = soup.new_tag('base', href=url)
        if soup.head:
            soup.head.insert(0, base_tag)

        return jsonify({"html": soup.prettify()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
