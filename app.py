import streamlit as st
import os
import tempfile
from src.profiler import ExcelProfiler
from src.router import GroqRouter
from src.planner import SchemaPlanner

st.set_page_config(page_title="Data Eng Copilot", layout="wide")

# Ensure API Key is available
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = st.secrets.get("GROQ_API_KEY", "")

st.title("Data Engineering Agent (Version 1)")

uploaded_file = st.file_uploader("Upload messy XLSX file", type=["xlsx"])

if uploaded_file:
    # Save to ephemeral storage for openpyxl/duckdb processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    st.success("File uploaded successfully.")

    if st.button("Analyze & Propose Schema"):
        with st.spinner("Profiling workbook topology (Deterministic)..."):
            # 1. Deterministic Profiling
            profiler = ExcelProfiler()
            profile_data = profiler.profile_workbook(tmp_path)
            st.json(profile_data)
        
        with st.spinner("Classifying Intent (Groq 8B)..."):
            # 2. Intent Routing
            router = GroqRouter()
            intent = router.route_intent("Analyze this newly uploaded file and suggest a better structure.")
            st.info(f"Detected Intent: {intent}")
            
        with st.spinner("Designing Schema (Groq 70B)..."):
            # 3. Schema Planning
            planner = SchemaPlanner()
            schema_proposal = planner.propose_schema(profile_data)
            st.markdown("### Proposed Data Structure")
            st.markdown(schema_proposal)
            
    # Cleanup temp file
    os.remove(tmp_path)
