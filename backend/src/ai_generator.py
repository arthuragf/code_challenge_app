import os
import json
from google import genai
from typing import Dict, Any
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    """
    Generates a challenge using AI based on the specified difficulty.
    
    Args:
        difficulty (str): The difficulty level of the challenge.
        
    Returns:
        Dict[str, Any]: A dictionary containing the generated challenge details.
    """
    system_prompt = """
You are a generator of multiple-choice coding questions.

Generate ONE multiple-choice coding question (not a coding task).

⚠️ DO NOT create a coding problem with input/output format, examples, or constraints.
⚠️ DO NOT include descriptions, problem statements, or any code to be written by the user.
✅ You must create a question with 4 plausible answer options, only one of which is correct.

The topic must match the specified difficulty level:
- Easy: focus on basic syntax, simple operations, or fundamental programming concepts.
- Medium: involve data structures, algorithms, or intermediate features.
- Hard: cover advanced topics like optimization, design patterns, or complex logic.

Output ONLY a valid JSON object with the following structure:

{
  "title": "The question text to be shown to the user",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct_answer_id": 2,
  "explanation": "A clear explanation of why the correct answer is right and the others are wrong"
}

🔒 Strict rules:
- You MUST return only the JSON object, nothing else.
- You MUST include exactly 4 options.
- You MUST include correct_answer_id as an integer from 0 to 3.
- You MUST include the explanation.
"""

    
    try:
        # Call the AI model to generate a challenge
        gemini_response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                temperature=0.7,  # Adjust the creativity level
                response_mime_type="application/json"
            ),
            contents=f"""
Create one multiple-choice coding question of {difficulty.lower()} difficulty.

Return only a JSON object with:
- "title": the question
- "options": a list of 4 plausible answers
- "correct_answer_id": index (0-3) of the correct answer
- "explanation": detailed reason why the answer is correct

Do not create input/output problems. Only return a single valid JSON object.
"""
        )
        
        # Parse the response
        challenge_data = json.loads(gemini_response.text)
        
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")
        
        return challenge_data
    
    except Exception as e:
        print(e)
        return {
            "title": "Wich is the correct method to add an element to a list in Python?",
            "options": [
                "my_list.append(5)",
                "my_list.add(5)",
                "my_list.push(5)"
                "my_list.insert(5)"
            ],
            "correct_answer_id": 0,
            "explanation": "The correct method to add an element to a list in Python is 'append'. The other methods do not exist for lists."
        }