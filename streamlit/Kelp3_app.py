import streamlit as st
import pandas as pd
import json
from collections import Counter
import os

st.set_page_config(page_title="Dataset Explorer", layout="wide")

@st.cache_data
def load_data(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            obj = json.loads(line)
            text = obj.get("text", "")

            for span in obj.get("spans", []):
                label = span["label"]

                if label == "OUT_OF_TOPIC":
                    continue

                try:
                    aspect, sentiment = label.split("_")
                except:
                    continue

                data.append({
                    "review_id": i,
                    "text": text,
                    "aspect": aspect,
                    "sentiment": sentiment
                })

    return pd.DataFrame(data)

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "dataset", "Kelp3_dataset_anotasi.jsonl")
df = load_data(DATA_PATH)

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", [
    "Overview",
    "Browse Reviews",
    "Statistik",
    "Panel ABSA"
])

if menu == "Overview":
    st.title("📊 Overview Dataset")

    st.write("Jumlah Data:", len(df))
    st.write("Jumlah Review:", df["review_id"].nunique())

    st.subheader("Distribusi Aspek")
    st.bar_chart(df["aspect"].value_counts())

elif menu == "Browse Reviews":
    st.title("🔍 Browse Reviews")

    keyword = st.text_input("Cari Review")

    if keyword:
        filtered = df[df["text"].str.contains(keyword, case=False)]
    else:
        filtered = df

    st.dataframe(filtered[["text", "aspect", "sentiment"]])

elif menu == "Statistik":
    st.title("Statistik")

    st.subheader("Distribusi Sentimen")
    st.bar_chart(df["sentiment"].value_counts())

    st.subheader("Panjang Review")
    df["length"] = df["text"].apply(len)
    st.bar_chart(df["length"])

# ========================
elif menu == "Panel ABSA":
    st.title("Panel ABSA")

    aspek = st.selectbox("Pilih Aspek", df["aspect"].unique())
    sentimen = st.selectbox("Pilih Sentimen", df["sentiment"].unique())

    filtered = df[
        (df["aspect"] == aspek) &
        (df["sentiment"] == sentimen)
    ]

    st.write("Jumlah:", len(filtered))
    st.dataframe(filtered)
