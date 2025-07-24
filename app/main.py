from flask import Flask, jsonify, request, redirect as flask_redirect
from app.models import URLStore
from app.utils import generate_short_code, is_valid_url, validate_short_code

app = Flask(__name__)
url_store = URLStore()


@app.route('/')
def health_check():
    """Basic health check endpoint - returns service status."""
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })


@app.route('/api/health')
def api_health():
    """API health check endpoint - confirms the service is running."""
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Shorten a long URL and return a 6-character short code."""
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url']
        
        # Validate URL
        if not is_valid_url(original_url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Generate unique short code
        existing_codes = set(url_store.urls.keys())
        short_code = generate_short_code(existing_codes=existing_codes)
        
        # Save the mapping
        url_store.save_url(short_code, original_url)
        
        # Return response
        return jsonify({
            'short_code': short_code,
            'short_url': f'{request.host_url}{short_code}'
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect to the original URL using the short code and track clicks."""
    # Validate short code format
    if not validate_short_code(short_code):
        return jsonify({'error': 'Invalid short code format'}), 404
    
    # Get URL data
    url_data = url_store.get_url(short_code)
    if not url_data:
        return jsonify({'error': 'Short code not found'}), 404
    
    # Increment click count
    url_store.increment_clicks(short_code)
    
    # Redirect to original URL
    return flask_redirect(url_data['url'], code=302)


@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Get analytics data for a short code (clicks, creation time, original URL)."""
    # Validate short code format
    if not validate_short_code(short_code):
        return jsonify({'error': 'Invalid short code format'}), 404
    
    # Get URL data
    url_data = url_store.get_url(short_code)
    if not url_data:
        return jsonify({'error': 'Short code not found'}), 404
    
    # Return analytics
    return jsonify({
        'url': url_data['url'],
        'clicks': url_data['clicks'],
        'created_at': url_data['created_at']
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)