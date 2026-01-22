import google.generativeai as genai
import os, json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

async def process_text_with_llm(text):
    prompt = f"""
Extract marksheet information and return STRICT JSON.

Fields:
- name
- father_name
- roll_no
- subject_wise_marks
- overall_result

Each field must contain:
- value
- confidence (0–1)

TEXT:
{text}
"""

    response = model.generate_content(prompt)
    output = response.text.strip()

    try:
        return json.loads(output)
    except:
        return {"raw_output": output}
