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

def generate(prompt, model=MODEL_NAME):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=data)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == "__main__":
    datasetsPath = (pathlib.Path("datasets"))
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
                output.write("#### Description:\n")
                output.write(generate("Describe this function using ONLY one paragraph." + functionString) + "\n")

                #Showing function code
                output.write("#### Code:\n")
                output.write("```\n" + functionString + "```\n")

                numFunctions+=1

        index += 1

    #No function declarations in file
    if numFunctions == 0:
        output.write("## No functions detected in this file.\n")

    print("Generated documentation " + output.name + "\n")

