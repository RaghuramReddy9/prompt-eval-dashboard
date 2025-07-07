import streamlit as st
import datetime
import pandas as pd
import evaluate
from utils.llm import generate_response as get_response

rouge = evaluate.load("rouge")

st.title(" Prompt Evaluation Logger")

# Prompt Input
prompt = st.text_input("Enter your prompt")
reference = st.text_input("Expected answer (reference)", help="Used for scoring")

#  Store logs
if "logs" not in st.session_state:
    st.session_state.logs = []


#  Handle input + log
if prompt and reference:
    response = get_response(prompt)

    # Score response vs. reference using ROUGE
    score = rouge.compute(predictions=[response], references=[reference])
    rouge_score = round(score["rougeL"], 3)

    log = {
        "Prompt": prompt,
        "Response": response,
        "Reference": reference,
        "ROUGE-L Score": rouge_score,
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    st.session_state.logs.append(log)
    st.success(f"Scored: ROUGE-L = {rouge_score}")

# Display logs
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    st.subheader("🔍 Prompt History")
    st.dataframe(df)
