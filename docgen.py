"""
Java documentation generator
COMPSCI 422 - Final Project
Group 2 - Carter Piepenburg, Austin VanDenPlas
"""

import pathlib
import random
import time
import os
import re


from prompts import zero_shot_prompt, general_code_prompt, explanation_with_chain_of_thought, few_shot_learning_prompt

# Main function to collect Java files and generate documentation
if __name__ == "__main__":
    start_time = time.perf_counter()

    # Starting from input directory
    javaFiles = list(pathlib.Path("input").rglob("*.java"))

    outputName = "documentation"
    outputNumber = 0
    while os.path.exists("outputs\\" + outputName + "-" + str(outputNumber) + ".md"):
        outputNumber += 1

    output = open("outputs\\" + outputName + "-" + str(outputNumber) + ".md", "w", encoding="utf-8")
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
            if line:  # Not a blank line

                if "{" in line:
                    totalOpenPara += 1
                if "}" in line:
                    totalOpenPara -= 1

                if "{" in line and ("public" in line or "private" in line or "final" in line) and "class" in line and "//" not in line and "*" not in line and totalOpenPara == 1:
                    # class
                    currentClass = True
                    output.write("# " + line[:line.rfind('{')] + "\n")
                    classes.append(line[:line.rfind('{')])

                elif "{" in line and ("public" in line or "private" in line or "final" in line) and "class" not in line and "//" not in line and "*" not in line and ")" in line and currentClass is True:
                    # function
                    currentFunction = True

                    output.write("### " + line[:line.rfind(')') + 1] + "\n")
                    functions[numClasses].append(line[:line.rfind(')') + 1])

                    # Extracting function string
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
                            break

                    # Generate description using zero_shot_prompt
                    output.write("\n#### Description:\n")
                    output.write(zero_shot_prompt(functionString) + "\n")

                    # Show function code
                    output.write("\n#### Code:\n")
                    output.write("```\n" + functionString + "```\n")
                    currentFunction = False

                elif currentClass is True and currentFunction is False and "}" in line and totalOpenPara == 0 and "//" not in line and "*" not in line:
                    # end of class
                    currentClass = False
                    numClasses += 1
                    functions.append([])
                    output.write("___\n")

            index += 1

        # No function declarations in file
        if numClasses == 0:
            print("No classes detected in file")

    # Table of contents
    print("Generating table of contents...")

    output.close()
    output = open("outputs\\" + outputName + "-" + str(outputNumber) + ".md", "r+", encoding="utf-8")
    oldContent = output.read()
    output.seek(0)

    output.write("# Table of Contents" + "\n")

    index = 0
    for clas in classes:
        clasLabel = clas.replace("<", "&lt").replace(">", "&gt")
        addressString = re.sub(r'[^a-z0-9\s-]', '', clas.lower())
        addressString = re.sub(r'\s+', '-', addressString)
        addressString = "#" + addressString

        output.write("<details>\n")
        output.write(f"<summary><a href=\"{addressString}\">{clasLabel}</a></summary>\n\n")

        output.write("<ul>\n")
        for func in functions[index]:
            funcLabel = func.replace("<", "&lt").replace(">", "&gt")
            funcString = re.sub(r'[^a-z0-9\s-]', '', func.lower())
            funcString = re.sub(r'\s+', '-', funcString)
            funcString = "#" + funcString
            output.write(f"<li><a href=\"{funcString}\">{funcLabel}</a></li>\n")
        output.write("</ul>\n")
        output.write("</details>\n\n")

        index += 1

    output.write("___\n\n")
    output.write(oldContent)

    end_time = time.perf_counter()
    print(f"Generated documentation at: {output.name}")
    print(f"Process took {end_time - start_time} seconds")