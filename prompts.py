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
        f"""
You are generating brief documentation for a Java code snippet.
Your response MUST be a single paragraph with NO bulletpoints, NO line breaks, and NO section headers.
Do NOT explain the prompt. Just output the summary.
Keep your explanation short and focused. Avoid repetition.
Start your response with the words (This function)
Summarize ONLY the core logic and purpose of the code.
Here is the Java code:
Summary (one paragraph only):
{function_code}"""
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
    examples = (
        "Example 1:\n"
        "Code:\n"
        "public static int max(int a, int b) {\n"
        "    return a > b ? a : b;\n"
        "}\n"
        "Step-by-step reasoning:\n"
        "1. The function `max` takes two integers as input.\n"
        "2. It compares the two integers using the ternary operator.\n"
        "3. If `a` is greater than `b`, it returns `a`; otherwise, it returns `b`.\n"
        "\nMarkdown documentation:\n"
        "```markdown\n"
        "Function: public static int max(int a, int b)\n"
        "Parameters:\n"
        "- a: First integer\n"
        "- b: Second integer\n"
        "Description:\n"
        "Returns the greater of the two input integers.\n"
        "```\n"
        "---\n"
        "Example 2:\n"
        "Code:\n"
        "public static int factorial(int n) {\n"
        "    if (n <= 1) return 1;\n"
        "    return n * factorial(n - 1);\n"
        "}\n"
        "Step-by-step reasoning:\n"
        "1. The function `factorial` takes a single integer `n`.\n"
        "2. If `n` is 1 or less, it returns 1 (base case).\n"
        "3. Otherwise, it returns `n` multiplied by the factorial of `n - 1` (recursive case).\n"
        "\nMarkdown documentation:\n"
        "```markdown\n"
        "Function: public static int factorial(int n)\n"
        "Parameters:\n"
        "- n: A non-negative integer\n"
        "Description:\n"
        "Computes the factorial of the input integer using recursion.\n"
        "```\n"
        "---\n"
    )
    prompt = (
        "Analyze the following Java function in a direct, step-by-step manner without pleasantries or introductions."
        " Then, provide a clean markdown (.md) documentation section."
        " Your response should begin immediately with the analysis and stay technical."
        "\n\n"
        f"{examples}"
        "Now analyze this code:\n"
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
        "Function: public static boolean isEven(int number)\n"
        "Parameters:\n"
        "- number: The integer to check\n"
        "Description:\n"
        "Returns true if the number is even, false otherwise.\n"
        "---\n"
        "Function: public static void printList(List<String> items)\n"
        "Parameters:\n"
        "- items: A list of strings to print\n"
        "Description:\n"
        "Prints each string from the provided list on a new line.\n"
        "---\n"
    )
    prompt = (
        "Based on the format shown below, write documentation for this Java function."
        f"\n\n{few_shot_example}"
        f"Java code:\n\n{function_code}"
    )
    return generate(prompt)

