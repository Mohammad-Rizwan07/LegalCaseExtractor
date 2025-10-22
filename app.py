import streamlit as st
import os
from extractor import extract_text_from_pdf, clean_text, build_nodes, extract_metadata
from tqdm import tqdm

st.set_page_config(page_title="Case Extractor", page_icon="⚖️", layout="wide")
st.title("⚖️ Legal Case Extractor - For & Against Points")

uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])

if uploaded_file:
    os.makedirs("temp_files", exist_ok=True)
    pdf_path = os.path.join("temp_files", uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extract & clean
    with st.spinner("🔍 Extracting text..."):
        text = extract_text_from_pdf(pdf_path)
        cleaned = clean_text(text)
    st.success("✅ Text extracted!")

    st.text_area("📄 Text Preview", cleaned[:1500] + "...", height=200)

    # Build nodes & metadata
    with st.spinner("⚙️ Extracting metadata..."):
        nodes = build_nodes(cleaned)
        metadata_results = extract_metadata(nodes[:5])  # limit for speed

    # Display For & Against points safely
    st.subheader("🟩 For Points")
    for_points = metadata_results[0]['metadata'].get('for_points', [])
    if for_points:
        for pt in for_points:
            st.write(f"• {pt}")
    else:
        st.write("No 'For' points found.")

    st.subheader("🟥 Against Points")
    against_points = metadata_results[0]['metadata'].get('against_points', [])
    if against_points:
        for pt in against_points:
            st.write(f"• {pt}")
    else:
        st.write("No 'Against' points found.")

    # Display section metadata
    st.subheader("📊 Metadata per Section")
    for i, r in enumerate(metadata_results, 1):
        with st.expander(f"Section {i}"):
            st.write(f"**Text:** {r['text'][:300]}...")
            st.write(f"**Title:** {r['metadata']['title']}")
            st.write(f"**Summary:** {r['metadata']['summary']}")
            st.write(f"**Keywords:** {r['metadata']['keywords']}")
            st.write(f"**Questions:** {r['metadata']['questions']}")
            st.write(f"**Entities:** {r['metadata']['entities']}")

else:
    st.info("👆 Upload a PDF to extract case details.")
