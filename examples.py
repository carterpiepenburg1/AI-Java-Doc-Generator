import requests
import json

# Configure your Ollama setup
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "codegemma:2b"  # Change to your preferred model

def generate_with_ollama(prompt, model=MODEL_NAME):
    """Send a prompt to Ollama and return the generated response."""
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

# ============= PROMPTING TECHNIQUES =============

def zero_shot_prompting(task_description):
    """
    Zero-shot prompting: Ask the model to perform a task without examples.
    
    Example use: zero_shot_prompting("Explain quantum computing in simple terms.")
    """
    prompt = f"""
Task: {task_description}
Respond directly to the task above.
"""
    return generate_with_ollama(prompt)

def few_shot_prompting(task_description, examples):
    """
    Few-shot prompting: Provide a few examples before asking for a task.
    
    Example use: few_shot_prompting(
        "Translate this English phrase to French: 'I love programming'",
        [
            {"input": "Hello world", "output": "Bonjour le monde"},
            {"input": "How are you?", "output": "Comment ça va?"}
        ]
    )
    """
    # Format the examples
    examples_text = ""
    for example in examples:
        examples_text += f"Input: {example['input']}\nOutput: {example['output']}\n\n"
    
    prompt = f"""
Here are some examples:

{examples_text}
Now, I want you to do something similar:

Task: {task_description}
Output:
"""
    return generate_with_ollama(prompt)

def chain_of_thought_prompting(problem):
    """
    Chain-of-thought prompting: Ask the model to work through a problem step by step.
    
    Example use: chain_of_thought_prompting("If I have 5 apples and give 2 to my friend, then buy 3 more, how many apples do I have?")
    """
    prompt = f"""
Problem: {problem}

Let's think through this step by step to find the answer:
"""
    return generate_with_ollama(prompt)

def structured_prompting(data, system_prompt):
    """
    Structured prompting: Provide clear roles and instructions.
    
    Example use: structured_prompting(
        "What's the capital of France?",
        "You are a geography expert. Provide accurate, concise answers with one interesting fact."
    )
    """
    prompt = f"""
System: {system_prompt}
User: {data}
Assistant:
"""
    return generate_with_ollama(prompt)



# # ============= DEMONSTRATION =============
#
# if __name__ == "__main__":
#     print("\n===== ZERO-SHOT PROMPTING =====")
#     task = "Write a short poem about programming."
#     print(f"Task: {task}")
#     print(zero_shot_prompting(task))
#
#     print("\n===== FEW-SHOT PROMPTING =====")
#     examples = [
#         {"input": "Apple", "output": "A fruit that is red or green, crunchy, and sweet."},
#         {"input": "Car", "output": "A vehicle with four wheels used for transportation."}
#     ]
#     task = "Define the following: Computer"
#     print(f"Task: {task}")
#     print(few_shot_prompting(task, examples))
#
#     print("\n===== CHAIN OF THOUGHT =====")
#     problem = "If a shirt costs $15 and is on sale for 20% off, what is the final price?"
#     print(f"Problem: {problem}")
#     print(chain_of_thought_prompting(problem))
#
#     print("\n===== STRUCTURED PROMPTING =====")
#     system = "You are a helpful coding assistant who responds in bullet points."
#     query = "What are the key principles of clean code?"
#     print(f"System: {system}\nUser: {query}")
#     print(structured_prompting(query, system))
    

