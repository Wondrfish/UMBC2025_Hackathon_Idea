from flask import Flask, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)


@app.route("/")
def home():
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Say hello from Gemini!")
    return response.text


if __name__ == "__main__":
    app.run(debug=True)
