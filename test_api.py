import requests
import json
import os

def test_api():
    """
    Test script to demonstrate the Flask API usage with PDF upload and redo functionality
    """
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running.\n")
        return
    
    # Test prompt_initial endpoint with PDF
    print("Testing prompt_initial endpoint with PDF...")
    
    # Check if essay PDF exists
    test_pdf_path = "essay.pdf"
    if not os.path.exists(test_pdf_path):
        print(f"Warning: Essay PDF file '{test_pdf_path}' not found.")
        print("Creating a simple test essay PDF or you can provide your own essay.pdf file.")
        print("For testing, you can create a simple PDF with some essay content.\n")
        return
    
    explanation = "Grade this essay based on clarity, coherence, argument strength, and writing quality. Provide detailed feedback on structure, content, and style."
    
    try:
        with open(test_pdf_path, 'rb') as pdf_file:
            files = {'pdf_file': (test_pdf_path, pdf_file, 'application/pdf')}
            data = {'explanation': explanation}
            
            response = requests.post(
                f"{base_url}/api/prompt_initial",
                files=files,
                data=data
            )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            print(f"PDF filename: {data['pdf_filename']}")
            print(f"Explanation: {data['explanation']}")
            print(f"PDF text length: {data['pdf_text_length']} characters")
            print(f"Claude's initial response: {data['response']}")
            
            # Store the initial feedback for redo testing
            initial_feedback = data['response']
            
            # Test prompt_redo endpoint
            print("\n" + "="*50)
            print("Testing prompt_redo endpoint...")
            test_prompt_redo(base_url, initial_feedback)
            
        else:
            print(f"Error: {response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except FileNotFoundError:
        print(f"File not found: {test_pdf_path}")

def test_prompt_redo(base_url, initial_feedback):
    """
    Test the prompt_redo endpoint with initial feedback and professor input
    """
    # Sample professor input (could be from speech-to-text)
    professor_input = "The student deserves higher marks for creativity and original thinking. The essay shows good analytical skills but needs more specific examples. Please adjust the grade accordingly."
    
    try:
        data = {
            'initial_feedback': initial_feedback,
            'professor_input': professor_input
        }
        
        response = requests.post(
            f"{base_url}/api/prompt_redo",
            data=data
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            print(f"Professor input: {data['professor_input']}")
            print(f"Claude's revised response: {data['response']}")
        else:
            print(f"Error: {response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

def test_prompt_redo_standalone():
    """
    Test the prompt_redo endpoint with sample data (without needing initial API call)
    """
    base_url = "http://localhost:5000"
    
    print("Testing prompt_redo endpoint with sample data...")
    
    # Sample initial feedback
    sample_initial_feedback = """Grade: B+ (85/100)

Feedback:
1. Structure: Good essay structure with clear introduction, body paragraphs, and conclusion
2. Content: Demonstrates understanding of the topic but lacks depth in analysis
3. Writing: Clear writing style with minor grammatical errors
4. Arguments: Presents reasonable arguments but could be more compelling
5. Evidence: Uses some examples but needs more specific supporting evidence"""

    # Sample professor input
    sample_professor_input = "This student shows exceptional critical thinking skills that weren't fully recognized in the initial assessment. The analysis is actually quite sophisticated. Please reconsider the grade and provide more detailed feedback on the analytical strengths."

    try:
        data = {
            'initial_feedback': sample_initial_feedback,
            'professor_input': sample_professor_input
        }
        
        response = requests.post(
            f"{base_url}/api/prompt_redo",
            data=data
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            print(f"Professor input: {data['professor_input']}")
            print(f"Claude's revised response: {data['response']}")
        else:
            print(f"Error: {response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

def create_test_essay_pdf():
    """
    Create a simple test essay PDF for demonstration purposes
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = "essay.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Add title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "Sample Essay: The Impact of Technology on Education")
        
        # Add content
        c.setFont("Helvetica", 12)
        content = [
            "Introduction:",
            "Technology has revolutionized the way we approach education in the 21st century.",
            "From online learning platforms to interactive digital tools, the integration of",
            "technology in educational settings has created both opportunities and challenges.",
            "",
            "Body Paragraph 1:",
            "One of the most significant benefits of technology in education is the",
            "accessibility it provides. Students can now access educational resources from",
            "anywhere in the world, breaking down geographical barriers and creating",
            "opportunities for lifelong learning. Online courses, digital libraries, and",
            "educational apps have made learning more flexible and personalized.",
            "",
            "Body Paragraph 2:",
            "However, the rapid adoption of technology also presents challenges.",
            "Digital divide issues persist, with some students lacking access to",
            "necessary devices and internet connectivity. Additionally, concerns about",
            "screen time and the potential for distraction in digital learning",
            "environments require careful consideration and balanced approaches.",
            "",
            "Conclusion:",
            "While technology offers tremendous potential to enhance education, its",
            "implementation must be thoughtful and inclusive. Educators and policymakers",
            "must work together to ensure that technological advances benefit all",
            "students and contribute to meaningful learning outcomes."
        ]
        
        y_position = height - 150
        for line in content:
            c.drawString(100, y_position, line)
            y_position -= 20
        
        c.save()
        print(f"Created test essay PDF: {filename}")
        return filename
        
    except ImportError:
        print("reportlab not available. Please install it with: pip install reportlab")
        return None
    except Exception as e:
        print(f"Error creating test essay PDF: {e}")
        return None

if __name__ == "__main__":
    # Try to create a test essay PDF if it doesn't exist
    if not os.path.exists("essay.pdf"):
        print("Creating test essay PDF...")
        create_test_essay_pdf()
    
    # Test the full workflow (initial + redo)
    test_api()
    
    # Also test redo endpoint with sample data
    print("\n" + "="*50)
    test_prompt_redo_standalone() 