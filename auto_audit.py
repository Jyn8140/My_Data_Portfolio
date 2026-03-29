

import os
import glob
from google import genai

# 1. FIX: Changed to match your GitHub Secret name
api_key = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=api_key)

# Look for Notebooks or CSVs
target_files = glob.glob("*.ipynb") + glob.glob("*.csv")

if not target_files:
    file_content = "No data files found."
    file_name = "None"
else:
    file_name = target_files[0]
    # 2. IMPROVEMENT: We read the file to actually send it to the AI
    with open(file_name, 'r', encoding='utf-8') as f:
        file_content = f.read()[:15000] # Read more text for a better audit

# 3. FIX: Actually put the {file_content} inside the prompt so the AI can see it
prompt = f"""
Act as a Senior Data Scientist. I have added Seaborn visualizations to my Vehicle Analysis. 
Audit this file ({file_name}) for visual clarity of Seaborn plots and statistical insights from the price distribution.

FILE CONTENT TO AUDIT:
{file_content}
"""

try:
    # 4. FIX: Changed model to gemini-1.5-flash to bypass the 'Limit 0' error
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )
    audit_text = response.text
except Exception as e:
    audit_text = f"Audit delayed: {str(e)}"

# Save the report
with open("DATA_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
    f.write(f"# 🤖 Automated Data Science Audit\n\nTarget: {file_name}\n\n")
    f.write(audit_text)