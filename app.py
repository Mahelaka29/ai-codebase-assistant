import streamlit as st
import streamlit.components.v1 as components

from utils.zip_loader import extract_zip
from utils.parser import read_code_files
from utils.chunker import chunk_code
from utils.embeddings import create_embeddings, get_model
from utils.vector_store import build_vector_store, search
from utils.gemini import generate_answer
from utils.language_detector import detect_languages
from utils.file_tree import build_tree
from utils.file_viewer import show_source_code
from utils.project_summary import summarize_project
from utils.question_router import classify_question
from utils.local_answer import answer_local_question



def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


def render_upload_onboarding():
    st.markdown(
        """
        <div class="upload-onboarding-card">
            <h3>📦 Upload a Project to Get Started</h3>
            <ol>
                <li>Tap the <span class="sidebar-hint">☰ sidebar button</span> in the top-left.</li>
                <li>Upload your ZIP project.</li>
                <li>Wait for indexing.</li>
                <li>Start asking questions.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    components.html(
        """
        <div class="open-sidebar-wrap">
            <button id="open-sidebar-btn" type="button">Open Sidebar ↑</button>
        </div>
        <script>
            document.getElementById("open-sidebar-btn").addEventListener("click", function () {
                const doc = window.parent.document;
                const selectors = [
                    '[data-testid="stSidebarCollapsedControl"]',
                    '[data-testid="collapsedControl"]',
                    'button[kind="headerNoPadding"]'
                ];
                for (const selector of selectors) {
                    const control = doc.querySelector(selector);
                    if (control) {
                        control.click();
                        return;
                    }
                }
            });
        </script>
        """,
        height=56,
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

if "has_uploaded_project" not in st.session_state:
    st.session_state.has_uploaded_project = False

st.set_page_config(
    page_title="AI Codebase Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="auto" if st.session_state.has_uploaded_project else "expanded",
)

load_css()

st.title("AI Codebase Assistant")

st.caption(
    "Upload any software project and ask questions about its architecture, files, APIs, authentication, and business logic."
)

st.divider()

# ================= Sidebar =================

with st.sidebar:

    st.header("Project Explorer")

    uploaded_zip = st.file_uploader(
        "Upload Source Code (.zip)",
        type=["zip"]
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ================= Main =================

if uploaded_zip:

    st.session_state.has_uploaded_project = True

    extract_path = extract_zip(uploaded_zip)

    code_files = read_code_files(extract_path)

    summary = summarize_project(code_files)

    languages = detect_languages(code_files)
    tree = build_tree(code_files)

    if not code_files:
        st.error("No supported source files were found in the uploaded ZIP.")
        st.stop()

    with st.sidebar:

        st.divider()

        st.subheader("Project Files")

        with st.expander("Browse Files", expanded=False):

            for file in sorted(code_files, key=lambda x: x["path"]):
                st.text(file["path"])

    chunks = chunk_code(code_files)
    col1, col2, col3 = st.columns(3)

    col1.metric("Files Indexed", len(code_files), "Source files")
    col2.metric("Code Chunks", len(chunks))
    col3.metric("Project", uploaded_zip.name.replace(".zip", ""))

    st.subheader("Languages")

    cols = st.columns(min(len(languages), 4))

    for i, (lang, count) in enumerate(languages.items()):
        cols[i % 4].metric(lang, count)


    st.subheader("Project Overview")

    st.markdown(summary)

    st.divider()
    
    st.subheader("Project Structure")

    for folder, files in sorted(tree.items()):
        with st.expander(f"📁 {folder}", expanded=False):
            for file in sorted(files):
                st.code(file, language="text")

    embeddings = create_embeddings(chunks)
    index = build_vector_store(embeddings)

    model = get_model()


    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    if len(st.session_state.messages) == 0:

        st.markdown("## Welcome")

        st.write("Ask questions about any uploaded software project.")

        col1, col2 = st.columns(2)

        with col1:
            st.info("""
        **Suggested Questions**

        • Explain this project

        • Describe the architecture

        • Which frameworks are used?

        • Explain the folder structure
        """)

        with col2:
            st.info("""
        **More Questions**

        • How does authentication work?

        • Which files handle routing?

        • Explain the database layer

        • Which APIs are available?
        """)

    question = st.chat_input("Ask anything about this project...")

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        route = classify_question(question)

        st.write(f"Route: {route}")

        if route == "local":

            answer = answer_local_question(
                question=question,
                code_files=code_files,
                languages=languages,
                tree=tree
            )

            if answer:

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                with st.chat_message("assistant"):
                    st.markdown(answer)

                st.stop()

        results = search(
            index=index,
            model=model,
            chunks=chunks,
            query=question,
            k=5
        )

        if not results:
            st.warning("No relevant code was found for this question.")
            st.stop()

        context = ""

        sources = []

        for result in results:

            context += result["text"] + "\n\n"

            sources.append(result["source"])

        with st.spinner("Understanding the codebase..."):

            answer = generate_answer(
                question,
                context
            )

        unique_sources = sorted(set(sources))

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": unique_sources
        })

        best_score = max(result["score"] for result in results)

        st.caption(f"Search Confidence: {best_score:.2f}")

        with st.chat_message("assistant"):

            st.markdown(answer)

            if unique_sources:

                st.divider()
                st.caption("Referenced Files")

                for source in unique_sources:
                    show_source_code(code_files, source)

else:

    render_upload_onboarding()

    st.markdown(
"""
# Welcome

Upload a ZIP file containing a software project.

Once indexed, you can ask questions such as:

- Explain this project
- Describe the architecture
- Where is authentication implemented?
- Explain the database schema
- Which APIs are available?
"""
)