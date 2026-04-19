# Project Detailed Documentation (Word-Ready)

## 1) Document Purpose

This document provides a complete **functional** and **technical** specification for the project: **LLM-Powered Analytics Assistant with RAG**. It is written in a format that can be copied directly into Microsoft Word as a project report.

---

## 2) Project Overview

### 2.1 Project Name
LLM-Powered Analytics Assistant with RAG

### 2.2 Problem Statement
Business stakeholders often need insights from both:
- Structured transactional data (orders, revenue, customers)
- Unstructured customer feedback (reviews and complaints)

Traditional workflows require separate tools and technical skills (SQL, BI tools, text analytics). This project provides one natural-language interface for both.

### 2.3 Project Objective
To enable users to ask natural-language business questions and receive:
- SQL-grounded quantitative metrics
- Review-grounded qualitative insights
- Hybrid answers combining both

### 2.4 Scope
The current scope is optimized for the Olist e-commerce dataset and common analytics intents (sales trends, category performance, delivery issues, sentiment, complaints).

---

## 3) Functional Documentation

## 3.1 Core Functional Capabilities

### F1. Natural Language Query Input
Users ask business questions in plain language through a Streamlit chat interface.

### F2. Intelligent Query Routing
Each query is classified into one of four routes:
- `SQL`
- `RAG`
- `HYBRID`
- `UNKNOWN`

### F3. SQL Analytics Path
For structured questions:
1. Generate SQL from user question
2. Sanitize/repair SQL for SQLite
3. Execute query against the database
4. Return table + chart + summary

### F4. RAG Review Insights Path
For feedback-focused questions:
1. Retrieve top-k relevant review chunks using embeddings
2. Translate/clean snippets when needed
3. Detect sentiment
4. Extract themes/complaints
5. Synthesize business-friendly answer

### F5. Hybrid Analysis Path
For mixed questions requiring metrics + feedback:
1. Split into SQL sub-question and RAG sub-question
2. Run both pipelines independently
3. Produce a combined grounded answer

### F6. Conversation and UX Features
- Prompt cards for common business questions
- Chat history in UI session
- Tabular outputs and visualization support

### F7. Runtime Asset Bootstrapping
If key assets are missing locally (database/index/chunks), the system can download them from configured URLs (useful for cloud deployments).

## 3.2 Functional User Stories

1. **As a business analyst**, I want to ask “Top categories by revenue” and get an immediate ranked answer with chart.
2. **As a CX manager**, I want to ask “What are customers complaining about in delivery?” and get themes and sentiment.
3. **As an operations lead**, I want to ask “Which high-selling categories have poor customer sentiment?” and get a combined hybrid insight.

## 3.3 Inputs and Outputs

### Inputs
- Natural-language user query
- Runtime assets (SQLite DB, FAISS index, review chunks)
- Optional runtime environment variables (`OLLAMA_URL`, `OLLAMA_MODEL`, asset URLs)

### Outputs
- Route decision (`SQL`/`RAG`/`HYBRID`/`UNKNOWN`)
- Structured tables (DataFrame view)
- Plotly charts (line/bar/pie where relevant)
- Narrative answer with grounded supporting signals

## 3.4 Functional Limitations
- Optimized for known Olist schema and common intents
- Not a fully general-purpose autonomous analytics engine
- Some complex intents rely on deterministic fallback SQL templates for reliability

---

## 4) Technical Documentation

## 4.1 Technology Stack
- **Language:** Python
- **UI:** Streamlit
- **Structured data engine:** SQLite + pandas
- **Visualization:** Plotly
- **Retrieval:** FAISS + sentence-transformers
- **LLM runtime:** Ollama-compatible API (with fallback behavior)

## 4.2 High-Level Architecture

### Layer A: Presentation
- `app.py`
- Handles user interaction, routing invocation, and rendering.

### Layer B: Control / Routing
- `router/query_router.py`
- Determines best execution path (`SQL`, `RAG`, `HYBRID`, `UNKNOWN`).

### Layer C1: Structured Analytics Engine
- `sql/nl_to_sql.py`
- `sql/executor.py`
- Responsible for SQL generation, sanitation, repair, execution, and stable caching.

### Layer C2: Retrieval-Augmented Insights Engine
- `rag/retriever.py`
- `rag/translator.py`
- `rag/sentiment_analysis.py`
- `rag/theme_extractor.py`
- `rag/synthesizer.py`
- Responsible for retrieval, enrichment, and evidence-grounded synthesis.

