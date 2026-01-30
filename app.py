import streamlit as st
import PyPDF2
import docx
import time

from logic import (
    assess_risk,
    overall_contract_risk,
    final_advice,
    mock_ai_response
)

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Contract Risk Assessment Bot",
    layout="wide"
)

# --------------------------------------------------
# Soft CSS polish (SAFE, professional)
# --------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stExpander"] {
        border-radius: 14px;
        border: 1px solid #e0e0e0;
        padding: 12px;
        margin-bottom: 12px;
        background-color: #fafafa;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #eee;
        padding: 15px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Title & description
# --------------------------------------------------
st.title("📄 Contract Analysis & Risk Assessment Bot")
st.write(
    "A GenAI-powered assistant for Indian SMEs to analyze contracts, "
    "identify legal risks, and get simple business-friendly explanations."
)

# --------------------------------------------------
# File reading helpers
# --------------------------------------------------
def read_txt(file):
    return file.read().decode("utf-8")


def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_docx(file):
    document = docx.Document(file)
    return "\n".join([p.text for p in document.paragraphs])


# --------------------------------------------------
# File upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload contract file (PDF, DOCX, or TXT)",
    type=["pdf", "docx", "txt"]
)

contract_text = ""

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        contract_text = read_txt(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        contract_text = read_pdf(uploaded_file)
    elif uploaded_file.type == (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        contract_text = read_docx(uploaded_file)

# --------------------------------------------------
# Text area
# --------------------------------------------------
contract_text = st.text_area(
    "Contract Text",
    value=contract_text,
    height=300,
    placeholder="Paste contract text here if not uploading a file..."
)

# --------------------------------------------------
# Analyze button with animation
# --------------------------------------------------
if st.button("🔍 Analyze Contract"):
    if contract_text.strip() == "":
        st.warning("Please upload a file or paste contract text.")
    else:
        # Spinner + progress animation
        with st.spinner("Analyzing contract clauses and risks..."):
            progress = st.progress(0)
            for i in range(5):
                time.sleep(0.25)
                progress.progress((i + 1) * 20)

            # Clause extraction
            raw_lines = contract_text.split("\n")
            clauses = [c.strip() for c in raw_lines if len(c.strip()) > 30]

            results = []

            for i, clause in enumerate(clauses, start=1):
                risk, reason = assess_risk(clause)
                ai_out = mock_ai_response(clause, risk)

                results.append({
                    "clause_no": i,
                    "text": clause,
                    "risk_level": risk,
                    "reason": reason,
                    "ai_explanation": ai_out["explanation"],
                    "ai_suggestion": ai_out["suggested_alternative"]
                })

            overall = overall_contract_risk(results)

        # Toast notification
        st.toast("✅ Contract analysis completed!", icon="📄")

        # --------------------------------------------------
        # Summary section (animated feel)
        # --------------------------------------------------
        st.markdown("---")
        st.subheader(f"📊 Overall Contract Risk: **{overall}**")
        st.write(final_advice(overall))

        high_count = len([r for r in results if r["risk_level"] == "High"])
        medium_count = len([r for r in results if r["risk_level"] == "Medium"])
        low_count = len([r for r in results if r["risk_level"] == "Low"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 High Risk Clauses", high_count)
        with col2:
            st.metric("🟠 Medium Risk Clauses", medium_count)
        with col3:
            st.metric("🟢 Low Risk Clauses", low_count)

        if overall == "Low":
            st.balloons()

        # --------------------------------------------------
        # Clause-by-clause analysis
        # --------------------------------------------------
        st.markdown("---")
        st.subheader("📌 Clause-by-Clause Analysis")

        for r in results:
            if r["risk_level"] == "High":
                risk_icon = "🔴"
            elif r["risk_level"] == "Medium":
                risk_icon = "🟠"
            else:
                risk_icon = "🟢"

            with st.expander(
                f"{risk_icon} Clause {r['clause_no']} — {r['risk_level']} Risk"
            ):
                st.write("**Clause Text:**")
                st.write(r["text"])

                st.write("**Why this matters:**")
                st.write(r["ai_explanation"])

                st.write("**Suggested Safer Alternative:**")
                st.write(r["ai_suggestion"])
