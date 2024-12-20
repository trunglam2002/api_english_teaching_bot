import google.generativeai as genai

genai.configure(api_key="AIzaSyDKwVQ7sjeljgqHbFPgnUKUWV5jxdHPfqs")
model = genai.GenerativeModel("gemini-1.5-flash")