### Layer D: Visualization
- `visualization/chart_generator.py`
- Selects chart type based on output schema and metrics.

## 4.3 Detailed Pipeline Flows

### SQL Pipeline
1. Query router classifies request as SQL
2. NL prompt sent to LLM SQL generator
3. SQL normalization and safety cleanup
4. Query execution in SQLite
5. Result summary generation
6. Data + chart rendering

### RAG Pipeline
1. Query router classifies request as RAG
2. Query embedding generated
3. Top-k chunks retrieved from FAISS
4. Translation/normalization
5. Sentiment + theme extraction
6. Answer synthesis based on retrieved evidence

### Hybrid Pipeline
1. Query router classifies request as HYBRID
2. Query decomposition into two sub-questions
3. SQL and RAG branches run
4. Joint synthesis of structured and unstructured findings

## 4.4 Data and Asset Dependencies
Required runtime files:
- `data/ecommerce.db`
- `rag/faiss_index.bin`
- `rag/review_chunks.pkl`

Cloud-friendly configuration via environment/secrets:
- `ECOMMERCE_DB_URL`
- `FAISS_INDEX_URL`
- `REVIEW_CHUNKS_URL`

## 4.5 Reliability and Stability Mechanisms
- SQL sanitization for SQLite compatibility
- SQL repair routines for malformed model outputs
- Deterministic query templates for recurring high-value intents
- Persistent validated SQL cache for repeat stability
- LLM fallback behavior for unavailable model runtime

## 4.6 Non-Functional Characteristics

### Performance
- Query response depends on LLM runtime latency and retrieval/index size
- Structured SQL answers are generally faster than generation-heavy hybrid responses

### Availability
- Local-first architecture can run without external cloud LLM if Ollama is available
- Graceful fallback mode supports degraded-but-usable operation

### Maintainability
- Modular package structure (`sql`, `rag`, `router`, `visualization`)
- Clear separation of pipeline responsibilities

### Portability
- Runs locally and on Streamlit-compatible deployment platforms
- Asset bootstrap path enables cloud startup with minimal manual provisioning

---

## 5) Security, Risk, and Governance Notes

### 5.1 Security Considerations
- Validate and sanitize generated SQL before execution
- Restrict data source scope to expected schema in production
- Keep secrets in environment/secret stores (not in source control)

### 5.2 Risks
- Model hallucination risk in free-form language responses
- Misrouting edge cases for ambiguous queries
- Dependency on quality/coverage of indexed review chunks

### 5.3 Mitigations
- Ground answers in SQL execution and retrieved review evidence
- Maintain deterministic fallback templates for key use-cases
- Add explicit uncertainty handling for low-confidence retrieval scenarios

---

## 6) Testing and Validation Approach

### 6.1 Functional Tests
- Route classification tests for SQL/RAG/HYBRID
- SQL generation and execution checks for known business prompts
- Retrieval relevance checks for common complaint categories
- Hybrid decomposition and synthesis verification

### 6.2 Technical Tests
- Module-level tests (example: visualization tests)
- Smoke test for app startup and required assets
- Runtime fallback tests (LLM unavailable scenario)

### 6.3 Acceptance Criteria
- Correct route selected for representative prompt families
- No SQL syntax errors for key business queries
- RAG answers include review-grounded themes and sentiment
- Hybrid responses include both quantitative and qualitative findings

---

## 7) Deployment and Operations

### 7.1 Local Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Ensure Ollama model runtime (optional but recommended)
3. Run app: `streamlit run app.py`

### 7.2 Cloud Deployment
- Deploy code repository
- Configure asset URLs in secure secrets/config
- Allow startup bootstrap to materialize missing runtime files

### 7.3 Operational Runbook (Recommended)
- Monitor failed query classes and add templates for high-frequency failures
- Log route decisions for tuning classification quality
- Periodically refresh FAISS index/chunks as data evolves

---

## 8) Future Enhancements

1. Role-aware access control and audit logs
2. Confidence scoring with explicit evidence citations per answer
3. Multi-dataset support beyond Olist schema
4. Scheduled index rebuild and drift monitoring
5. Dashboard export to Word/PDF/PowerPoint formats

---

## 9) Appendix: Suggested Word Formatting

To convert this into a formal Word report:
- Heading 1: major sections (1,2,3...)
- Heading 2/3: subsections
- Use table styles for Functional Requirements and Test Matrix
- Add architecture diagram image from project artifacts if available
- Add title page with version, author, and date

**Document Version:** 1.0  
**Prepared On:** 2026-04-19
