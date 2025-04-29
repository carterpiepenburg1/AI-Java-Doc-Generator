"""
Code-base documentation generator
COMPSCI 422 - Final Project
Group 2 - Carter Piepenburg, Austin VanDenPlas
"""

import pathlib
from docgen import build_prompt, generate_documentation
from json_utils import save_to_json

if __name__ == "__main__":
    # Path to dataset
    datasetsPath = pathlib.Path("datasets")
    datasets = list(datasetsPath.iterdir())

    javaFiles = list(datasets[2].rglob("*.java"))[:5]  # Just 2 files for testing

    # This will store the documentation results
    documentation_entries = []

    # Loop over each Java file
    for javaFile in javaFiles:
        try:
            content = javaFile.read_text()
            prompt = build_prompt(content)
            documentation = generate_documentation(prompt)

            entry = {
                "filename": javaFile.name,
                "summary": documentation.strip()
            }
            # Add the entry to our list
            documentation_entries.append(entry)
            #Success
            print(f"Processed: {javaFile.name}")
        except Exception as e:
            #Failure
            print(f"Failed to process {javaFile.name}: {e}")

    # Save all entries into a JSON file
    save_to_json(documentation_entries, "documentation.json")
    print(f"Documentation saved to documentation.json")