import os
import glob
import google.generativeai as genai

# 1. Setup API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Find files to audit (CSV or SQL)
files_to_audit = glob.glob("*.csv") + glob.glob("*.sql")

if not files_to_audit:
    summary_text = "No data or SQL files found to audit."
else:
    # Read the first file found (or loop through all)
    with open(files_to_audit[0], 'r') as f:
        content = f.read()[:2000] # Send first 2000 chars to stay in limits
    summary_text = f"Content from {files_to_audit[0]}:\n{content}"

# 3. Ask Gemini for an expert review
prompt = f"""
Act as a Senior Data Scientist. Review this file content for 'bugs', 
logic errors, or optimization tips:
{summary_text}
"""

response = model.generate_content(prompt)

# 4. Save the report
with open("DATA_AUDIT_REPORT.md", "w") as f:
    f.write("# 🤖 Automated Data & Code Audit\n")
    f.write(response.text)
print("Report generated successfully!")
