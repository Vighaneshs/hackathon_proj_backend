from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
import base64
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import PyPDF2
import io

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_file):
    """Extract text content from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def encode_pdf_to_base64(pdf_file):
    """Encode PDF file to base64 string"""
    try:
        pdf_file.seek(0)  # Reset file pointer to beginning
        pdf_content = pdf_file.read()
        return base64.b64encode(pdf_content).decode('utf-8')
    except Exception as e:
        raise Exception(f"Error encoding PDF to base64: {str(e)}")

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

@app.route('/api/prompt_initial', methods=['POST'])
def prompt_anthropic():
    """
    API endpoint that takes a PDF file and explanation, sends them to Anthropic's Claude API
    """
    try:
        # Check if PDF file is present in the request
        if 'pdf_file' not in request.files:
            return jsonify({
                'error': 'Missing PDF file in request'
            }), 400
        
        pdf_file = request.files['pdf_file']
        
        # Check if file was selected
        if pdf_file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400
        
        # Check if file type is allowed
        if not allowed_file(pdf_file.filename):
            return jsonify({
                'error': 'Only PDF files are allowed'
            }), 400
        
        # Get explanation from form data
        explanation = request.form.get('explanation', '')
        
        if not explanation:
            return jsonify({
                'error': 'Missing "explanation" field in request'
            }), 400
        
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_file)
        
        if not pdf_text.strip():
            return jsonify({
                'error': 'Could not extract text from PDF or PDF is empty'
            }), 400
        
        # Create the prompt with PDF content and explanation
        prompt = f"""You are a voice assistant. You take an input which is a text explaining how you have to grade the assignment and the assignment content from a PDF.

explanation:
{explanation}

assignment content from PDF:
{pdf_text}

The output should be a formatted structure text in the form of points containing the feedback explaining how you graded that assignment.
Do not give a grade range, give a proper grade."""
        
        # Send to Anthropic Claude with PDF content
        message = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract the response content
        response_content = message.content[0].text
        
        return jsonify({
            'success': True,
            'response': response_content,
            'pdf_filename': secure_filename(pdf_file.filename),
            'explanation': explanation,
            'pdf_text_length': len(pdf_text)
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


@app.route('/api/prompt_redo', methods=['POST'])
def redo_prompt_anthropic():
    """
    API endpoint that takes initial feedback and professor input, sends them to Anthropic's Claude API for re-evaluation
    """
    try:
        # Get initial feedback from form data
        initial_feedback = request.form.get('initial_feedback', '')
        
        if not initial_feedback:
            return jsonify({
                'error': 'Missing "initial_feedback" field in request'
            }), 400

        professor_input = request.form.get('professor_input', '')
        
        if not professor_input:
            return jsonify({
                'error': 'Missing "professor_input" field in request'
            }), 400

        # Create the prompt with initial feedback and professor input
        prompt = f"""You are a voice assistant. You gave points to the assignment and feedback to the student. Modify your initial feedback and points based on the professor's input.
        If professor's input is positive, you should give more points. If professor's input is negative, you should reduce points.

initial feedback and points to the students:
{initial_feedback}

professor's input:
{professor_input}

The output should be a formatted structure text in the form of points containing the feedback explaining how you graded that assignment."""
        
        # Send to Anthropic Claude
        message = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract the response content
        response_content = message.content[0].text
        
        return jsonify({
            'success': True,
            'response': response_content,
            'initial_feedback': initial_feedback,
            'professor_input': professor_input
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
            'POST /api/prompt_initial': 'Send a PDF file and explanation to Anthropic Claude API',
            'GET /api/health': 'Health check endpoint',
            'GET /': 'This documentation'
        },
        'usage': {
            'POST /api/prompt_initial': {
                'method': 'multipart/form-data',
                'fields': {
                    'pdf_file': 'PDF file to be processed',
                    'explanation': 'Text explaining how to grade the assignment'
                },
                'response': {
                    'success': True,
                    'response': 'Claude\'s response',
                    'pdf_filename': 'Name of uploaded PDF',
                    'explanation': 'Original explanation',
                    'pdf_text_length': 'Length of extracted text'
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 