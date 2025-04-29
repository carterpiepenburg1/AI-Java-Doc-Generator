import re
import requests

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:1.5b"

def generate(prompt, model=MODEL_NAME):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=data)
    if response.status_code == 200:
        return response.json()["response"].strip().replace("\n", " ")
    else:
        return f"Error: {response.status_code}, {response.text}"

def build_prompt_block(code: str) -> str:
    return (
        "You are generating brief documentation for a Java code snippet.\n"
        "Your response MUST be a **single paragraph** with NO bullet points, NO line breaks, and NO section headers.\n"
        "Do NOT explain the prompt. Just output the summary.\n"
        "Keep your explanation short and focused. Avoid repetition.\n"
        "Start your response with 'This function '.\n"
        "Summarize ONLY the core logic and purpose of the code.\n\n"
        f"Here is the Java code:\n\n{code}\n\nSummary (one paragraph only):"
    )

def extract_class_functions_from_java(code: str):
    lines = code.splitlines()
    inside_class = False
    functions = []
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if re.match(r"(public|private|protected)?\s*class\s+\w+", line):
            inside_class = True

        if inside_class and re.match(r"(public|private|protected).*\(.*\).*{", line) and "class" not in line:
            header = line[:line.find("{")+1]
            function_body = lines[index] + "\n"
            open_braces = 1
            index += 1

            while index < len(lines) and open_braces > 0:
                next_line = lines[index]
                function_body += next_line + "\n"
                open_braces += next_line.count("{")
                open_braces -= next_line.count("}")
                index += 1

            functions.append({
                "header": header.strip(),
                "code": function_body.strip()
            })
        else:
            index += 1

    return functions

def parse_response_blocks(response: str, expected_count: int):
    # Attempt to split on "---" or newlines, return list of summaries
    blocks = [block.strip() for block in response.split("---") if block.strip()]
    if len(blocks) != expected_count:
        print("Mismatch in expected response count. Returning raw fallback.")
        return [response.strip()] * expected_count
    return blocks