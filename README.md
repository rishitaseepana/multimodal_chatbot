# Multimodal RAG Chatbot
A Multimodal Retrieval-Augmented Generation (RAG) chatbot built using **Streamlit**, **LangChain**, **FAISS**, **CLIP**, and **Groq**. The chatbot allows users to upload documents, indexes text, tables, and images, and answers questions using only the retrieved information from the uploaded documents.
---
# Features
- Upload and index multiple document formats
 - PDF
 - DOCX
 - PPTX
 - TXT
- Text extraction and chunking
- Table extraction and conversion to text
- Automatic table storage as `.txt` files
- Image extraction from PDF, DOCX, and PPTX
- CLIP-based image embeddings
- Hugging Face text embeddings
- Separate FAISS databases for text and images
- Persistent local vector database
- Incremental indexing (only new documents are indexed)
- Delete individual indexed documents
- Clear the complete database
- Session-based chat history
- Retrieve relevant text and images
- Answer questions using Groq LLM
- Local storage of embeddings and metadata
---
# Project Structure
```text
multimodal_rag/
│
├── app.py
├── rag_utils.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── uploads/
│   └── images/
│
├── vector_db/
│
├── image_db/
│
├── tables/
│
└── metadata/
```
---
# Installation
## Clone the repository
```bash
git clone <repository_url>
cd multimodal_rag
```
## Create a virtual environment
```bash
python -m venv .venv
```
## Activate the environment
### Windows
```bash
.venv\Scripts\activate
```
### Linux / macOS
```bash
source .venv/bin/activate
```
## Install dependencies
```bash
pip install -r requirements.txt
```
---
# Environment Variables
Create a `.env` file in the project directory.
```env
GROQ_API_KEY=your_groq_api_key
```
---
# Running the Application
```bash
streamlit run app.py
```
---
# How It Works
1. Upload one or more supported documents.
2. Click **Index Files**.
3. Previously indexed files are skipped automatically.
4. Text is extracted and split into chunks.
5. Tables are converted to text and stored locally.
6. Images are extracted and embedded using CLIP.
7. Text and image embeddings are stored in local FAISS databases.
8. Ask questions about the uploaded documents.
9. The chatbot retrieves the most relevant text and images.
10. Groq generates an answer using only the retrieved context.
---
# Technologies Used
- Python
- Streamlit
- LangChain
- FAISS
- Hugging Face Embeddings
- CLIP (OpenAI)
- Groq
- PyMuPDF
- python-docx
- python-pptx
- NumPy
- Pillow
---
# Supported File Types
| File Type | Text | Tables | Images |
|-----------|------|--------|--------|
| PDF | ✅ | ✅ | ✅ |
| DOCX | ✅ | ✅ | ✅ |
| PPTX | ✅ | Limited | ✅ |
| TXT | ✅ | ❌ | ❌ |
---
# Storage
The application stores data locally to avoid re-indexing previously processed files.
- Uploaded documents
- Text vector database
- Image vector database
- Image metadata
- Indexed file metadata
- Extracted table text files
---
# Limitations
- Image retrieval is based on CLIP embeddings.
- For questions based on images it shows accurate retrieved images but cannot answer based on it.
- Answers are generated only from retrieved document content.
- Chat history is maintained only for the current session.
- No internet search is performed.
---
# License
This project is intended for educational and learning purposes.
