import os
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

client = genai.GenerativeModel('models/gemini-2.5-flash')