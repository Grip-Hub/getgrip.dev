# GRIP

**Get a grip on your codebase.**

A retrieval engine that learns your data's vocabulary, remembers what works, and tells the AI when it doesn't have a good answer.

```bash
pip install getgrip
```

---

## What is GRIP?

Most retrieval systems are stateless — query in, results out, everything forgotten. GRIP is different.

- **Co-occurrence expansion** — Search "auth" and GRIP finds "authentication", "OAuth", "middleware" because it learned those terms co-occur in *your* data. No external model. No API call.
- **Auto-remember** — Queries that return good results are reinforced. The system gets better every time you use it. Persistent across restarts.
- **Session context** — Say "tell me more" and GRIP knows what you were just searching for. Retrieval with conversational memory.
- **Confidence scoring** — Results scored HIGH / MEDIUM / LOW / NONE. The LLM knows when to say "I don't know" instead of hallucinating.
- **Fully offline** — No cloud. No network. No telemetry. Works air-gapped. Your data stays on your machine.

No embedding model required. No vector database required. No API keys for core retrieval.

---

## Quick Start

```bash
# Install
pip install getgrip

# Ingest your codebase
grip ingest --source /path/to/your/code

# Search it
grip search "authentication handler"

# Ask questions (requires Ollama or OpenAI-compatible LLM)
grip ask "how does the auth middleware work?"
```

---

## Benchmarks

### BEIR (Industry Standard)

6 datasets. 2,771 queries. Corpora from 3K to 5.4M documents.

| Dataset | Corpus | BM25 | GRIP | Delta |
|---------|--------|------|------|-------|
| FEVER | 5,416,568 | 0.509 | **0.808** | +0.299 |
| HotpotQA | 5,233,329 | 0.595 | **0.741** | +0.146 |
| SciFact | 5,183 | 0.665 | **0.682** | +0.017 |
| NQ | 2,681,468 | 0.276 | **0.542** | +0.266 |
| FiQA | 57,638 | 0.232 | **0.347** | +0.116 |
| NFCorpus | 3,633 | 0.311 | **0.344** | +0.034 |

**Average NDCG@10: 0.58** — Beats BM25 on all 6 datasets.

Two-stage pipeline: retrieval narrows candidates, then a pluggable neural reranker (MiniLM, 22M params) does semantic scoring. Swap in a better reranker and quality goes up. Retrieval cost stays the same.

### Accuracy at Scale

3,000 auto-generated queries. No hand-curation. No cherry-picking.

| Domain | Corpus | Queries | Accuracy |
|--------|--------|---------|----------|
| Linux Kernel (code) | 188,209 chunks | 1,000 | **98.7%** |
| Wikipedia (encyclopedia) | 11.2M chunks | 1,000 | **98.5%** |
| Project Gutenberg (prose) | 173,817 chunks | 1,000 | **95.4%** |
| **Combined** | | **3,000** | **97.5%** |

---

## What's Included

- BM25 retrieval engine with Porter stemming
- Co-occurrence expansion (learns from your data)
- Auto-remember (reinforces successful queries)
- Session continuity (conversational retrieval)
- Confidence scoring (HIGH / MEDIUM / LOW / NONE)
- Plugin system — sources, chunkers, LLMs, analyzers
- CLI + FastAPI server (8 endpoints, CORS-ready)
- Ollama and OpenAI-compatible LLM plugins
- GitHub and local source ingestion plugins
- Code-aware and generic chunking plugins

---

## Free Demo Limits

The free `pip install` package includes all features with a **10,000 chunk limit**. No license key required. No time limit. Chunks can be deleted and replaced, but learned data (co-occurrence, remember scores) resets on deletion. Licensed tiers preserve learning permanently.

Need more? See [Pricing](https://getgrip.dev/#pricing).

---

## Licensed Tiers

| Tier | Chunks | Price |
|------|--------|-------|
| Personal | 100,000 | $499/year |
| Team | 500,000 | $1,499/year |
| Professional | 5,000,000 | $4,999/year |
| Enterprise | 25,000,000+ | [Contact us](mailto:enterprise@getgrip.dev) |

One license per deployment. No per-seat fees. No per-query fees. Unlimited users.

License keys are validated locally. No phone-home. No telemetry. Works air-gapped.

```bash
export GRIP_LICENSE_KEY=<your-key>
```

---

## Enterprise

An accelerated engine is available for organizations with large-scale retrieval needs.

**1.2ms at 28 million records. Single GPU.**

[enterprise@getgrip.dev](mailto:enterprise@getgrip.dev)

---

## License

See [LICENSE](./LICENSE) for full terms.

Free tier: evaluation and non-production use.  
Licensed tiers: production use within your organization.  
Accelerated engine: available under NDA.
