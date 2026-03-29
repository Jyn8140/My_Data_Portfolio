
import os
import glob
import google.generativeai as genai # Switched to the stable library

# 1. Setup Client
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Look for your notebook
target_files = glob.glob("*.ipynb") + glob.glob("*.csv")

if not target_files:
    file_content = "No data files found."
    file_name = "None"
else:
    file_name = target_files[0]
    with open(file_name, 'r', encoding='utf-8') as f:
        # We read the first 10,000 characters to keep it within free limits
        file_content = f.read()[:10000]

# 3. Use the stable Model
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = f"""
Act as a Senior Data Scientist. Audit this file ({file_name}) 
for visual clarity of Seaborn plots and statistical insights.

CONTENT:
{file_content}
"""

try:
    # 4. Generate Content (Stable method)
    response = model.generate_content(prompt)
    audit_text = response.text
except Exception as e:
    audit_text = f"Audit delayed: {str(e)}"

# 5. Save the report
with open("DATA_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
    f.write(f"# 🤖 Automated Data Science Audit\n\nTarget: {file_name}\n\n")
    f.write(audit_text)