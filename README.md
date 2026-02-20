# GRIP

<p align="center">
  <img src="Logo.png" alt="GRIP — Get a grip on your data" width="480">
</p>

**Get a grip on your codebase.**

A retrieval engine that learns your data's vocabulary, remembers what works, and tells the AI when it doesn't have a good answer.

🌐 [getgrip.dev](https://grip-hub.github.io/getgrip.dev/) · 📦 [PyPI](https://pypi.org/project/getgrip/) · 📖 [User Guide](./GUIDE.md) · 📄 [License](./LICENSE)

---

## Try it in 60 seconds

```bash
pip install getgrip
grip ingest --source /path/to/your/code
grip search "authentication handler"
```

Or with Docker:

```bash
docker run -d -p 7878:8000 -v grip-data:/data -v /your/code:/code griphub/grip:free
curl -X POST localhost:7878/ingest -H "Content-Type: application/json" -d '{"source": "/code"}'
curl "localhost:7878/search?q=authentication+handler&top_k=5"
```

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

---

## Features

- **Co-occurrence expansion** — Learns which terms appear together in your data and expands queries automatically
- **Auto-remember** — Reinforces successful queries. Results improve with use
- **Session context** — "Tell me more" carries context from the previous query
- **Confidence scoring** — HIGH / MEDIUM / LOW / NONE. Your LLM knows when to say "I don't know"
- **Plugin system** — Sources (local, GitHub), chunkers (code-aware, generic), LLMs (Ollama, OpenAI, Anthropic)
- **CLI + API + Web UI** — 9 endpoints, CORS-ready, FastAPI server
- **Fully offline** — No cloud. No telemetry. Your data stays on your machine

---

## Benchmarks

### BEIR (Industry Standard)

6 datasets. 2,771 queries. Beats BM25 on all 6.

| Dataset | Corpus | BM25 | GRIP | Delta |
|---------|--------|------|------|-------|
| FEVER | 5,416,568 | 0.509 | **0.808** | +0.299 |
| HotpotQA | 5,233,329 | 0.595 | **0.741** | +0.146 |
| SciFact | 5,183 | 0.665 | **0.682** | +0.017 |
| NQ | 2,681,468 | 0.276 | **0.542** | +0.266 |
| FiQA | 57,638 | 0.232 | **0.347** | +0.116 |
| NFCorpus | 3,633 | 0.311 | **0.344** | +0.034 |

**Average NDCG@10: 0.58**

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
        r = requests.post(f"{self.grip_url}/search", json={"q": query, "top_k": self.top_k})
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

## Pricing

The free tier includes **all features** with a 10,000 chunk limit (~3,500 files). No credit card. No time limit. Learned data resets when you delete a source — licensed tiers preserve it permanently.

| Tier | Chunks | Price | $/chunk/yr |
|------|--------|-------|-----------|
| **Free** | 10,000 | $0 | — |
| Personal | 100,000 | $499/year | $0.005 |
| Team | 500,000 | $1,499/year | $0.003 |
| Professional | 5,000,000 | $4,999/year | $0.001 |
| Enterprise | 25,000,000+ | [Contact us](mailto:getgrip.dev@gamil.com) | Custom |

One license per deployment. No per-seat fees. No per-query fees. Unlimited users. License validated locally — no phone-home.

**Quick estimate:** Your text files × 3 = approximate chunks. See the [User Guide](./GUIDE.md#estimating-your-chunk-count) for detailed sizing.

---

## Enterprise

An accelerated engine is available for organizations with large-scale retrieval needs.

**1.2ms at 28 million records. Single GPU.**

[enterprise@getgrip.dev](mailto:getgrip.dev@gamil.com)

---

## Documentation

📖 **[User Guide](./GUIDE.md)** — Installation, ingestion, searching, sessions, LLM integration, plugins, Docker, API reference, integration examples, troubleshooting

📄 **[License](./LICENSE)** — Free tier for evaluation, licensed tiers for production

🌐 **[getgrip.dev](https://grip-hub.github.io/getgrip.dev/)** — Landing page with pricing and benchmarks
