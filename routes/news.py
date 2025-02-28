from flask import Blueprint, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

news_bp = Blueprint('news', __name__, url_prefix='/apps/news')

# Base URL for the News API
NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")
NYTIMES_API_URL = "https://api.nytimes.com/svc/topstories/v2"

# Mapping of our categories to API categories
CATEGORY_MAPPING = {
    'business': 'business',
    'technology': 'technology',
    'world': 'world',
    'automobile': 'automobiles', 
    'sports': 'sports',
}

@news_bp.route('/')
def news_page():
    """Render the news page"""
    return render_template('news.html')

@news_bp.route('/fetch', methods=['GET'])
def fetch_news():
    """Fetch news from the News API"""
    try:
        # Get category from request, default to business
        category = request.args.get('category', 'business')
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
        articles = data.get('results', [])[:10]  # Limit to 10 articles

        transformed_data = {
            'success': True,
            'category': category,
            'data': []
        }

        # Process articles securely
        for article in articles:
            summary = article.get('abstract', 'No summary available')
            url = article.get('url', "https://www.nytimes.com")

            # Get first available image
            image_url = "https://via.placeholder.com/150"
            multimedia = article.get('multimedia', [])
            if multimedia and isinstance(multimedia, list):
                for media in multimedia:
                    if media.get('url'):
                        image_url = media['url']
                        break  # Use first available image

            transformed_data['data'].append({
                'title': article.get('title', 'No Title'),
                'content': summary,
                'date': article.get('published_date', ''),
                'readMoreUrl': url,
                'imageUrl': image_url
            })
            
        return jsonify(transformed_data)
    except requests.RequestException:
        return jsonify({'success': False, 'error': 'Error fetching news'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
