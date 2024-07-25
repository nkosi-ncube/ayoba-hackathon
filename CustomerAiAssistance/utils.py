import logging
import os
import vertexai
from vertexai.generative_models import GenerativeModel  # Replace with the actual import path
from gatewayapi.models import Customer

def generate_normal_response(user_prompt):
    logging.basicConfig(level=logging.DEBUG)
    root_project_folder = os.path.dirname(__file__)
    
    # Path to your Google Cloud credentials file
    key_file_path = "application_default_credentials.json"
    key_path = os.path.join(root_project_folder, key_file_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    project_id = "strong-kit-422108-p4"

    logging.debug("Initializing Vertex AI")
    
    try:
        # Initialize Vertex AI and Generative Model
        vertexai.init(project=project_id, location="us-central1")
        model = GenerativeModel(model_name="gemini-1.5-pro")
        logging.debug("Model initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing model: {e}")
        return "Error initializing AI model."

    # Create the prompt
    prompt = f"""
    You are a professional assistant for an Ayoba business chat. Your role is to assist clients with their queries related to our services. 
    Keep responses concise, professional, and relevant to the business context. Avoid unnecessary greetings and be straightforward.
    Ensure responses are clear and informative, and include any relevant links or resources where applicable.

    User Query: {user_prompt}

    Provide a useful response that addresses the user's query effectively. If the query is complex, break it down into simpler parts and guide the user accordingly.
    """

    contents = [prompt]
    logging.debug("Contents prepared")

    print("Please wait while I generate a response ...")

    try:
        # Generate the response from the model
        response = model.generate_content(contents)
        logging.debug("Response generated successfully")
        return response.text
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "Sorry, there was an error processing your request."
