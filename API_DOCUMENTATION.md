# API Documentation

## Overview

This Flask backend provides two main endpoints for AI-powered assignment grading:

1. **`/api/prompt_initial`** - Initial grading of PDF assignments
2. **`/api/prompt_redo`** - Re-evaluation based on professor feedback

## Base URL

```
http://localhost:5000
```

---

## Endpoint 1: Initial Assignment Grading

### `POST /api/prompt_initial`

Uploads a PDF assignment and receives AI-generated grading feedback.

#### Request Format

**Method:** `POST`  
**Content-Type:** `multipart/form-data`

#### Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pdf_file` | File | Yes | PDF file containing the assignment to be graded |
| `explanation` | String | Yes | Instructions for how to grade the assignment |

#### Request Example

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/prompt_initial \
  -F "pdf_file=@assignment.pdf" \
  -F "explanation=Grade this essay based on clarity, coherence, argument strength, and writing quality. Provide detailed feedback on structure, content, and style."
```

**Using Python requests:**
```python
import requests

with open('assignment.pdf', 'rb') as pdf_file:
    files = {'pdf_file': ('assignment.pdf', pdf_file, 'application/pdf')}
    data = {'explanation': 'Grade this essay based on clarity and completeness.'}
    
    response = requests.post(
        'http://localhost:5000/api/prompt_initial',
        files=files,
        data=data
    )

if response.status_code == 200:
    result = response.json()
    print(f"Grade: {result['response']}")
else:
    print(f"Error: {response.json()['error']}")
```

**Using HTML Form:**
```html
<form action="http://localhost:5000/api/prompt_initial" method="post" enctype="multipart/form-data">
    <input type="file" name="pdf_file" accept=".pdf" required>
    <textarea name="explanation" placeholder="Explain how to grade this assignment" required></textarea>
    <button type="submit">Submit for Grading</button>
</form>
```

#### Response Format

**Success Response (200):**
```json
{
    "success": true,
    "response": "Grade: A- (88/100)\n\nFeedback:\n1. Structure: Excellent essay structure with clear introduction, body paragraphs, and conclusion\n2. Content: Demonstrates deep understanding of the topic with thorough analysis\n3. Writing: Clear and engaging writing style with minimal errors\n4. Arguments: Presents compelling arguments with strong logical flow\n5. Evidence: Uses relevant examples and supporting evidence effectively",
    "pdf_filename": "assignment.pdf",
    "explanation": "Grade this essay based on clarity, coherence, argument strength, and writing quality.",
    "pdf_text_length": 1250
}
```

**Error Response (400/401/429/500):**
```json
{
    "error": "Error description"
}
```

#### Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Missing PDF file, missing explanation, or invalid file type |
| 401 | Invalid Anthropic API key |
| 429 | Rate limit exceeded |
| 500 | Server or API error |

---

## Endpoint 2: Re-evaluation with Professor Feedback

### `POST /api/prompt_redo`

Takes initial feedback and professor input to generate revised grading feedback.

#### Request Format

**Method:** `POST`  
**Content-Type:** `application/x-www-form-urlencoded`

#### Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `initial_feedback` | String | Yes | The original AI-generated feedback |
| `professor_input` | String | Yes | Professor's comments or corrections (can be from speech-to-text) |

#### Request Example

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/prompt_redo \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "initial_feedback=Grade: B+ (85/100) Feedback: Good structure but needs more analysis" \
  -d "professor_input=The student shows exceptional critical thinking that wasn't recognized. Please reconsider the grade and provide more detailed feedback on analytical strengths."
```

**Using Python requests:**
```python
import requests

data = {
    'initial_feedback': 'Grade: B+ (85/100)\n\nFeedback:\n1. Structure: Good essay structure\n2. Content: Demonstrates understanding but lacks depth\n3. Writing: Clear writing style',
    'professor_input': 'This student shows exceptional critical thinking skills that weren\'t fully recognized. Please reconsider the grade and provide more detailed feedback on the analytical strengths.'
}

response = requests.post(
    'http://localhost:5000/api/prompt_redo',
    data=data
)

if response.status_code == 200:
    result = response.json()
    print(f"Revised Grade: {result['response']}")
else:
    print(f"Error: {response.json()['error']}")
```

**Using JavaScript (fetch):**
```javascript
const data = new FormData();
data.append('initial_feedback', 'Grade: B+ (85/100) Feedback: Good structure but needs more analysis');
data.append('professor_input', 'The student shows exceptional critical thinking. Please reconsider the grade.');

fetch('http://localhost:5000/api/prompt_redo', {
    method: 'POST',
    body: data
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        console.log('Revised feedback:', result.response);
    } else {
        console.error('Error:', result.error);
    }
});
```

