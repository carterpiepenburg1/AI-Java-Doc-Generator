"""
Code-base documentation generator
COMPSCI 422 - Final Project
Group 2 - Carter Piepenburg, Austin VanDenPlas
"""

import requests
import json
import pathlib

OLLAMA_API = "http://localhost:11434/api/generate"
#MODEL_NAME = "qwen2.5-coder:1.5b"
#MODEL_NAME = "smollm2"
MODEL_NAME = "llama3.2:1b"

def generateDocumentation(prompt, model=MODEL_NAME, max_tokens=250):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "max_tokens": max_tokens
    }

    response = requests.post(OLLAMA_API, json=data)
    if response.status_code == 200:
        return response.json()["response"].strip().replace("\n", " ")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Build a focused, one-paragraph prompt
def buildPrompt(code):
    return (
        "You are generating brief documentation for a Java code snippet.\n"
        "Your response MUST be a **single paragraph** with NO bullet points, NO line breaks, and NO section headers.\n"
        "Do NOT explain the prompt. Just output the summary.\n"
        "Keep your explanation short and focused (3–5 sentences max). Avoid repetition.\n"
        "Summarize ONLY the core logic and purpose of the code.\n\n"
        "Here is the Java code:\n\n"
        + code +
        "\n\nSummary (one paragraph only):"
    )

# Main function to collect Java files and generate documentation
if __name__ == "__main__":
    datasetsPath = pathlib.Path("datasets")
    datasets = list(datasetsPath.iterdir())
    javaFiles = list(datasets[2].rglob("*.java"))  # You can change this index as needed

    content = javaFiles[10].read_text()

    # Generate the documentation using the strict prompt
    prompt = buildPrompt(content)
    documentation = generateDocumentation(prompt)

    # Save documentation to output file
    output_path = javaFiles[10].name + "-documentation.md"
    with open(output_path, "w") as output:
        output.write(documentation)

    print(f" Generated one-paragraph documentation: {output_path}")