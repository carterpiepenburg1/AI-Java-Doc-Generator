"""
Code-base documentation generator
COMPSCI 422 - Final Project
Group 2 - Carter Piepenburg, Austin VanDenPlas
"""

import requests
import json
import pathlib

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:1.5b"
#MODEL_NAME = "deepseek-r1:1.5b"

def generateDocumentation(prompt, model=MODEL_NAME):
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

#Collecting every java file from dataset
if __name__ == "__main__":
    datasetsPath = (pathlib.Path("datasets"))
    datasets = list(datasetsPath.iterdir())

    javaFiles = list(datasets[2].rglob("*.java"))

    content = javaFiles[10].read_text()
    output = open(javaFiles[10].name + "-documentation.md", "w")

    output.write(generateDocumentation("Write documentation for all functions in this java code."
                                       "Do not include anything in the response other than the following for each function {"
                                       "Function: (function name with parameters)"
                                       "Parameters: A list of the parameters with short descriptions"
                                       "Description: A brief description of the function and its usage }"
                                       "Format the responses as if it was a .md file."
                                       "Here is the code: " + content))

    print("Generated documentation " + output.name + "\n")

