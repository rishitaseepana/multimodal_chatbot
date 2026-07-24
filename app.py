import streamlit as st
from rag_utils import RAG
from rag_utils import GROQ_API_KEY
import uuid

st.set_page_config(
   page_title="Multimodal RAG",
   layout="wide"
)
st.title("Multimodal RAG Chatbot")

GROQ_API_KEY

@st.cache_resource
def load_rag():
    return RAG() 

rag = load_rag()

uploaded_files = st.file_uploader(
   "Upload PDF, DOCX, PPTX or TXT files",
   type=["pdf", "docx", "pptx", "txt"],
   accept_multiple_files=True
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if uploaded_files:
   if st.button("Index Files"):
            files_to_index = []
            for uploaded_file in uploaded_files:
                path = rag.storage.save_uploaded_file(
                    uploaded_file
                )
                if rag.storage.is_new_file(path):
                    files_to_index.append(path)
            if files_to_index:
                rag.index_files(files_to_index)
                st.success(
                    f"Indexed {len(files_to_index)} new file(s)."
                )
            else:
                st.info(
                        "All selected files are already indexed."
                    )

st.sidebar.title("Database")

if st.sidebar.button("Clear Database"):
   rag.clear_database()
   st.sidebar.success("Database cleared.")

files = rag.storage.get_uploaded_files()
if files:
   selected = st.sidebar.selectbox(
       "Delete File",
       files
   )
   if st.sidebar.button("Delete Selected File"):
       rag.delete_file(selected)
       st.sidebar.success(
           f"{selected} deleted."
       )

query = st.text_input(
   "Ask a question"
)

if st.button("Ask"):
   if not query.strip():
       st.warning("Enter a question.")
   else:
       with st.spinner("Generating answer..."):
           result = rag.ask(query)
       if result["cached"]:
        st.info("Answer retrieved from chat memory.")
       st.subheader("Answer")
       st.write(result["answer"])

       if result["text"]:
           with st.expander("Retrieved Chunks"):
               for i, doc in enumerate(result["text"], 1):
                   st.markdown(
                       f"### Chunk {i}"
                   )
                   st.write(doc.page_content)
                   st.caption(
                       doc.metadata
                   )

       if result["images"]:
           with st.expander("Retrieved Images"):
               for image in result["images"]:
                   st.image(
                       image["path"],
                       caption=image["file"],
                       use_container_width=True
                   )

st.sidebar.title("Chat History")
history = rag.storage.get_session_history(
   st.session_state.session_id
)
for i, chat in enumerate(history, 1):
   with st.sidebar.expander(
       chat["question"]
   ):
       st.write(
           "**Question**"
       )
       st.write(
           chat["question"]
       )
       st.write(
           "**Answer**"
       )
       st.write(
           chat["answer"]
       )
