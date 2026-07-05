import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


model = genai.GenerativeModel("gemini-2.5-flash")


SYSTEM_PROMPT = """
You are AI Codebase Assistant.

You are given relevant pieces of a software project.

Your job is to answer ONLY from the provided context.

Rules:

- Never invent code.
- If the answer is not present, say:
  "I couldn't find that information in the uploaded codebase."

- Explain code in simple language.
- Mention filenames when possible.
- Keep answers concise and developer-friendly.
"""


def generate_answer(question, context):

    prompt = f"""
{SYSTEM_PROMPT}

================ CODEBASE CONTEXT ================

{context}

================ USER QUESTION ===================

{question}

==================================================
"""

    response = model.generate_content(prompt)

    return response.text