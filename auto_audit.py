
import os
import glob
from google import genai

# 1. Setup Gemini 3 Flash Client
# Make sure your GitHub Secret is named GEMINI_API_KEY
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Find files to audit (Notebooks, SQL, or CSVs)
files = glob.glob("*.ipynb") + glob.glob("*.sql") + glob.glob("*.csv")

if not files:
    content_to_check = "No specific data science files found in the root directory."
    file_name = "None"
else:
    file_name = files[0]
    with open(file_name, 'r', encoding='utf-8') as f:
        # Read the first 5000 characters to stay within free limits
        content_to_check = f.read()[:5000] 

# 3. Request a Senior Data Scientist Review
prompt = f"""
Act as a Senior Data Scientist and Code Auditor. 
Review the following content from the file '{file_name}'.
Check for:
1. Logic errors or bugs.
2. Data quality issues (outliers, missing values).
3. Suggestions for better visualization or SQL optimization.

Content:
{content_to_check}
"""

try:
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
    )
    report_text = response.text
except Exception as e:
    report_text = f"Error generating report: {str(e)}"

# 4. Save the results to a Markdown file
with open("DATA_AUDIT_REPORT.md", "w", encoding='utf-8') as f:
    f.write(f"# 🤖 Automated Data Science Audit\n")
    f.write(f"**Target File:** {file_name}\n\n")
    f.write(report_text)

print(f"Successfully audited {file_name}")
