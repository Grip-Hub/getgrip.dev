# GRIP

<p align="center">
  <img src="Logo.png" alt="GRIP — Get a grip on your data" width="480">
</p>

**Get a grip on your data.**

A knowledge engine that learns your data's vocabulary, reads every document — including scanned pages and technical drawings — remembers what works, and tells the AI when it doesn't have a good answer.

[getgrip.dev](https://grip-hub.github.io/getgrip.dev/) | [PyPI](https://pypi.org/project/getgrip/) | [User Guide](./GUIDE.md) | [License](./LICENSE)

---

## Install

**Option A — pip (recommended)**

```bash
pip install getgrip

getgrip                        # starts web UI + API on localhost:7878
```

**Option B — Download from GitHub**

```bash
# Clone the repository
git clone https://github.com/Grip-Hub/getgrip.dev.git
cd getgrip.dev
pip install .

# Or download the zip directly (no git required)
# → https://github.com/Grip-Hub/getgrip.dev/archive/refs/heads/main.zip
```

**Option C — Docker**

```bash
docker run -d -p 7878:7878 \
  -v grip-data:/data \
  -v /your/files:/code \
  griphub/grip:free
```

**Option D — Download a release**

Pre-built packages are available on the [Releases](https://github.com/Grip-Hub/getgrip.dev/releases) page. Download the `.whl` or `.tar.gz` for your platform and install with:

```bash
pip install getgrip-<version>.whl
```

Then ingest and search:

```bash
curl -X POST localhost:7878/ingest \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/to/your/data"]}'

curl "localhost:7878/search?q=valve+specification&top_k=5"
```

Or open `http://localhost:7878` for the web UI.

---

## What makes GRIP different

GRIP doesn't search your documents. It **learns** them.

First query costs the full retrieval pass — every chunk, every document. That answer gets cached as a knowledge artifact. Second query on the same topic? Zero LLM calls, sub-millisecond. Similar question? One LLM call to adapt the cached knowledge. Your corpus gets smarter every time someone asks a question.

```
Query:    "valve specification for nitrogen piping"
Expanded: "valve specification nitrogen piping pressure rating material schedule"
Result:   Synthesized answer across 14 documents with citations
Cached:   Knowledge artifact stored — next query instant
```

| | Typical RAG | GRIP |
|---|---|---|
| Embedding model | Required | Not needed |
| Vector database | Required | Not needed |
| API keys | Required | Not needed |
| Reads scanned documents | No | Yes — OCR with confidence scoring |
| Reads technical drawings | No | Yes — visual captioning + rotation OCR |
| Learns your vocabulary | No | Yes — from your data |
| Remembers what works | No | Yes — knowledge artifacts |
| Knows when it doesn't know | No | Yes — confidence scoring |
| Detects stale answers | No | Yes — corpus versioning |
| Works offline | Rarely | Fully air-gapped |
| Gets better with use | No | Yes — automatically |

---

## Works With Your Data

GRIP reads everything. Not just clean PDFs — **everything**.

### 30+ File Formats

PDFs, Word docs (.docx), Excel (.xlsx/.xls), PowerPoint (.pptx), RTF, OpenDocument (ODS/ODT/ODP), CSV, Markdown, plain text, and all major code file types. One ingest command. No format conversion.

### Scanned Documents (OCR)

Scanned PDFs, photographed pages, faxed contracts — GRIP detects pages with no selectable text and automatically runs OCR. Three-tier engine fallback: PaddleOCR → RapidOCR → Tesseract. Per-page detection means mixed PDFs (some pages scanned, some digital) are handled transparently.

```bash
pip install getgrip[ocr]   # Apache-2.0 clean: pytesseract + Pillow
pip install getgrip[vision]      # Full visual pipeline: Florence-2 + OCR
```

### Technical Drawings & Diagrams

ISO drawings, P&IDs, schematics, architectural plans — GRIP doesn't just OCR the text labels. It **understands the drawing**.

Two parallel paths run on every visual page:
- **PaddleOCR with confidence-gated rotation** — detects text regions, reads them, and if confidence is low, rotates the patch through isometric angles (30°, 60°, 90°...) until confidence clears threshold. Catches angled dimension callouts, rotated spec text, vertical border labels.
- **Florence-2 visual captioning** — generates structural descriptions: "Isometric piping diagram showing utility water and nitrogen system with ball valve, check valve, and concentric swages." Makes drawings searchable by meaning, not just by text.

Both become searchable chunks in the same index as your text documents. Someone searching "check valve on the nitrogen line" finds the answer whether it came from a spec PDF or an ISO drawing.

### Confidence-Tagged OCR

Every OCR result carries a confidence score. High-confidence text is treated as authoritative. Low-confidence text is tagged `[OCR confidence: 45%]` so the synthesis engine treats it as approximate rather than definitive. Most systems either silently drop uncertain text or present it without qualification.

### Embedded Images

Images embedded inside PDFs and Word documents are extracted and captioned automatically. A spec sheet with an embedded assembly diagram produces text chunks from the prose AND visual description chunks from the diagram. Both are searchable.

---

## Knowledge Artifacts

GRIP's knowledge layer is what makes it a knowledge engine instead of a search engine.

**Exact hit** — Same question asked before? Zero LLM calls. Sub-millisecond. The cached synthesis is returned instantly with all citations.

**Similar match** — A related question was asked before? One LLM call adapts the cached knowledge to the new query. "What are the valve specs?" adapts a cached artifact from "What valves are on the nitrogen line?" — one call instead of a full retrieval pass.

**Stale detection** — Documents changed since the last answer? The artifact is flagged stale. Next query triggers a delta update that incorporates the changes without re-processing the entire corpus.

**Compounding intelligence** — Every question asked makes the system smarter. By month three, most queries resolve from cached artifacts. New employees get instant access to knowledge that took senior staff years to accumulate.

---

## Features

- **Co-occurrence expansion** — Learns which terms appear together in your data and expands queries automatically
- **Auto-remember** — Reinforces successful queries. Results improve with use
- **Session context** — "Tell me more" carries context from the previous query
- **Confidence scoring** — HIGH / MEDIUM / LOW / NONE. Your LLM knows when to say "I don't know"
- **Exhaustive synthesis** — Reads every chunk, not top-k. Nothing gets skipped
- **Knowledge artifacts** — Cached answers with stale detection and delta updates
- **Visual content pipeline** — OCR + captioning for scanned docs and technical drawings
- **Plugin system** — Sources (local, GitHub), chunkers (code-aware, generic), LLMs (Ollama, OpenAI, Anthropic)
- **API + Web UI** — 8 endpoints + directory browser, CORS-ready, FastAPI server
- **Fully offline** — No cloud. No telemetry. Your data stays on your machine (*API to LLMs excluded)

---

## Benchmarks

### BEIR (Industry Standard IR Benchmark)

Core engine — no neural components, no GPU, no reranker. 6 datasets, 21,708 queries, full query sets.

| Dataset | Corpus | Queries | NDCG@10 | Latency |
|---------|--------|---------|---------|---------|
| SciFact | 5,183 | 300 | **0.687** | 10.6ms |
| HotpotQA | 5,233,329 | 7,405 | **0.624** | 145.6ms |
| FEVER | 5,416,568 | 6,666 | **0.598** | 139.6ms |
| NFCorpus | 3,633 | 3,237 | **0.324** | 2.7ms |
| NQ | 2,681,468 | 3,452 | **0.310** | 68.5ms |
| FiQA | 57,638 | 648 | **0.243** | 7.5ms |
| **Average** | | **21,708** | **0.464** | |

For context: published BM25 baselines average 0.35-0.50 on this slice depending on implementation and tuning. Dense retrievers (DPR, E5) typically score 0.40-0.55. GRIP achieves this range with zero learned parameters.

Optional: `pip install getgrip[rerank]` adds a cross-encoder (MiniLM, 22M params) that bumps the average to ~0.58.

### Scaling

Tested from 1,000 to 39.2 million documents. Streaming model R² = 0.999.

```
39,219,414 documents → 1.2ms per query (streaming shards)
BVH build: 14.9ms per 1M items
Sublinear: 39,219x data → 140x latency
```

### Real-World Accuracy

3,000 auto-generated queries across 3 domains. No cherry-picking.

| Domain | Corpus | Accuracy |
|--------|--------|----------|
| Linux Kernel (code) | 188,209 chunks | **98.7%** |
| Wikipedia (encyclopedia) | 11.2M chunks | **98.5%** |
| Project Gutenberg (prose) | 173,817 chunks | **95.4%** |
| **Combined** | **3,000 queries** | **97.5%** |

---

## Who Uses GRIP

GRIP works with any corpus of documents, but it's especially powerful in industries where knowledge is trapped in large, messy document sets that nobody has time to read completely.

| Industry | What GRIP Does | Learn More |
|----------|---------------|------------|
| **Engineering & Construction** | Reads ISO drawings, P&IDs, valve specs, welding procedures. Synthesizes across IFC packages. Catches revision changes. | [→ Engineering](https://grip-hub.github.io/getgrip.dev/engineering) |
| **Legal** | Exhaustive review across discovery sets. Every document read, every clause cited. Staleness detection when case law changes. | [→ Legal](https://grip-hub.github.io/getgrip.dev/legal) |
| **Education & Research** | 500 papers → literature review with citations. Students synthesize sources without plagiarism. Researchers find what they're missing. | [→ Education & Research](https://grip-hub.github.io/getgrip.dev/education) |
| **Business & Operations** | 18 years of service manuals → instant answers for new hires. Supplier contracts, compliance reports, policy docs — all queryable. | [→ Business](https://grip-hub.github.io/getgrip.dev/business) |

---

## Drop Into Your Existing Stack

GRIP is a JSON API. Swap it into LangChain, LlamaIndex, or any RAG pipeline:

```python
from langchain.schema import BaseRetriever, Document
import requests

class GRIPRetriever(BaseRetriever):
    grip_url: str = "http://localhost:7878"
    top_k: int = 5

    def _get_relevant_documents(self, query):
        r = requests.get(f"{self.grip_url}/search", params={"q": query, "top_k": self.top_k})
        data = r.json()
        return [
            Document(
                page_content=chunk["text"],
                metadata={"source": chunk["source"], "score": chunk["score"],
                          "confidence": data["confidence"]}
            )
            for chunk in data["results"]
        ]
```

Replace Pinecone, Chroma, or any vector store. Your existing prompts, chains, and agents work unchanged.

See the [User Guide](./GUIDE.md#integrating-grip-into-your-application) for Python, JavaScript, CI/CD, LlamaIndex, and more integration examples.

---

## Optional Extras

```bash
pip install getgrip[pdf]        # PDF parsing
pip install getgrip[docs]       # All document formats (docx, xlsx, pptx, rtf, odt...)
pip install getgrip[ocr]  # OCR — Apache-2.0 clean (pytesseract + Pillow)
pip install getgrip[vision]     # Visual pipeline (Florence-2 captioning + OCR)
pip install getgrip[rerank]     # Cross-encoder reranking (MiniLM, 22M params)
pip install getgrip[llm]        # LLM-powered answers (Ollama, OpenAI, Anthropic, Groq)
pip install getgrip[all]        # Everything (commercially safe)
```

All extras are optional. Core retrieval works with zero extras installed.

---

## Pricing

The free tier includes **all features** with a 10,000 chunk limit (~3,500 files). No credit card. No time limit. Learned data resets when you delete a source — licensed tiers preserve it permanently.

| Tier | Chunks | Price | $/chunk/yr |
|------|--------|-------|-----------|
| **Free** | 10,000 | $0 | — |
| Personal | 100,000 | $499/year | $0.005 |
| Team | 500,000 | $1,499/year | $0.003 |
| Professional | 5,000,000 | $4,999/year | $0.001 |
| Enterprise | 25,000,000+ | [Contact us](mailto:getgrip.dev@gmail.com) | Custom |

One license per deployment. No per-seat fees. No per-query fees. Unlimited users. License validated locally — no phone-home.

**Quick estimate:** Your text files × 3 = approximate chunks. See the [User Guide](./GUIDE.md#estimating-your-chunk-count) for detailed sizing.

---

## Enterprise

An accelerated engine is available for organizations with large-scale retrieval needs.

**1.2ms at 28 million records. Single GPU.**

[getgrip.dev@gmail.com](mailto:getgrip.dev@gmail.com)

---

## Documentation

[User Guide](./GUIDE.md) — Installation, ingestion, searching, sessions, LLM integration, plugins, Docker, API reference, integration examples, troubleshooting

[License](./LICENSE) — Free tier for evaluation, licensed tiers for production

[getgrip.dev](https://grip-hub.github.io/getgrip.dev/) — Landing page with pricing and benchmarks

*RT (Real Time) is hardware dependent.
