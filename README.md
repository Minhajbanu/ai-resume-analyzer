# 🚀 AI Resume Intelligence System (RAG-Based ATS)

An AI-powered Resume Analyzer that evaluates resume-job compatibility using:

- 🔎 Semantic Similarity (Embeddings + FAISS)
- 📊 ATS Keyword Scoring
- 🧠 Skill Gap Detection
- 🤖 LLM-based Intelligent Analysis
- 🔐 User Authentication System

This system combines rule-based scoring and LLM reasoning to simulate real-world AI-driven Applicant Tracking Systems (ATS).

---

## 🎯 Key Features

✅ Resume PDF Parsing  
✅ Resume Chunking & Embedding Generation  
✅ FAISS Vector Search (Top Relevant Resume Context)  
✅ Semantic Similarity Score  
✅ ATS Keyword Match Score  
✅ Skill Match Percentage  
✅ Missing Skills Identification  
✅ LLM-based Detailed Resume Evaluation  
✅ Login & Signup System (bcrypt-secured)  
✅ Interactive Dashboard (Plotly Graphs)  

---

## 🧠 System Architecture

### 🔹 Processing Flow

1. Resume PDF → Text Extraction  
2. Text → Chunking  
3. Chunks → Embeddings  
4. FAISS → Retrieve Most Relevant Context  
5. Semantic Similarity Calculation  
6. ATS Keyword Matching  
7. Skill Extraction & Gap Detection  
8. LLM → Intelligent Analysis Explanation  

---

### 🔹 Hybrid Scoring Formula

Final Score is calculated using:

Final Score = 0.6 × Semantic Score + 0.4 × Keyword Score

Where:

- Semantic Score = Cosine Similarity between Resume & Job Embeddings
- Keyword Score = Rule-based ATS keyword overlap percentage

Cosine Similarity formula:

cos(θ) = (A · B) / (||A|| ||B||)

---

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **FAISS**
- **Sentence Transformers**
- **Ollama (Local LLM)**
- **matplotlib**
- **SQLite**
- **bcrypt**

---

## 💡 Why This Project is Unique

Unlike traditional ATS systems that rely only on keyword matching, this project:

✔ Uses semantic understanding through embeddings  
✔ Implements Retrieval-Augmented Generation (RAG)  
✔ Combines rule-based scoring with LLM reasoning  
✔ Detects skill gaps intelligently  
✔ Provides explainable AI feedback  

---

