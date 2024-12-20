import google.generativeai as genai

API_KEY = "AIzaSyDKwVQ7sjeljgqHbFPgnUKUWV5jxdHPfqs"

def configure_api():
    genai.configure(api_key=API_KEY)

def get_model(model_name="gemini-1.5-flash"):
    return genai.GenerativeModel(model_name=model_name)