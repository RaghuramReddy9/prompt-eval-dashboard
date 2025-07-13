# llm.py
import os
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from dotenv import load_dotenv
load_dotenv()


# === Setup Gemini securely ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# === Setup TinyLLaMA ===
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

def generate_tinyllama(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
