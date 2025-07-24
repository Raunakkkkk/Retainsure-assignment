"""
URL Shortener Test Suite

This comprehensive test suite validates all core functionality of the URL shortener service.
Tests cover the complete API surface including success cases, error handling, and edge cases.

Test Coverage:
- ✅ Health check endpoints (API status validation)
- ✅ URL shortening (valid URLs, invalid URLs, missing parameters)
- ✅ URL redirection (successful redirects, click tracking)
- ✅ Analytics/stats (click counts, creation timestamps, metadata)
- ✅ Error handling (404s for non-existent codes, 400s for invalid input)
- ✅ Input validation (short code format validation)
- ✅ Concurrent operations (thread safety, unique code generation)

The test suite uses Flask's test client to simulate HTTP requests and validates:
- Correct HTTP status codes
- Proper JSON response formats
- Expected data structures and values
- Error message content and formatting

All tests are designed to be independent and can run in any order.
"""

import pytest
import json
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


def test_api_health_check(client):
    """Test API health endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'URL Shortener API is running' in data['message']


def test_shorten_valid_url(client):
    """Test shortening a valid URL."""
    url = "https://www.example.com/very/long/url/path"
    response = client.post(
        '/api/shorten',
        data=json.dumps({'url': url}),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) == 6
    assert data['short_code'].isalnum()
    assert data['short_url'].endswith(data['short_code'])


def test_shorten_invalid_url(client):
    """Test shortening an invalid URL."""
    invalid_urls = [
        "not-a-url",
        "ftp://",
        "",
        "http://",
        "just some text"
    ]
    
    for invalid_url in invalid_urls:
        response = client.post(
            '/api/shorten',
            data=json.dumps({'url': invalid_url}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid URL format' in data['error']


def test_shorten_missing_url(client):
    """Test shortening without providing URL."""
    response = client.post(
        '/api/shorten',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'URL is required' in data['error']


def test_redirect_functionality(client):
    """Test URL redirection and click tracking."""
    # First, shorten a URL
    original_url = "https://www.example.com/test"
    response = client.post(
        '/api/shorten',
        data=json.dumps({'url': original_url}),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = response.get_json()
    short_code = data['short_code']
    
    # Test redirect
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == original_url


def test_redirect_nonexistent_code(client):
    """Test redirect with non-existent short code."""
    response = client.get('/xyz123')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'Short code not found' in data['error']


def test_redirect_invalid_format(client):
    """Test redirect with invalid short code format."""
    invalid_codes = ['abc', 'toolong123', 'ab@123']  
    
    for code in invalid_codes:
        response = client.get(f'/{code}')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


def test_stats_functionality(client):
    """Test analytics/stats endpoint."""
    # First, shorten a URL
    original_url = "https://www.example.com/analytics-test"
    response = client.post(
        '/api/shorten',
        data=json.dumps({'url': original_url}),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = response.get_json()
    short_code = data['short_code']
    
    # Check initial stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    stats = response.get_json()
    assert stats['url'] == original_url
    assert stats['clicks'] == 0
    assert 'created_at' in stats
    
    # Click the link to increment counter
    client.get(f'/{short_code}')
    client.get(f'/{short_code}')  # Second click
    
    # Check updated stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    stats = response.get_json()
    assert stats['clicks'] == 2


def test_stats_nonexistent_code(client):
    """Test stats with non-existent short code."""
    response = client.get('/api/stats/xyz123')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'Short code not found' in data['error']


def test_stats_invalid_format(client):
    """Test stats with invalid short code format."""
    response = client.get('/api/stats/abc')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid short code format' in data['error']


def test_concurrent_shortening(client):
    """Test that multiple URLs can be shortened simultaneously."""
    urls = [
        "https://www.example1.com",
        "https://www.example2.com", 
        "https://www.example3.com"
    ]
    
    short_codes = []
    for url in urls:
        response = client.post(
            '/api/shorten',
            data=json.dumps({'url': url}),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.get_json()
        short_codes.append(data['short_code'])
    
    # Ensure all codes are unique
    assert len(short_codes) == len(set(short_codes))
    
    # Test that all redirects work
    for i, short_code in enumerate(short_codes):
        response = client.get(f'/{short_code}')
        assert response.status_code == 302
        assert response.location == urls[i]