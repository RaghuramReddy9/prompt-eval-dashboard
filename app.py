import asyncio
# Fix event loop on Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
import datetime
import pandas as pd
import evaluate
import sqlite3
from llm import generate_response as get_response
from utils.db import save_to_db

# Load metric
rouge = evaluate.load("rouge")


# App title
st.title("📊 Prompt Evaluation Logger")

# Model Selector
model_choice = st.selectbox("Choose Model", ["TinyLLaMA", "OpenAI", "Gemini"])

# Prompt Inputs
prompt = st.text_input("Enter your prompt")
reference = st.text_input("Expected answer (reference)", help="Used for scoring")

# Upload Prompt CSV
st.subheader("📂 Upload Prompt Set (CSV)")
uploaded_file = st.file_uploader("Upload CSV with 'Prompt' and 'Reference' columns", type=["csv"])

# Initialize logs
if "logs" not in st.session_state:
    st.session_state.logs = []

#  Bulk evaluation button
if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file)
    st.success(f"Uploaded {len(df_upload)} prompts for evaluation.")
    batch_logs = []

    if st.button("🚀 Evaluate Uploaded Prompts"):
       

        for idx, row in df_upload.iterrows():
            prompt = row["Prompt"]
            reference = row["Reference"]
            response = get_response(prompt)
            score = rouge.compute(predictions=[response], references=[reference])
            rouge_score = round(score["rougeL"], 3)

            log = {
                "Model": model_choice,
                "Prompt": prompt,
                "Response": response,
                "Reference": reference,
                "ROUGE-L Score": rouge_score,
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            batch_logs.append(log)
            save_to_db(prompt, response, reference, rouge_score, log["Timestamp"])

        st.session_state.logs.extend(batch_logs)
        st.success(f"{len(batch_logs)} prompts evaluated and logged.")
        st.dataframe(pd.DataFrame(batch_logs))

#  Handle single prompt evaluation
if prompt and reference:
    response = get_response(prompt)
    score = rouge.compute(predictions=[response], references=[reference])
    rouge_score = round(score["rougeL"], 3)

    log = {
        "Model": model_choice,
        "Prompt": prompt,
        "Response": response,
        "Reference": reference,
        "ROUGE-L Score": rouge_score,
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    st.session_state.logs.append(log)
    st.success(f"Scored: ROUGE-L = {rouge_score}")
    save_to_db(prompt, response, reference, rouge_score, log["Timestamp"])

#  Display Results
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    df.to_csv("logs/prompt_logs.csv", index=False)

    # Filter by model
    st.subheader("🔍 Prompt History")
    model_filter = st.selectbox("Filter by Model", df["Model"].unique())
    filtered_df = df[df["Model"] == model_filter]
    st.dataframe(df)

    # Download button
    st.download_button(
        label="📥 Download Logs as CSV",
        data=df.to_csv(index=False),
        file_name="prompt_logs.csv",
        mime="text/csv"
    )

    # Filter by ROUGE score
    min_score = st.slider("Filter by minimum ROUGE score", 0.0, 1.0, 0.0, 0.01)
    filtered_df = filtered_df[filtered_df["ROUGE-L Score"] >= min_score]

    st.subheader("🔍 Filtered Prompt Logs")
    st.dataframe(filtered_df)

    st.subheader("📊 ROUGE Score Chart")
    st.bar_chart(filtered_df["ROUGE-L Score"])

    st.subheader("📈 Summary")
    total = len(df)
    above_90 = len(df[df["ROUGE-L Score"] >= 0.9])
    avg_score = round(df["ROUGE-L Score"].mean(), 3)

    st.markdown(f"**Total Prompts:** {total}")
    st.markdown(f"**Average ROUGE Score:** {avg_score}")
    st.markdown(f"**% Scored ≥ 0.9:** {round(100 * above_90 / total, 1)}%")

    st.subheader("📊 Avg ROUGE by Model")
    model_scores = df.groupby("Model")["ROUGE-L Score"].mean().round(3)
    st.bar_chart(model_scores)
