import os
import glob
import google.generativeai as genai
import nbformat

# 1. Setup API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Find the Notebook
target_files = glob.glob("*.ipynb")
if not target_files:
    print("No notebook found.")
    exit(1)

file_name = target_files[0]

# 3. Read the Notebook (Only Code Cells)
with open(file_name, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)
    code_content = ""
    for cell in nb.cells:
        if cell.cell_type == 'code':
            code_content += cell.source + "\n\n"

# 4. THE FIX: Using the full model path
# Adding 'models/' tells the library exactly which path to take.
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

prompt = f"""
Act as a Senior Data Scientist. 
Audit this vehicle analysis for visualization clarity and price logic.
Focus on Seaborn plot effectiveness.

CODE CONTENT:
{code_content[:15000]}
"""

try:
    print(f"Communicating with Stable API for {file_name}...")
    response = model.generate_content(prompt)
    audit_text = response.text
    print("Audit successful!")
except Exception as e:
    # If it fails, we want to know EXACTLY why
    audit_text = f"Audit failed. Technical Error: {str(e)}"
    print(f"Error: {e}")

# 5. Save the report
with open("DATA_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
    f.write(f"# 🤖 Automated Data Science Audit\n\nTarget: {file_name}\n\n")
    f.write(audit_text)