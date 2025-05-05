import requests

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:1.5b"

def generate(prompt: str, model=MODEL_NAME) -> str:
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

def zero_shot_prompt(function_code: str) -> str:
    prompt = (
        "Write documentation for all functions in this java code."
        " Do not include anything in the response other than the following for each function {"
        " Function: (function name with parameters)"
        " Parameters: A list of the parameters with short descriptions"
        " Description: A brief description of the function and its usage }"
        " Format the responses as if it was a .md file."
        f" Here is the code: {function_code}"
    )
    return generate(prompt)

def general_code_prompt(function_code: str) -> str:
    prompt = (
        "You are a helpful assistant that generates Java function documentation."
        " Generate a markdown (.md) formatted section that includes:"
        "\n- Function signature"
        "\n- Parameter list with brief descriptions"
        "\n- A concise one-paragraph summary of what the function does"
        "\nDo not include any extra explanation or section headers beyond the markdown."
        f"\nHere is the Java function:\n{function_code}"
    )
    return generate(prompt)



#move generate from docgen to prompts.py then call generate in zero shot prompt and have that function return the response to docgen