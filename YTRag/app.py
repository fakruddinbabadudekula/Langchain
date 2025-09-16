# app.py
import os
import streamlit as st
from urllib.parse import urlparse, parse_qs
from utils import yttranscript_from_url
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub   # or OpenAI, etc.

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
# 2. Initialize Gemini 2.5 Pro
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.7,
)


# ----------------- Helpers -----------------

def get_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    return None


@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def get_or_create_vectorstore(url: str, chunk_size=1000, overlap=200):
    """Load FAISS if exists, else build and save it."""
    video_id = get_video_id(url)
    index_path = os.path.join("vectorstores", video_id)#Later we will save as video name instead of id

    if os.path.exists(index_path):
        vectors = FAISS.load_local(index_path, load_embeddings())
    else:
        transcript = yttranscript_from_url(url)
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        chunks = splitter.create_documents([transcript])
        vectors = FAISS.from_documents(chunks, load_embeddings())
        os.makedirs("vectorstores", exist_ok=True)
        vectors.save_local(index_path)

    return vectors


def get_qa_chain(vectorsdb):
    """Create a RetrievalQA chain for chatting with video."""
    retriever = vectorsdb.as_retriever(search_kwargs={"k": 3})
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


# ----------------- Streamlit UI -----------------

st.set_page_config(page_title="YouTube Chat App", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Video Chat App")
st.write("Paste a YouTube URL, fetch the transcript, and chat with it!")

if "vectorstores" not in st.session_state:
    st.session_state["vectorstores"] = {}

youtube_url = st.text_input("Enter YouTube Video URL:")

if st.button("Fetch Transcript"):
    if youtube_url:
        video_id = get_video_id(youtube_url)
        if not video_id:
            st.error("Invalid YouTube URL.")
        else:
            if video_id not in st.session_state["vectorstores"]:
                st.session_state["vectorstores"][video_id] = get_or_create_vectorstore(youtube_url)
            st.success(f"Transcript embedded for video: {video_id}")
    else:
        st.error("Please enter a valid YouTube URL.")

# If we already have vectorstores loaded
if st.session_state["vectorstores"]:
    st.subheader("💬 Chat with a video")

    # Let user pick which video to chat with
    video_choice = st.selectbox("Choose a video:", list(st.session_state["vectorstores"].keys()))

    user_query = st.text_input("Ask a question about the video:")

    if st.button("Get Answer"):
        if user_query:
            qa_chain = get_qa_chain(st.session_state["vectorstores"][video_choice])
            answer = qa_chain.run(user_query)
            st.success(answer)
        else:
            st.error("Please enter a question.")
