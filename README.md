# GRIP

<p align="center">
  <img src="Logo.png" alt="GRIP — Get a grip on your data" width="480">
</p>

**Get a grip on your codebase.**

A retrieval engine that learns your data's vocabulary, remembers what works, and tells the AI when it doesn't have a good answer.

[getgrip.dev](https://grip-hub.github.io/getgrip.dev/) | [PyPI](https://pypi.org/project/getgrip/) | [User Guide](./GUIDE.md) | [License](./LICENSE)

---

## Try it in 60 seconds

```bash
pip install getgrip

getgrip # starts web UI + API on localhost:7878
```

Then ingest and search:

```bash
curl -X POST localhost:7878/ingest \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/to/your/code"]}'

curl "localhost:7878/search?q=authentication+handler&top_k=5"
```

Or open `http://localhost:7878` and use the Browse button to add folders.

Open `http://localhost:7878` for the web UI.

---

## What makes GRIP different

Search "auth" — GRIP finds results containing "authentication", "OAuth", "JWT", "middleware" because it learned those terms co-occur in **your** data. No embedding model. No vector database. No API keys.

```
Query:    "confidence scoring"
Expanded: "confidence scoring heuristic percentil comput rerank"
Result:   [27.95] grip_retrieval/server.py:160 — the exact function
Latency:  1.4ms
```

| | Typical RAG | GRIP |
|---|---|---|
| Embedding model | Required | Not needed |
| Vector database | Required | Not needed |
| API keys | Required | Not needed |
| Learns your vocabulary | No | Yes — from your data |
| Remembers what works | No | Yes — across restarts |
| Knows when it doesn't know | No | Yes — confidence scoring |
| Works offline | Rarely | Fully air-gapped |
| Gets better with use | No | Yes — automatically |
| Cold start | Minutes (model loading) | < 2 seconds |
| Dependencies | 10-30+ | 4 (fastapi, uvicorn, pydantic, numpy) |

---

## Features

- **Co-occurrence expansion** — Learns which terms appear together in your data and expands queries automatically
- **Auto-remember** — Reinforces successful queries. Results improve with use
- **Session context** — "Tell me more" carries context from the previous query
- **Confidence scoring** — HIGH / MEDIUM / LOW / NONE. Your LLM knows when to say "I don't know"
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

Tested from 1,000 to 39.2 million documents. Streaming model R^2 = 0.999.

```
39,219,414 documents → 1.2ms per query (streaming shards)
BVH build: 14.9ms per 1M items
Sublinear: 39,219x data → 140x latency
```

### Cold vs Warm

```
Cold (first query):  7.7ms
Warm p50:            8.5ms
Deterministic:       YES — same query always returns same results
```

### Adversarial Robustness

Tested against degenerate queries (zero-match, 200-term floods, 50x duplicates), adversarial spatial distributions, and burst traffic (481K queries/sec).

Result: **PASS** — 14/15 tests pass, no crashes, no degradation under load.

Full benchmark logs: [`logs/`](./logs/)

### Real-World Accuracy

3,000 auto-generated queries across 3 domains. No cherry-picking.

| Domain | Corpus | Accuracy |
|--------|--------|----------|
| Linux Kernel (code) | 188,209 chunks | **98.7%** |
| Wikipedia (encyclopedia) | 11.2M chunks | **98.5%** |
| Project Gutenberg (prose) | 173,817 chunks | **95.4%** |
| **Combined** | **3,000 queries** | **97.5%** |

---

## Drop into your existing stack

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

## Optional extras

```bash
pip install getgrip[rerank]   # Cross-encoder reranking (MiniLM, 22M params)
pip install getgrip[pdf]      # PDF parsing
pip install getgrip[llm]      # LLM-powered answers (Ollama, OpenAI, Anthropic, Groq)
pip install getgrip[all]      # Everything
```

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

**Quick estimate:** Your text files x 3 = approximate chunks. See the [User Guide](./GUIDE.md#estimating-your-chunk-count) for detailed sizing.

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
