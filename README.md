# Flask Backend with Anthropic Integration

A Flask backend API that takes string input and sends it to Anthropic's Claude API for processing.

## Features

- RESTful API endpoint for sending messages to Claude
- Error handling for various API scenarios
- CORS enabled for frontend integration
- Health check endpoint
- Environment variable configuration

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

### POST /api/prompt

Send a message to Anthropic's Claude API.

**Request Body:**
```json
{
    "message": "Your string input here"
}
```

**Response:**
```json
{
    "success": true,
    "response": "Claude's response to your message",
    "input_message": "Your original message"
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
curl -X POST http://localhost:5000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you today?"}'
```

### Using Python requests

```python
import requests

response = requests.post(
    'http://localhost:5000/api/prompt',
    json={'message': 'Hello, how are you today?'}
)

if response.status_code == 200:
    data = response.json()
    print(f"Claude's response: {data['response']}")
else:
    print(f"Error: {response.json()['error']}")
```

## Error Handling

The API handles various error scenarios:

- **400 Bad Request**: Missing or invalid message field
- **401 Unauthorized**: Invalid Anthropic API key
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server or API errors

## Dependencies

- Flask: Web framework
- flask-cors: CORS support
- anthropic: Anthropic API client
- python-dotenv: Environment variable management

## Development

The application runs in debug mode by default. For production, set `debug=False` in `app.py`. 
