import os
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

IGNORE_DIRS=[".git",".venv","venv","__pycache__",".pyc","node_modules","dist","build",".idea",
             ".vscode","package-lock.json","poetry.lock"]

IGNORE_EXTENSIONS =[".png", ".jpg", ".ico", ".mp4", ".gif", ".zip", ".tar", ".exe", ".pdf",".env"]

VALID_EXTENSIONS= [".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c", ".rb", ".php", ".md", ".html", ".css", ".json", ".yml", ".yaml", ".sh", ".bat", ".json", ".yaml", ".yml", ".toml", ".env.example", "requirements.txt", "package.json"]


def check_codebase(root_dir="."):
    code_content={}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:]=[d for d in dirnames if d not in IGNORE_DIRS]

        for file in filenames:
            if os.path.splitext(file)[1] in IGNORE_EXTENSIONS:
                continue

            _, ext = os.path.splitext(file)
            if ext in VALID_EXTENSIONS or file == "requirements.txt" or file == "package.json":
                file_path = os.path.join(dirpath, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code_content[file_path] = f.read()
                except UnicodeDecodeError:
                    continue

    return code_content


code_content= check_codebase()

SYSTEM_PROMPT= f"""
You are an expert software engineer and elite technical writer. You can analyze any codebase, understand its architecture, features, and dependencies, and generate comprehensive, professional documentation.

Your task is to analyze the provided code files and generate a complete, well-formatted `README.md` file in Markdown. 

Your output must be strictly the Markdown content (no conversational filler, no extra text outside the markdown block). 

Include the following sections based on the codebase:

### Core & Mandatory Sections
- **Project Title & Badges:** A clear, professional project title, brief description, and relevant badges (build, license, version).
- **Description:** A concise explanation of what the project does, the problem it solves, and why it exists.
- **Table of Contents:** An outline for quick navigation.
- **Tech Stack / Built With:** The languages, frameworks, libraries, and tools used in the repository.
- **Prerequisites & Installation:** Step-by-step installation commands and environment setup instructions.
- **Run Locally / Usage:** Clear code snippets, instructions, or commands showing how to run and use the project.
- **License:** Statement of user and modification rights (e.g., MIT).
- **Authors & Acknowledgements:** Credit to creators, contributors, and inspirations.

### Include These Custom Sections Where Applicable
*(Analyze the code to determine which of these apply and fill them out if relevant)*
- **API Reference:** Endpoints, methods, and parameters if it's a backend/API service.
- **Environment Variables:** Required `.env` keys and configuration parameters.
- **Features:** Key highlights and capabilities of the code.
- **Roadmap:** Future plans, upcoming features, or scaling goals based on project state.
- **Contributing:** Guidelines for how other developers can contribute, report bugs, or submit PRs.
- **Screenshots / Demo:** Visual placeholders or descriptions of output.
- **Support / FAQ:** Troubleshooting or contact details.

Ensure the formatting uses clean Markdown syntax, code blocks for commands, and professional technical terminology throughout.
"""


def code_to_api(code_content):

    formatted_code = ""
    for file_path, content in code_content.items():
        formatted_code += f"\n\n--- FILE: {file_path} ---\n{content}"

    USER_PROMPT = f"""
    You are provided with the following code files from a project:
    {formatted_code}
    
    Analyze them to understand the architecture, features, and dependencies. 
    Generate a complete, professional `README.md` in Markdown format that includes all the sections outlined in the system prompt.
    """

    print("Sending codebase to Groq LLM to generate README...")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",  
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        temperature=0.3,)

    
    readme_content = response.choices[0].message.content

   
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("Success! README.md has been generated and saved.")



if __name__ == "__main__":
    
    print(f"Found {len(code_content)} code files in the codebase.\n")
    code_to_api(code_content)