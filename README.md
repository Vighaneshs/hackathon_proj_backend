# Flask Backend with Anthropic Integration

A Flask backend API that accepts PDF files and sends them to Anthropic's Claude API for processing and grading assignments.

## Features

- RESTful API endpoint for uploading PDF files and sending them to Claude
- PDF text extraction and processing
- Error handling for various API scenarios
- CORS enabled for frontend integration
- Health check endpoint
- Environment variable configuration
- File upload validation and security

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory with your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

You can get your API key from the [Anthropic Console](https://console.anthropic.com/).

### 3. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST /api/prompt_initial

Upload a PDF file and send it to Anthropic's Claude API for grading.

**Request Method:** `multipart/form-data`

**Form Fields:**
- `pdf_file`: PDF file to be processed (required)
- `explanation`: Text explaining how to grade the assignment (required)

**Response:**
```json
{
    "success": true,
    "response": "Claude's grading feedback",
    "pdf_filename": "assignment.pdf",
    "explanation": "Grade based on clarity and completeness",
    "pdf_text_length": 1250
}
```

**Error Response:**
```json
{
    "error": "Error description"
}
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "message": "Flask backend is running"
}
```

### GET /

API documentation and usage information.

## Example Usage

### Using curl

```bash
curl -X POST http://localhost:5000/api/prompt_initial \
  -F "pdf_file=@assignment.pdf" \
  -F "explanation=Grade this assignment based on clarity, completeness, and accuracy of the answers. Provide detailed feedback on each section."
```

### Using Python requests

```python
import requests

with open('assignment.pdf', 'rb') as pdf_file:
    files = {'pdf_file': ('assignment.pdf', pdf_file, 'application/pdf')}
    data = {'explanation': 'Grade this assignment based on clarity and completeness.'}
    
    response = requests.post(
        'http://localhost:5000/api/prompt_initial',
        files=files,
        data=data
    )

if response.status_code == 200:
    data = response.json()
    print(f"Claude's response: {data['response']}")
else:
    print(f"Error: {response.json()['error']}")
```

### Using HTML Form

```html
<form action="http://localhost:5000/api/prompt_initial" method="post" enctype="multipart/form-data">
    <input type="file" name="pdf_file" accept=".pdf" required>
    <textarea name="explanation" placeholder="Explain how to grade this assignment" required></textarea>
    <button type="submit">Submit for Grading</button>
</form>
```

## Error Handling

The API handles various error scenarios:

- **400 Bad Request**: Missing PDF file, missing explanation, or invalid file type
- **401 Unauthorized**: Invalid Anthropic API key
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server or API errors

## File Requirements

- **File Type**: Only PDF files are accepted
- **File Size**: Maximum 16MB
- **Content**: PDF must contain extractable text content

## Dependencies

- Flask: Web framework
- flask-cors: CORS support
- anthropic: Anthropic API client
- python-dotenv: Environment variable management
- PyPDF2: PDF text extraction
- reportlab: PDF creation (for testing)

## Testing

Run the test script to verify the API functionality:

```bash
python test_api.py
```

The test script will:
1. Create a sample PDF if one doesn't exist
2. Test the health endpoint
3. Upload the PDF and test the grading functionality

## Development

The application runs in debug mode by default. For production, set `debug=False` in `app.py`. 
