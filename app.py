from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

@app.route('/api/prompt', methods=['POST'])
def prompt_anthropic():
    """
    API endpoint that takes a string input and sends it to Anthropic's Claude API
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing "message" field in request body'
            }), 400
        
        user_message = data['message']
        
        if not user_message or not isinstance(user_message, str):
            return jsonify({
                'error': 'Message must be a non-empty string'
            }), 400
        
        # Send message to Anthropic Claude
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        
        # Extract the response content
        response_content = message.content[0].text
        
        return jsonify({
            'success': True,
            'response': response_content,
            'input_message': user_message
        })
        
    except anthropic.AuthenticationError:
        return jsonify({
            'error': 'Authentication failed. Please check your Anthropic API key.'
        }), 401
        
    except anthropic.RateLimitError:
        return jsonify({
            'error': 'Rate limit exceeded. Please try again later.'
        }), 429
        
    except anthropic.APIError as e:
        return jsonify({
            'error': f'Anthropic API error: {str(e)}'
        }), 500
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Flask backend is running'
    })

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API documentation
    """
    return jsonify({
        'message': 'Flask Backend with Anthropic Integration',
        'endpoints': {
            'POST /api/prompt': 'Send a message to Anthropic Claude API',
            'GET /api/health': 'Health check endpoint',
            'GET /': 'This documentation'
        },
        'usage': {
            'POST /api/prompt': {
                'body': {
                    'message': 'Your string input here'
                },
                'response': {
                    'success': True,
                    'response': 'Claude\'s response',
                    'input_message': 'Your original message'
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 