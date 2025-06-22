import requests
import json

def test_api():
    """
    Test script to demonstrate the Flask API usage
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
    
    # Test prompt endpoint
    print("Testing prompt endpoint...")
    test_message = "Hello! Can you tell me a short joke?"
    
    try:
        response = requests.post(
            f"{base_url}/api/prompt",
            json={"message": test_message},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            print(f"Input message: {data['input_message']}")
            print(f"Claude's response: {data['response']}")
        else:
            print(f"Error: {response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

if __name__ == "__main__":
    test_api() 