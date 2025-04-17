"""
Code-base documentation generator
COMPSCI 422 - Final Project
Group 2 - Carter Piepenburg, Austin VanDenPlas
"""

import requests
import pathlib
import random

OLLAMA_API = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5-coder:1.5b"
#MODEL_NAME = "smollm2"
#MODEL_NAME = "llama3.2:1b"

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

# Main function to collect Java files and generate documentation
if __name__ == "__main__":
    datasetsPath = pathlib.Path("datasets")
    datasets = list(datasetsPath.iterdir())

    #Collecting random java file
    javaFiles = list(random.choice(datasets).rglob("*.java"))
    filePath = random.choice(javaFiles)
    #Specific java file
    #filePath = pathlib.Path("datasets/Java-master/src/main/java/com/thealgorithms/puzzlesandgames/Sudoku.java")

    context = filePath.read_text()
    file = open(filePath)
    output = open("outputs/" + filePath.name.removesuffix(".java") + "-documentation.md", "w")

    output.write("# " + filePath.name.removesuffix(".java") + "\n")
    lines = file.readlines()
    index = 0
    numFunctions = 0
    print("Scanning Java file...\n")
    while index < len(lines):
        line = lines[index].strip()
        if line: #Not a blank line
            if "{" in line and ("public" in line or "private" in line) and "class" not in line and "//" not in line and ")" in line:

                #Function header
                output.write("___\n")
                output.write("### " + line[:line.rfind(')') + 1] + "\n")

                #Extracting function string
                openPara = 1
                functionString = lines[index]
                while openPara > 0:
                    index += 1
                    if index < len(lines):
                        line = lines[index].strip()
                        if line:  # Not a blank line
                            functionString = functionString + lines[index]
                            if "{" in line:
                                openPara += 1
                            if "}" in line:
                                openPara -= 1
                    else:
                        break;

                #Function generated description
                output.write("\n#### Description:\n")
                #output.write(generate("Describe this function using ONLY one paragraph." + functionString) + "\n")
                output.write(generate("You are generating brief documentation for a Java code snippet.\n" 
                                      "Your response MUST be a **single paragraph** with NO bullet points, NO line breaks, and NO section headers.\n" 
                                      "Do NOT explain the prompt. Just output the summary.\n" 
                                      "Keep your explanation short and focused. Avoid repetition.\n"
                                      "Start your response with 'This function '\n" 
                                      "Summarize ONLY the core logic and purpose of the code.\n\n" 
                                      "Here is the Java code:\n\n" + functionString + "\n\nSummary (one paragraph only):\n" ))

                #Showing function code
                output.write("\n#### Code:\n")
                output.write("```\n" + functionString + "```\n")

                numFunctions+=1

        index += 1

    #No function declarations in file
    if numFunctions == 0:
        output.write("## No functions detected in this file.\n")

    print(f" Generated documentation at: {output.name}")
