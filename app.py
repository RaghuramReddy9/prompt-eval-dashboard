import streamlit as st
import datetime
import pandas as pd
import evaluate
import sqlite3
import asyncio
from llm import generate_response as get_response
from utils.db import save_to_db

rouge = evaluate.load("rouge")

st.title(" Prompt Evaluation Logger")

# Fix the "no running loop" error on Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
    # Adding SQLite database
    save_to_db(
        prompt,
        response,
        reference,
        rouge_score,
        log["Timestamp"]
        )

if st.session_state.logs:
    #  Create the DataFrame
    df = pd.DataFrame(st.session_state.logs)
    df.to_csv("logs/prompt_logs.csv", index=False)

    #  Show full prompt history
    st.subheader("🔍 Prompt History")
    st.dataframe(df)

    #  Download button
    st.download_button(
        label="📥 Download Logs as CSV",
        data=df.to_csv(index=False),
        file_name="prompt_logs.csv",
        mime="text/csv"
    )

    #  FILTER logic starts here — only runs if df exists
    min_score = st.slider("Filter by minimum ROUGE score", 0.0, 1.0, 0.0, 0.01)
    filtered_df = df[df["ROUGE-L Score"] >= min_score]

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
