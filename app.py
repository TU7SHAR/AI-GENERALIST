import os
import json
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initializing the SDK Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Your chosen model
MODEL_ID = "gemini-3.1-flash-lite-preview"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.json.get("goal")
    
    if not user_input:
        return jsonify({"error": "No goal provided"}), 400

    # Clean, simple config. No File Search tools. Just JSON formatting.
    config = types.GenerateContentConfig(
        system_instruction="You are a Technical Architect. Break down the user's project into technical steps.",
        response_mime_type="application/json",
        response_schema={
            "type": "OBJECT",
            "properties": {
                "project_name": {"type": "STRING"},
                "difficulty_level": {"type": "STRING"},
                "steps": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "milestone": {"type": "STRING"},
                            "tech_stack": {"type": "STRING"},
                            "description": {"type": "STRING"}
                        }
                    }
                }
            },
            "required": ["project_name", "difficulty_level", "steps"]
        }
    )

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_input,
            config=config
        )
        
        return jsonify(json.loads(response.text))
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)