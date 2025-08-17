import logging
from flask import Blueprint, request, jsonify, current_app
from paraphrase_service import ParaphraseService
from rate_limiter import RateLimiter
import time

api_bp = Blueprint('api', __name__)
paraphrase_service = ParaphraseService()
rate_limiter = RateLimiter()

logger = logging.getLogger(__name__)

@api_bp.route('/paraphrase', methods=['POST'])
def paraphrase():
    """
    Paraphrase text endpoint
    
    Expected JSON payload:
    {
        "text": "Text to paraphrase",
        "max_length": 100 (optional),
        "temperature": 0.7 (optional)
    }
    """
    try:
        # Get client IP for rate limiting
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        # Check rate limit
        if not rate_limiter.is_allowed(client_ip):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.',
                'retry_after': 60
            }), 429
        
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'The "text" field is required'
            }), 400
        
        text = data['text'].strip()
        
        # Validate text input
        if not text:
            return jsonify({
                'error': 'Empty text',
                'message': 'Text cannot be empty'
            }), 400
        
        if len(text) > 1000:
            return jsonify({
                'error': 'Text too long',
                'message': 'Text must be less than 1000 characters'
            }), 400
        
        # Optional parameters
        max_length = data.get('max_length', 100)
        temperature = data.get('temperature', 0.7)
        
        # Validate optional parameters
        if not isinstance(max_length, int) or max_length < 10 or max_length > 200:
            max_length = 100
        
        if not isinstance(temperature, (int, float)) or temperature < 0.1 or temperature > 2.0:
            temperature = 0.7
        
        start_time = time.time()
        
        # Perform paraphrasing
        try:
            paraphrased_text = paraphrase_service.paraphrase(
                text=text,
                max_length=max_length,
                temperature=temperature
            )
        except Exception as e:
            logger.error(f"Paraphrasing failed: {str(e)}")
            return jsonify({
                'error': 'Paraphrasing failed',
                'message': 'Unable to process the text. Please try again.'
            }), 500
        
        processing_time = round(time.time() - start_time, 3)
        
        # Record successful request for rate limiting
        rate_limiter.record_request(client_ip)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'paraphrased_text': paraphrased_text,
            'processing_time_seconds': processing_time,
            'parameters': {
                'max_length': max_length,
                'temperature': temperature
            }
        })
    
    except Exception as e:
        logger.error(f"Unexpected error in paraphrase endpoint: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

@api_bp.route('/paraphrase', methods=['GET'])
def paraphrase_info():
    """Get information about the paraphrase endpoint"""
    return jsonify({
        'endpoint': '/api/paraphrase',
        'method': 'POST',
        'description': 'Paraphrase text using AI models',
        'required_fields': ['text'],
        'optional_fields': ['max_length', 'temperature'],
        'limits': {
            'max_text_length': 1000,
            'max_length_range': [10, 200],
            'temperature_range': [0.1, 2.0],
            'rate_limit': '60 requests per minute'
        },
        'example': {
            'request': {
                'text': 'The quick brown fox jumps over the lazy dog.',
                'max_length': 50,
                'temperature': 0.7
            }
        }
    })

@api_bp.route('/status', methods=['GET'])
def api_status():
    """Get API status and model information"""
    model_status = paraphrase_service.get_model_status()
    return jsonify({
        'api_status': 'active',
        'model_loaded': model_status['loaded'],
        'model_name': model_status['model_name'],
        'supported_operations': ['paraphrase'],
        'rate_limits': {
            'requests_per_minute': 60
        }
    })
