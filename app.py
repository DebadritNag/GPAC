import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API using environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return "AI Agent Running", 200


@app.route("/summarize", methods=["POST"])
def summarize():
    """
    Accepts a JSON body with a 'text' field and returns a summary.
    Example request body: { "text": "Long text here..." }
    """
    data = request.get_json()

    # Validate that request body exists and contains 'text'
    if not data or "text" not in data or not data["text"].strip():
        return jsonify({"error": "Missing or empty 'text' field in request body."}), 400

    input_text = data["text"]

    try:
        # Build the prompt for summarization
        prompt = f"Summarize the following text in 2-3 sentences:\n\n{input_text}"

        # Call the Gemini model
        response = model.generate_content(prompt)

        # Return the summary as JSON
        return jsonify({"summary": response.text}), 200

    except Exception as e:
        # Return a generic error message if something goes wrong
        return jsonify({"error": f"Failed to generate summary: {str(e)}"}), 500


if __name__ == "__main__":
    # Use PORT env var if set (required by Cloud Run), default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