#### Response Format

**Success Response (200):**
```json
{
    "success": true,
    "response": "Grade: A- (88/100)\n\nRevised Feedback:\n1. Structure: Good essay structure with clear organization\n2. Content: Demonstrates exceptional critical thinking and sophisticated analysis\n3. Writing: Clear and engaging writing style\n4. Arguments: Presents compelling arguments with strong analytical depth\n5. Evidence: Uses relevant examples effectively\n\nNote: Upon reconsideration, the student's analytical skills are more sophisticated than initially assessed.",
    "initial_feedback": "Grade: B+ (85/100) Feedback: Good structure but needs more analysis",
    "professor_input": "The student shows exceptional critical thinking. Please reconsider the grade."
}
```

**Error Response (400/401/429/500):**
```json
{
    "error": "Error description"
}
```

#### Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Missing initial_feedback or professor_input |
| 401 | Invalid Anthropic API key |
| 429 | Rate limit exceeded |
| 500 | Server or API error |

---

## Complete Workflow Example

Here's how to use both endpoints in sequence:

### Step 1: Initial Grading

```python
import requests

# Upload and grade assignment
with open('essay.pdf', 'rb') as pdf_file:
    files = {'pdf_file': ('essay.pdf', pdf_file, 'application/pdf')}
    data = {'explanation': 'Grade this essay based on clarity, coherence, and argument strength.'}
    
    response = requests.post(
        'http://localhost:5000/api/prompt_initial',
        files=files,
        data=data
    )

if response.status_code == 200:
    initial_result = response.json()
    initial_feedback = initial_result['response']
    print("Initial Grade:", initial_feedback)
else:
    print("Error in initial grading:", response.json()['error'])
    exit()
```

### Step 2: Professor Review and Re-evaluation

```python
# Professor provides feedback (could be from speech-to-text)
professor_input = "The student's analysis is more sophisticated than initially assessed. The critical thinking skills deserve higher recognition."

# Get revised feedback
data = {
    'initial_feedback': initial_feedback,
    'professor_input': professor_input
}

response = requests.post(
    'http://localhost:5000/api/prompt_redo',
    data=data
)

if response.status_code == 200:
    revised_result = response.json()
    print("Revised Grade:", revised_result['response'])
else:
    print("Error in re-evaluation:", response.json()['error'])
```

---

## File Requirements

### PDF Files
- **Format**: Only PDF files are accepted
- **Size**: Maximum 16MB
- **Content**: Must contain extractable text content
- **Security**: Files are processed in memory and not stored

### Text Input
- **Length**: No strict limits, but very long inputs may hit API token limits
- **Encoding**: UTF-8 recommended
- **Special Characters**: Supported

---

## Rate Limits and Performance

- **File Size**: 16MB maximum per upload
- **Processing Time**: Typically 5-15 seconds depending on PDF size and content
- **Concurrent Requests**: Limited by server resources
- **API Rate Limits**: Subject to Anthropic API limits

---

## Error Handling Best Practices

### Client-Side Validation
```python
import os

def validate_pdf_upload(file_path, explanation):
    # Check file exists
    if not os.path.exists(file_path):
        raise ValueError("File does not exist")
    
    # Check file size (16MB limit)
    if os.path.getsize(file_path) > 16 * 1024 * 1024:
        raise ValueError("File too large (max 16MB)")
    
    # Check file extension
    if not file_path.lower().endswith('.pdf'):
        raise ValueError("Only PDF files are supported")
    
    # Check explanation
    if not explanation or len(explanation.strip()) == 0:
        raise ValueError("Explanation is required")
    
    return True
```

### Error Recovery
```python
import time

def retry_request(request_func, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            response = request_func()
            if response.status_code == 429:  # Rate limit
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
                continue
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay)
    return None
```

---

## Testing

Use the provided test script to verify API functionality:

```bash
python test_api.py
```

The test script will:
1. Create a sample essay PDF
2. Test the initial grading endpoint
3. Test the redo endpoint with the initial feedback
4. Test the redo endpoint with sample data

---

## Security Considerations

- **API Keys**: Store your Anthropic API key securely in environment variables
- **File Uploads**: Only PDF files are accepted and processed
- **Data Privacy**: Files are processed in memory and not stored on disk
- **CORS**: Configured for frontend integration

---

## Support

For issues or questions:
1. Check the error messages in the API responses
2. Verify your Anthropic API key is valid
3. Ensure PDF files contain extractable text
4. Check server logs for detailed error information 