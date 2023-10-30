# LlaMA 2 7B LLM Generative AI NLP Professional resume writer

This tool will help you to get a job interview by simply aligning your resume with the job Ad requirements. This tool uses Meta's famous Llama 2 large language model.

## Run Locally

### 1. Download LlaMA 2 model from Hugging Face

[LlaMA 2 7b Model GGUF file](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q8_0.gguf) 7 GB

### 2. Place downloaded file path inside llama_cpu.py

```python
MODEL_PATH = "D:\\path\\to\\folder\\llama-2-7b-chat.Q8_0.gguf"
```

### 3. Install Packages Python version is 3.9.18

```sh
$ pip install -r requirements.txt
```

### 4. Run server

```sh
$ uvicorn api:app
```

### 5. Open frontend

Open browser and navigate to URL

http://127.0.0.1:8000/frontend/index.html

## CPU/RAM requirements

Atleast a good 6 core CPU.
12 GB of free RAM.
