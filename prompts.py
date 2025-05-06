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

def explanation_with_chain_of_thought(function_code: str) -> str:
    prompt = (
        "Analyze the following Java function in a direct, step-by-step manner without pleasantries or introductions."
        " Then, provide a clean markdown (.md) documentation section."
        " Your response should begin immediately with the analysis and stay technical."
        "\n\nCode:\n"
        f"{function_code}"
    )
    return generate(prompt)


def few_shot_learning_prompt(function_code: str) -> str:
    few_shot_example = (
        "Example:\n"
        "Function: public static int add(int a, int b)\n"
        "Parameters:\n"
        "- a: First integer\n"
        "- b: Second integer\n"
        "Description:\n"
        "Adds two integers and returns the result.\n"
        "---\n"
    )
    prompt = (
        "Based on the format shown below, write documentation for this Java function."
        f"\n\n{few_shot_example}"
        f"Java code:\n\n{function_code}"
    )
    return generate(prompt)

#move generate from docgen to prompts.py then call generate in zero shot prompt and have that function return the response to docgen