import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from seo_utils import calculate_score, parse_ai_output
from main import generate_ai_content

# ---------------- PAGE ----------------
st.set_page_config(page_title="SEO AI Tool", layout="centered")

# ---------------- HEADER ----------------
st.title("🚀 YouTube SEO AI Optimizer")
st.caption("Generate viral titles, descriptions & boost ranking")

st.divider()

# ---------------- INPUT ----------------
st.subheader("📥 Input Details")

concept = st.text_input("Video Concept")
keywords = st.text_input("Keywords (comma separated)")
title = st.text_input("Title")
description = st.text_area("Description", height=120)

analyze = st.button("📊 Analyze SEO")

# ---------------- RESULT ----------------
if analyze:

    if not keywords or not title or not description:
        st.warning("⚠️ Fill all fields")
    else:
        result = calculate_score(keywords, title, description)

        st.subheader("📊 SEO Score")
        st.success(f"{result['Final Score']} / 100")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Title", result["Title Score"])
        c2.metric("Desc", result["Description Score"])
        c3.metric("Hook", result["Hook Score"])
        c4.metric("Curiosity", result["Curiosity Score"])

        # ---------------- CHARTS ----------------
        st.subheader("📈 Performance")

        labels = ["Title", "Desc", "Hook", "Curiosity"]
        max_scores = [30, 30, 20, 20]
        values = [
            result["Title Score"],
            result["Description Score"],
            result["Hook Score"],
            result["Curiosity Score"]
        ]

        x = np.arange(len(labels))

        # -------- BAR CHART --------
        fig1, ax1 = plt.subplots(figsize=(5,3))

        ax1.bar(x, values)
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)
        ax1.set_ylim(0, max(max_scores) + 10)  # 👈 FIX OVERLAP

        # labels ABOVE bars (clean spacing)
        for i in range(len(values)):
            ax1.text(
                i,
                values[i] + 2,   # 👈 extra spacing
                f"{values[i]}/{max_scores[i]}",
                ha='center',
                fontsize=9,
                fontweight='bold'
            )

        st.pyplot(fig1)

        # -------- LINE CHART --------
        fig2, ax2 = plt.subplots(figsize=(5,3))

        ax2.plot(x, values, marker='o')
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels)
        ax2.set_ylim(0, max(max_scores) + 10)  # 👈 FIX OVERLAP

        # labels ABOVE points
        for i in range(len(values)):
            ax2.text(
                i,
                values[i] + 2,
                f"{values[i]}/{max_scores[i]}",
                ha='center',
                fontsize=9,
                fontweight='bold'
            )

        st.pyplot(fig2)

# ---------------- AI SECTION ----------------
st.divider()

if st.button("🤖 Generate AI Suggestions"):

    if not concept or not keywords or not title or not description:
        st.warning("⚠️ Fill all inputs")
    else:
        ai_output = generate_ai_content(concept, keywords, title, description)

        st.subheader("🧠 AI Suggestions")
        st.code(ai_output)

        titles, ai_desc, hashtags = parse_ai_output(ai_output)

        best_score = 0
        best_title = ""

        for t in titles:
            score = calculate_score(keywords, t, ai_desc)["Final Score"]
            if score > best_score:
                best_score = score
                best_title = t

        st.success(f"🏆 Best Title: {best_title}")

        st.write("### 📄 Description")
        st.write(ai_desc)

        st.write("### #️⃣ Hashtags")
        st.write(hashtags)