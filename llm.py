from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to("cpu")

def generate_response(prompt):
    
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id  # Optional fix for small models
        )

    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Only slice if it starts with prompt
    if decoded.startswith(prompt):
        return decoded[len(prompt):].strip()
    return decoded.strip()

