import os
import glob
from google import genai

# 1. Setup Gemini 3 Flash
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Find any Data Science files (CSV, SQL, or Notebooks)
files = glob.glob("*.csv") + glob.glob("*.sql") + glob.glob("*.ipynb")

if not files:
    content_to_check = "No data files found to audit."
else:
    # Read the first file (max 5000 chars for a quick audit)
    with open(files[0], 'r') as f:
        content_to_check = f.read()[:5000] 

# 3. Ask Gemini 3 Flash for a Senior Review
response = client.models.generate_content(
    model='gemini-3-flash', 
    contents=f"Act as a Senior Data Scientist. Audit this file for bugs, outliers, or SQL logic errors:\n{content_to_check}"
)

# 4. Save the professional report
with open("DATA_AUDIT_REPORT.md", "w") as f:
    f.write("# 🤖 Automated Data Science Audit\n")
    f.write(response.text)
 tips:
{summary_text}
"""

response = model.generate_content(prompt)

# 4. Save the report
with open("DATA_AUDIT_REPORT.md", "w") as f:
    f.write("# 🤖 Automated Data & Code Audit\n")
    f.write(response.text)
print("Report generated successfully!")
