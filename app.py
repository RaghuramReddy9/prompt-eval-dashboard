import streamlit as st
import pandas as pd
import evaluate
from llm import generate_gemini, generate_tinyllama

rouge = evaluate.load("rouge")
st.title("🔍 LLM Model Comparator: Gemini vs TinyLLaMA")

st.header("🧪 Prompt Comparison")
compare_prompt = st.text_input("Enter prompt to compare")
reference = st.text_input("Expected ideal answer")

if compare_prompt and reference:
    # Get responses
    gemini_response = generate_gemini(compare_prompt)
    llama_response = generate_tinyllama(compare_prompt)

    # Score
    responses = {
        "Gemini": gemini_response,
        "TinyLLaMA": llama_response
    }

    results = []
    for model, response in responses.items():
        score = rouge.compute(predictions=[response], references=[reference])
        results.append({
            "Model": model,
            "Response": response,
            "ROUGE-L Score": round(score["rougeL"], 3)
        })

    # Display
    df = pd.DataFrame(results)
    st.subheader("📊 Comparison Table")
    st.dataframe(df)

    st.subheader("📈 ROUGE Scores")
    st.bar_chart(df.set_index("Model")["ROUGE-L Score"])

    # Save
    df.to_csv("logs/model_comparison_log.csv", index=False)
    st.success("✅ Logged to model_comparison_log.csv")
