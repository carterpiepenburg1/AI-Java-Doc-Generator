Notes:
1. Train open source LLM to detect comments and code functionality to generate documentation for functions
2. Use a model with lower b value (2.5 to 5)
3. Presentations will be mostly showing code and functionality
4. Presentations will probably only cover one complicated class/file

To run you must install the following:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 (WINDOWS WITH GPU)
ollama pull codegemma:2b
ollama pull deepseek-r1:1.5b
ollama pull qwen2.5-coder:1.5b
