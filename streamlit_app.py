
import os
import json
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Ensure local imports work even without `pip install -e .`
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(THIS_DIR, "src")
if SRC_DIR not in os.sys.path:
    os.sys.path.insert(0, SRC_DIR)

from hipporag.course_resolver import CourseResolver
from hipporag.utils.config_utils import BaseConfig
from hipporag.StandardRAG import StandardRAG
from hipporag.HippoRAG import HippoRAG

load_dotenv()

def env(key: str, default: str = "") -> str:
    v = os.getenv(key)
    return default if v is None or str(v).strip() == "" else str(v).strip()

# ---- Unified defaults (NO mapping-only UI; this UI answers questions) ----
# IMPORTANT: E5/XLM-R family supports up to 512 tokens; clamp here too.
E5_MAX_SEQ_LEN = min(int(env("E5_MAX_SEQ_LEN", "512")), 512)

DEFAULTS = {
    "OPENAI_MODEL": env("OPENAI_MODEL", "gpt-4o"),
    "E5_MODEL": env("E5_MODEL", "intfloat/multilingual-e5-large"),
    "E5_DEVICE": env("E5_DEVICE", "cuda"),
    "E5_DTYPE": env("E5_DTYPE", "float32"),
    "E5_BATCH": int(env("E5_BATCH", "4")),
    "E5_MAX_SEQ_LEN": E5_MAX_SEQ_LEN,
    "INDEX_ROOT": env("INDEX_ROOT", "./outputs"),
    "CATALOG_PATH": env("CATALOG_PATH", "./catalog.json"),
    "COURSE_THRESHOLD": float(env("COURSE_THRESHOLD", "0.80")),
    "COURSE_MARGIN": float(env("COURSE_MARGIN", "0.02")),
    "CORPUS_DS": env("CORPUS_DS", "./data_processing_pipeline/outputs/DS_corpus.json"),
    "CORPUS_MCS": env("CORPUS_MCS", "./data_processing_pipeline/outputs/MCS_corpus.json"),
    "CORPUS_AM": env("CORPUS_AM", "./data_processing_pipeline/outputs/AM_corpus.json"),
}

MAJORS = {
    "DS": DEFAULTS["CORPUS_DS"],
    "MCS": DEFAULTS["CORPUS_MCS"],
    "AM": DEFAULTS["CORPUS_AM"],
}

def load_corpus(path: str):
    path = str(Path(path))
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_text_chars(text: str, max_chars: int = 1200, overlap: int = 100):
    text = (text or "").strip()
    if not text:
        return []
    step = max(1, max_chars - overlap)
    return [text[i:i+max_chars] for i in range(0, len(text), step)]

def docs_from_corpus(corpus, chunk_chars: int = 1200, overlap: int = 100):
    docs = []
    for d in corpus:
        title = d.get("title", "")
        txt = d.get("text", "")
        for part in chunk_text_chars(txt, max_chars=chunk_chars, overlap=overlap):
            docs.append(f"Course ID: {title}\n{part}")
    return docs

def build_config(save_dir: str, engine: str) -> BaseConfig:
    # Both StandardRAG and HippoRAG accept BaseConfig in this repo.
    # Keep indicative knobs small for GTX 1070 Ti.
    return BaseConfig(
        llm_name=DEFAULTS["OPENAI_MODEL"],
        embedding_model_name=DEFAULTS["E5_MODEL"],
        embedding_model_dtype=DEFAULTS["E5_DTYPE"],
        embedding_batch_size=DEFAULTS["E5_BATCH"],
        embedding_max_seq_len=DEFAULTS["E5_MAX_SEQ_LEN"],
        retrieval_top_k=50,
        qa_top_k=5,
        save_dir=save_dir,
        force_index_from_scratch=False,
    )

@st.cache_resource
def get_resolver():
    return CourseResolver(
        catalog_path=DEFAULTS["CATALOG_PATH"],
        threshold=DEFAULTS["COURSE_THRESHOLD"],
        margin=DEFAULTS["COURSE_MARGIN"],
    )

@st.cache_resource
def get_engine(engine: str, major: str):
    save_dir = os.path.join(DEFAULTS["INDEX_ROOT"], f"{engine}_{major}")
    cfg = build_config(save_dir=save_dir, engine=engine)
    if engine == "HippoRAG":
        return HippoRAG(global_config=cfg)
    return StandardRAG(global_config=cfg)

def index_ready(obj) -> bool:
    # Do NOT call obj.retrieve(...) here (HippoRAG may not have passage embeddings yet).
    try:
        id2row = obj.chunk_embedding_store.get_all_id_to_rows()
        return bool(id2row) and len(id2row) > 0
    except Exception:
        return False

def ensure_index(obj, docs, rebuild: bool) -> str:
    if rebuild:
        # wipe directory for safety
        try:
            sd = getattr(obj.global_config, "save_dir", None)
            if sd and os.path.isdir(sd):
                # remove only known index artifacts; keep folder
                for name in os.listdir(sd):
                    p = os.path.join(sd, name)
                    if os.path.isfile(p):
                        os.remove(p)
        except Exception:
            pass
        obj.index(docs)
        return "Rebuilt index from scratch"

    if index_ready(obj):
        return "Index is available"

    obj.index(docs)
    return "Index not found : built now"

st.set_page_config(page_title="HCMUS QA ", layout="wide")
st.title("HCMUS QA (E5 + GPT 4o)")

with st.sidebar:
    st.header("Settings")
    major = st.selectbox("Major corpus", list(MAJORS.keys()), index=0)
    engine = st.selectbox("Engine", ["StandardRAG", "HippoRAG"], index=0)
    use_resolver = st.checkbox("Use course resolver", value=True)
    rebuild = st.checkbox("Rebuild index", value=False)
    chunk_chars = st.slider("Chunk size", min_value=300, max_value=2000, value=500, step=10)
    overlap = st.slider("Chunk overlap", min_value=0, max_value=400, value=50, step=10)

corpus_path = MAJORS[major]
corpus = load_corpus(corpus_path)
docs = docs_from_corpus(corpus, chunk_chars=chunk_chars, overlap=overlap)

obj = get_engine(engine, major)
st.info(ensure_index(obj, docs, rebuild))

question = st.text_area("Chào mày, hỏi đi :", height=120, placeholder="VD: môn Tieng Anh 1 học gì? điều kiện qua môn?")
ask = st.button("Hỏi")

def augment_query(q: str) -> str:
    if not use_resolver:
        return q
    resolver = get_resolver()
    try:
        out = resolver.resolve(q)
        canonical_note = out.get("canonical_note", "")
        if canonical_note:
            return q + "\n\n" + canonical_note
    except Exception:
        pass
    return q

if ask and question.strip():
    q_final = augment_query(question.strip())

    with st.spinner("Retrieving..."):
        t0 = time.time()
        sols = obj.retrieve([q_final], num_to_retrieve=50)
        t1 = time.time()

    with st.spinner("Answering..."):
        sols, raw_msgs, meta = obj.qa(sols)
        t2 = time.time()

    st.subheader("Answer")
    st.write(sols[0].answer if hasattr(sols[0], "answer") else str(sols[0]))

    st.caption(f"Retrieve: {t1-t0:.2f}s | QA: {t2-t1:.2f}s | Engine: {engine} | Major: {major}")

    st.subheader("Top 5 retrieved")
    top_docs = getattr(sols[0], "docs", [])[:5]
    for i, d in enumerate(top_docs, 1):
        st.markdown(f"**{i}.** {d[:400]}{'...' if len(d)>400 else ''}")
