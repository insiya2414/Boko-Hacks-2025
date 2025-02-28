from flask import Blueprint, render_template, jsonify, request
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

news_bp = Blueprint('news', __name__, url_prefix='/apps/news')

# Base URL for the News API
NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")
NYTIMES_API_URL = "https://api.nytimes.com/svc/topstories/v2"

# Mapping of our categories to API categories
CATEGORY_MAPPING = {
    'business': 'business',
    'technology': 'technology',
    'world': 'world',
}

INTERNAL_NEWS = [
    {
        "title": "CONFIDENTIAL: Security Update",
        "description": "Internal security review document. Restricted access.",
        "url": "#internal-only",
        "publishedAt": "2025-01-15T08:30:00Z",
        "imageUrl": ""
    },
    {
        "title": "CONFIDENTIAL: Product Launch Details",
        "description": "Upcoming product specifications for internal review only.",
        "url": "#internal-only",
        "publishedAt": "2025-02-01T10:15:00Z",
        "imageUrl": ""
    }
]

@news_bp.route('/')
def news_page():
    """Render the news page"""
    return render_template('news.html')

@news_bp.route('/fetch', methods=['GET'])
def fetch_news():
    """Fetch news from the News API with a vulnerability"""
    try:
        # Get category from request, default to business
        category = request.args.get('category', 'general')
        if category not in CATEGORY_MAPPING:
            return jsonify({'success': False, 'error': 'Invalid category'}), 400
        
        api_category = CATEGORY_MAPPING[category]

        if not NYTIMES_API_KEY:
            return jsonify({'success': False, 'error': 'API key missing'}), 500
        
        api_url = f"{NYTIMES_API_URL}/{api_category}.json?api-key={NYTIMES_API_KEY}"

        response = requests.get(api_url, timeout=10)

        if response.status_code != 200:
            return jsonify({'success': False, 'error': 'Failed to fetch news'}), response.status_code
        
        data = response.json()
        articles = data.get('results', [])[:10]
   
        filter_param = request.args.get('filter', '{}')
            
        try:
            filter_options = json.loads(filter_param)
        except json.JSONDecodeError:
            return jsonify({'success': False, 'error': 'Invalid filter parameter'}), 400
        
        auth_token = request.headers.get("Authorization")
        if filter_options.get('showInternal') is True and auth_token == f"Bearer {INTERNAL_SECRET}":
            articles = INTERNAL_NEWS + articles

        # Transform the data to match expected format
        transformed_data = {
            'success': True,
            'category': category,
            'data': []
        }

        # Process articles securely
        for article in articles:
            
            summary = article.get('abstract', 'No summary available')
            url = article.get('url', "https://www.nytimes.com")

            multimedia = article.get('multimedia', [])
            image_url = "https://via.placeholder.com/150"  # Default placeholder

            if multimedia and isinstance(multimedia, list):  # Check if multimedia exists
                for media in multimedia:
                    if media.get('url'):  # Find first valid image URL
                        image_url = media['url']
                        break  # Stop after finding the first valid image

            transformed_data['data'].append({
                'title': article.get('title', 'No Title'),
                'summary': summary,
                'date': article.get('published_date', ''),
                'url': url,
                'imageUrl': image_url  # FIXED: Ensures the image URL is always valid
            })
            
        return jsonify(transformed_data)
    except requests.RequestException as e:
        return jsonify({'success': False, 'error': 'Error fetching news'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500