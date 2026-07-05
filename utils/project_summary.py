from utils.gemini import generate_answer

def summarize_project(code_files):
    context = ""

    for file in code_files[:15]:
        context += f"\nFILE: {file['path']}\n"
        context += file["content"][:2000]
        context += "\n\n"

    prompt = """
Analyze this software project and provide:

1. Project Purpose
2. Programming Languages
3. Frameworks
4. Architecture
5. Database
6. Authentication
7. Main Features

Keep it concise.
"""

    return generate_answer(prompt, context)