
import os
import glob
from google import genai

# Setup Gemini Client
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# Look for Notebooks or CSVs
target_files = glob.glob("*.ipynb") + glob.glob("*.csv")

if not target_files:
    file_content = "No data files found."
    file_name = "None"
else:
    file_name = target_files[0]
    with open(file_name, 'r', encoding='utf-8') as f:
        file_content = f.read()[:8000] # Grabs the start of your analysis

# The Data Scientist Prompt
prompt = f"Act as a Senior Data Scientist. Audit this file ({file_name}) for logic errors, missing data handling, and visualization improvements:\n\n{file_content}"

try:
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
    )
    audit_text = response.text
except Exception as e:
    audit_text = f"Audit delayed: {str(e)}"

with open("DATA_AUDIT_REPORT.md", "w", encoding='utf-8') as r:
    r.write(f"# 🤖 Automated Data Science Audit\n**Target:** {file_name}\n\n{audit_text}")
