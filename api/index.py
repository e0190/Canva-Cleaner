# api/index.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/clean', methods=['POST'])
def clean_site():
    data = request.json
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Target Canva-specific branding
        watermark_selectors = [
            '._1Q9m1w', 
            '[aria-label="Canva"]',
            '.canva-watermark',
            'footer'
        ]

        for selector in watermark_selectors:
            for el in soup.select(selector):
                el.decompose()

        # Inject a base tag so images/scripts still load from Canva's servers
        base_tag = soup.new_tag('base', href=url)
        soup.head.insert(0, base_tag)

        return jsonify({"html": soup.prettify()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Vercel
app.debug = True
