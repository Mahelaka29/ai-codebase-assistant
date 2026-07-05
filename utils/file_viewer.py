import streamlit as st

def show_source_code(code_files, source_path):
    for file in code_files:
        if file["path"] == source_path:

            with st.expander(f"📄 {source_path}", expanded=False):
                st.code(
                    file["content"],
                    language=source_path.split(".")[-1]
                )

            return