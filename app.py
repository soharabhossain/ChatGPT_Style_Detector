import streamlit as st
import pandas as pd
import json
from style_detector import ChatGPTStyleDetector
import altair as alt

st.set_page_config(page_title="ChatGPT Style Detector", layout="wide")
st.title("🧠 ChatGPT Writing Style Detector")

st.markdown("""
Upload a list of **style words** and one or two `.txt` files. The app will:
- Highlight style words
- Compute style scores
- Visualize word frequencies
- Export results as `.json` or `.csv`
""")

style_words_file = st.file_uploader("📘 Upload `style_words.txt`", type=["txt"])
text1_file = st.file_uploader("📄 Upload Text File 1", type=["txt"], key="text1")
text2_file = st.file_uploader("📄 Upload Text File 2 (optional for comparison)", type=["txt"], key="text2")

def display_results(text_label, text_data, detector):
    result = detector.analyze_text(text_data)
    highlighted = detector.highlight_style_words(text_data)

    st.subheader(f"📄 {text_label} Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Words", result['total_words'])
    col2.metric("Style Words Found", result['num_style_words'])
    col3.metric("Style Score", f"{result['style_score_percent']} %")

    st.markdown("**🖋 Highlighted Text:**")
    st.markdown(highlighted, unsafe_allow_html=True)

    if result['style_words_found']:
        df = pd.DataFrame(
            list(result['style_words_found'].items()),
            columns=["Style Word", "Count"]
        ).sort_values("Count", ascending=False)

        st.markdown("**📊 Style Word Frequency Chart**")
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("Style Word", sort='-y'),
            y="Count",
            tooltip=["Style Word", "Count"]
        ).properties(width=600)
        st.altair_chart(chart, use_container_width=True)

        st.markdown("**📁 Download Analysis**")
        col1, col2 = st.columns(2)
        json_data = json.dumps(result, indent=2)
        csv_data = df.to_csv(index=False)

        col1.download_button("⬇️ Download JSON", json_data, file_name=f"{text_label.lower().replace(' ', '_')}_analysis.json")
        col2.download_button("⬇️ Download CSV", csv_data, file_name=f"{text_label.lower().replace(' ', '_')}_frequency.csv")
    else:
        st.info("No style words found in the text.")

    return result

if style_words_file and text1_file:
    style_words = style_words_file.read().decode("utf-8").splitlines()
    detector = ChatGPTStyleDetector(style_words)
    text1 = text1_file.read().decode("utf-8")

    result1 = display_results("Text 1", text1, detector)

    if text2_file:
        text2 = text2_file.read().decode("utf-8")
        result2 = display_results("Text 2", text2, detector)

        similarity = round(100 - abs(result1['style_score_percent'] - result2['style_score_percent']), 2)
        st.subheader("🔍 Style Similarity Between Texts")
        st.metric("Similarity Score", f"{similarity} %")