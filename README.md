# LLM Model Comparator: Gemini vs TinyLLaMA

This project lets you compare prompt responses from two LLMs — **Google Gemini 1.5 Flash** and **TinyLLaMA** — using the **ROUGE-L metric**. It evaluates which model gives a better answer compared to a reference answer and visualizes the results.

Built with **Streamlit**, this app is perfect for developers, researchers, and prompt engineers who want to benchmark lightweight and powerful models.

---

## Features


-  Compare two LLM responses to the same prompt
-  ROUGE-L scoring against your reference answer
-  Dynamic bar chart to visualize model performance
-  Logs all responses, scores, and timestamps to `model_comparison_log.csv`
-  Uses `.env` to securely hide your API keys

---

## Example Use Case

> **Prompt**: “What is fine-tuning in machine learning?”  
> **Reference Answer**: “Fine-tuning means adapting a pre-trained model on a smaller, task-specific dataset.”

The app compares both models’ answers to the reference, scores them with ROUGE, and shows a visual chart of who performed better.

---

##  Tech Stack

| Tool            | Purpose                            |
|-----------------|------------------------------------|
| Streamlit       | Frontend Web UI                    |
| Google Gemini   | LLM API (via `google.generativeai`)|
| TinyLLaMA       | Local lightweight LLM (PyTorch)    |
| Evaluate + ROUGE| Scoring language output similarity |
| Pandas          | Data processing                    |
| SQLite          | Optional (if logging to DB)        |


---

##  Run This App Locally

### 1. Clone the repo
```bash
git clone https://github.com/RaghuramReddy9/prompt-eval-dashboard.git
cd llm-model-comparator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Add Your `.env` File
```bash
GEMINI_API_KEY=your_google_api_key_here
```

### 4. Launch the app
```bash
streamlit run app.py
```
⚠️ First-time model loading may take 1–2 minutes (~2GB). After that, it's instant.


### Folder Structure
```perl
├── app.py                   # Main Streamlit app
├── llm.py                   # Gemini & TinyLLaMA model logic
├── utils/
│   └── db.py                # Optional SQLite logging
├── logs/
│   └── model_comparison_log.csv
├── .env                     # Your Gemini API key (excluded from Git)
├── requirements.txt
├── .gitignore
└── README.md

```


### 👨‍💻 Author
```
Raghuram Reddy
Aspiring GenAI Engineer | Building real-world LLM apps
```

### 📄 License
```
MIT License
```
