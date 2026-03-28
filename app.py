import os
import json
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initializing the latest SDK Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use the specific Lite model for your assignment
MODEL_ID = "gemini-3.1-flash-lite-preview"

# Adapted instructions from your project to meet assignment goals
SYSTEM_INSTRUCTION = (
    "You are a friendly, conversational Senior AI Architect. "
    "Speak like a helpful human colleague. "
    "Your goal is to deconstruct user projects into actionable milestones. "
    "Keep answers brief, natural, and conversational. "
    "DO NOT use bulleted lists in your main dialogue. "
    "Format your final technical plan as a structured JSON object. "
    "If information is missing, say: 'Information not found. You can UPDATE me via the /admin panel.'"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.json.get("goal")
    target_store_id = request.json.get("store_id", "default_store") # Use for Knowledge Base if needed
    
    if not user_input:
        return jsonify({"error": "No goal provided"}), 400

    # Structured Output Config
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        # Adding File Search tool logic inspired by your project
        tools=[types.Tool(
            file_search=types.FileSearch(
                file_search_store_names=[target_store_id]
            )
        )],
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
        # Custom error message inspired by your handling
        return jsonify({
            "error": f"SYSTEM ALERT: The AI server is unavailable ({str(e)}). Please try again."
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)