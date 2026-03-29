import os
import glob
import google.generativeai as genai
import nbformat

# 1. Setup API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Find the Analysis File
target_files = glob.glob("*.ipynb")
if not target_files:
    print("No notebook found.")
    exit(1)

file_name = target_files[0]

# 3. Read the content
with open(file_name, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)
    code_content = ""
    for cell in nb.cells:
        if cell.cell_type == 'code':
            code_content += cell.source + "\n\n"

# 4. Talk to Gemini 1.5-Flash (The Stable Model)
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = f"Audit this vehicle analysis for visualization clarity and price logic:\n\n{code_content[:15000]}"

try:
    response = model.generate_content(prompt)
    audit_text = response.text
except Exception as e:
    audit_text = f"Audit failed: {str(e)}"

# 5. Save the report
with open("DATA_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
    f.write(f"# 🤖 Automated Data Science Audit\n\nTarget: {file_name}\n\n")
    f.write(audit_text)