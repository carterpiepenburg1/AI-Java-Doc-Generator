"""
Java documentation generator
COMPSCI 422 - Final Project
Group 2 - Carter Piepenburg, Austin VanDenPlas
"""

import requests
import pathlib
import random
import time
import os
import re

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
    start_time = time.perf_counter()

    #Collecting random java file
    #datasetsPath = pathlib.Path("datasets")
    #datasets = list(datasetsPath.iterdir())
    #javaFiles = list(random.choice(datasets).rglob("*.java"))
    #filePath = random.choice(javaFiles)
    #Specific java file
    #filePath = pathlib.Path("datasets/Java-master/src/main/java/com/thealgorithms/puzzlesandgames/Sudoku.java")

    #Starting from input directory
    javaFiles = list(pathlib.Path("input").rglob("*.java"))

    output = open(r"outputs\documentation.md", "w")
    classes = []
    numClasses = 0
    functions = [[]]

    for filePath in javaFiles:

        context = filePath.read_text()
        file = open(filePath)

        lines = file.readlines()
        index = 0

        currentClass = False
        currentFunction = False

        totalOpenPara = 0

        print("Generating documentation for " + file.name + "...")
        while index < len(lines):
            line = lines[index].strip()
            if line: #Not a blank line

                if "{" in line:
                    totalOpenPara += 1
                if "}" in line:
                    totalOpenPara -= 1

                if "{" in line and ("public" in line or "private" in line or "final" in line) and "class" in line and "//" not in line and "*" not in line and totalOpenPara == 1:
                    #class
                    currentClass = True

                    output.write("# " + line[:line.rfind('{')] + "\n")
                    classes.append(line[:line.rfind('{')])

                elif "{" in line and ("public" in line or "private" in line or "final" in line) and "class" not in line and "//" not in line and "*" not in line and ")" in line and currentClass is True:
                    #function
                    currentFunction = True

                    #Function header
                    #output.write("___\n")
                    output.write("### " + line[:line.rfind(')') + 1] + "\n")
                    functions[numClasses].append(line[:line.rfind(')') + 1])

                    #Extracting function string
                    openPara = totalOpenPara - 1
                    functionString = lines[index]
                    while totalOpenPara > openPara:
                        index += 1
                        if index < len(lines):
                            line = lines[index].strip()
                            if line:  # Not a blank line
                                functionString = functionString + lines[index]
                                if "{" in line:
                                    totalOpenPara += 1
                                if "}" in line:
                                    totalOpenPara -= 1
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
                    currentFunction = False

                elif currentClass is True and currentFunction is False and "}" in line and totalOpenPara == 0 and "//" not in line and "*" not in line:
                    #end of class
                    currentClass = False
                    numClasses += 1
                    functions.append([])
                    output.write("___\n")

            index += 1

        #No function declarations in file
        if numClasses == 0:
            #output.write("## No classes detected in file.\n")
            print("No classes detected in file")

    #table of contents
    print("Generating table of contents...")

    output.close()
    output = open(r"outputs\documentation.md", "r+")
    oldContent = output.read()
    output.seek(0)

    output.write("# Table of Contents" + "\n")

    index = 0
    for clas in classes:
        clasLabel = clas
        clasLabel = clasLabel.replace("<", "&lt")
        clasLabel = clasLabel.replace(">", "&gt")
        addressString = clas
        addressString = addressString.lower()
        addressString = re.sub(r'[^a-z0-9\s-]', '', addressString)
        addressString = addressString.replace(" ", "-")
        addressString = "#" + addressString

        output.write("<details>\n")
        output.write(f"<summary><a href=\"{addressString}\">{clasLabel}</a></summary>\n\n")

        output.write("<ul>\n")
        for func in functions[index]:
            funcLabel = func
            funcLabel = funcLabel.replace("<", "&lt")
            funcLabel = funcLabel.replace(">", "&gt")
            funcString = func
            funcString = funcString.lower()
            funcString = re.sub(r'[^a-z0-9\s-]', '', funcString)
            funcString = funcString.replace(" ", "-")
            funcString = "#" + funcString
            output.write(f"<li><a href=\"{funcString}\">{funcLabel}</a></li>\n")
        output.write("</ul>\n")
        output.write("</details>\n\n")

        index+=1

    output.write("___\n\n")

    output.write(oldContent)

    end_time = time.perf_counter()
    print(f"Generated documentation at: {output.name}")
    print(f"Process took {end_time - start_time} seconds")



