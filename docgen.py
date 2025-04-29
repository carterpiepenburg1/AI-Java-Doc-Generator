import requests
import pathlib
import random
import json
import time  # Import time module for timing

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:1.5b"

def generate(prompt, model=MODEL_NAME):
    """
    Send prompt to the Ollama API and return the generated response.
    """
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=data)
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == "__main__":
    # Define the path to your specific Java file
    specific_file_path = pathlib.Path("datasets/Java-master/src/main/java/com/thealgorithms/puzzlesandgames/Sudoku.java")  # Modify this path if needed

    # Start timing the execution
    start_time = time.time()

    lines = specific_file_path.read_text().splitlines()

    output_folder = pathlib.Path("outputs")
    output_folder.mkdir(exist_ok=True)

    output_md = open(output_folder / (specific_file_path.stem + "-documentation.md"), "w")
    output_md.write("# " + specific_file_path.stem + "\n")

    documentation_entries = []
    function_blocks = []  # Save detected functions
    index = 0

    print("Scanning Java file...\n")

    while index < len(lines):
        line = lines[index].strip()
        if line:  # Not blank
            if "{" in line and ("public" in line or "private" in line) and "class" not in line and "//" not in line and ")" in line:
                function_signature = line[:line.rfind(')') + 1]

                # Extract full function body
                openPara = 1
                functionString = lines[index]
                index += 1
                while openPara > 0 and index < len(lines):
                    line = lines[index]
                    functionString += "\n" + line
                    if "{" in line:
                        openPara += line.count("{")
                    if "}" in line:
                        openPara -= line.count("}")
                    index += 1

                function_blocks.append({
                    "signature": function_signature,
                    "code": functionString
                })
                continue  # Skip normal index increment to avoid skipping lines
        index += 1

    # No functions detected
    if not function_blocks:
        output_md.write("## No functions detected in this file.\n")
        output_md.close()
        print(f"No functions found in {specific_file_path.name}")
        exit(0)

    # --- Build big prompt ---
    big_prompt = (
        "You are generating brief documentation for multiple Java functions.\n"
        "For each function, write exactly **one short paragraph** that summarizes its core logic.\n"
        "NO bullet points, NO line breaks inside the paragraph.\n"
        "Format your output exactly like this:\n\n"
        "Function 1: [One paragraph summary]\n\n"
        "Function 2: [One paragraph summary]\n\n"
        "Function 3: [One paragraph summary]\n\n"
        "DO NOT skip any function. Always number them correctly.\n"
        "Start now:\n\n"
    )

    for idx, block in enumerate(function_blocks, 1):
        big_prompt += f"Function {idx}:\n{block['code']}\n\n"

    # --- Send 1 API request ---
    print(f"Sending {len(function_blocks)} functions in one API call...")
    ai_response = generate(big_prompt)

    # --- Parse AI response ---
    print("Parsing AI response...")

    splits = ai_response.split("Function ")
    function_summaries = {}
    for part in splits:
        if part.strip():
            header_end = part.find(":")
            if header_end != -1:
                idx = int(part[:header_end].strip())
                summary = part[header_end+1:].strip()
                function_summaries[idx] = summary

    # --- Write markdown and json outputs ---
    for idx, block in enumerate(function_blocks, 1):
        signature = block["signature"]
        code = block["code"]
        description = function_summaries.get(idx, "No description generated.")

        # Markdown
        output_md.write("___\n")
        output_md.write(f"### {signature}\n")
        output_md.write("\n#### Description:\n")
        output_md.write(description + "\n")
        output_md.write("\n#### Code:\n")
        output_md.write("```\n" + code + "\n```\n")

        # JSON
        documentation_entries.append({
            "function_signature": signature,
            "description": description,
            "code": code.strip()
        })

    output_md.close()

    # Save JSON file
    json_filename = output_folder / (specific_file_path.stem + "-documentation.json")
    try:
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(documentation_entries, f, indent=4, ensure_ascii=False)
        print(f"Documentation saved to: {json_filename}")
    except Exception as e:
        print(f"Failed to save JSON file: {e}")

    print(f"Generated markdown documentation at: {output_md.name}")

    # End timing and print time taken
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken to process the file: {execution_time:.2f} seconds")