# GRIP User Guide

<p align="center">
  <img src="Logo.png" alt="GRIP" width="400">
</p>

Complete documentation for GRIP — Graph Retrieval with Intrinsic Patterns.

← Back to [README](./README.md) · 🌐 [getgrip.dev](https://grip-hub.github.io/getgrip.dev/)

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

**Option A — pip**

```bash
# Install and start
pip install getgrip
getgrip
# → opens http://localhost:7878 (web UI with Browse button)

# Or via curl:
curl -X POST http://localhost:7878/ingest \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/to/your/code"]}'

curl "http://localhost:7878/search?q=authentication+handler&top_k=5"
```

**Option B — Docker**

```bash
# Start GRIP
docker run -d -p 7878:7878 -v grip-data:/data -v /your/code:/code griphub/grip:free

# Ingest
curl -X POST http://localhost:7878/ingest \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/code"]}'

# Search
curl "http://localhost:7878/search?q=authentication+handler&top_k=5"

# Or open http://localhost:7878 in your browser
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
- CLI + FastAPI server (9 endpoints, CORS-ready)
- Ollama and OpenAI-compatible LLM plugins
- GitHub and local source ingestion plugins
- Code-aware and generic chunking plugins

---

## Free Demo Limits

The free `pip install` package includes all features with a **10,000 chunk limit**. No license key required. No time limit. Chunks can be deleted and replaced, but learned data (co-occurrence, remember scores) resets when you delete a source. Licensed tiers preserve learning permanently — even through deletions.

Need more? See [Pricing](https://grip-hub.github.io/getgrip.dev/#pricing).

---

## Estimating Your Chunk Count

GRIP splits text into chunks of ~500 tokens (~375 words, ~2KB of text) with 50-token overlap.

**Quick estimate from file count:**

```
Your text files × 3 = approximate chunks
```

Most code files produce 1–5 chunks. Documentation files produce 2–10. The average across real projects is ~3 chunks per file.

**Quick estimate from disk size:**

```
Total text size in MB × 500 = approximate chunks
```

This counts only text files — binary files (images, compiled artifacts) are skipped automatically.

**Real-world examples:**

| Project | Files | Chunks | Chunks/File |
|---------|-------|--------|-------------|
| Small app (200 files) | 200 | ~600 | 3.0 |
| Medium app (1,000 files) | 1,000 | ~3,000 | 3.0 |
| FastAPI (GitHub) | 2,424 | 4,195 | 1.7 |
| Large app (5,000 files) | 5,000 | ~12,000 | 2.4 |
| Monorepo (20,000 files) | 20,000 | ~45,000 | 2.3 |
| Linux kernel (70K+ files) | 70,000+ | 188,209 | 2.7 |
| One book (~80K words) | 1 | ~215 | — |
| Wikipedia article | 1 | ~12 | — |

**Tier selection guide:**

| If you have... | You need... | Tier |
|----------------|-------------|------|
| One project under 3,500 files | < 10K chunks | Free |
| Multiple projects or a large codebase | 10K–100K chunks | Personal ($499/yr) |
| A monorepo or several team repos | 100K–500K chunks | Team ($1,499/yr) |
| Enterprise-scale code + documentation | 500K–5M chunks | Professional ($4,999/yr) |
| Beyond 5M chunks | Custom | [Enterprise](mailto:getgrip.dev@gmail.com) |

**Check your count after ingesting:**

```bash
curl http://localhost:7878/stats
# → "total_chunks": 4223
```

---

## Licensed Tiers

| Tier | Chunks | Price |
|------|--------|-------|
| Personal | 100,000 | $499/year |
| Team | 500,000 | $1,499/year |
| Professional | 5,000,000 | $4,999/year |
| Enterprise | 25,000,000+ | [Contact us](mailto:getgrip.dev@gmail.com) |

One license per deployment. No per-seat fees. No per-query fees. Unlimited users.

License keys are validated locally. No phone-home. No telemetry. Works air-gapped.

```bash
export GRIP_LICENSE_KEY=<your-key>
```

---

## Enterprise

An accelerated engine is available for organizations with large-scale retrieval needs.

**1.2ms at 28 million records. Single GPU.**

[getgrip.dev@gmail.com](mailto:getgrip.dev@gmail.com)

---

## User Guide

### Installation

**Option A — pip (free tier)**

```bash
pip install getgrip
```

Requires Python 3.9+. No other dependencies needed for core retrieval.

**Option B — Docker (free or licensed)**

```bash
# Free tier
docker run -d -p 7878:7878 -v /your/data:/data -v /your/code:/code griphub/grip:free

# Licensed tier
docker run -d -p 7878:7878 -v /your/data:/data -v /your/code:/code \
  -e GRIP_LICENSE_KEY="GRIP-<your-key>" griphub/grip:latest
```

The `/data` volume stores the index, co-occurrence graph, and remember scores. Mount it to persist data across restarts. The `/code` volume is where your source files live.

Open `http://localhost:7878` for the web UI, or use the API and CLI below.

---

### Ingesting Data

GRIP needs data before it can search. Ingest local directories or clone GitHub repos directly.

**API**

```bash
# Local directory
curl -X POST http://localhost:7878/ingest \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/code/my-project"]}'

# GitHub repo
curl -X POST http://localhost:7878/ingest \
  -H "Content-Type: application/json" \
  -d '{"paths": ["https://github.com/org/repo"]}'
```

Or use the **Browse** button in the web UI at `http://localhost:7878` to select directories visually.

**What gets indexed:** Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, PHP, Swift, Kotlin, Markdown, RST, TXT, YAML, JSON, TOML, and other text files. Binary files (images, compiled artifacts, archives) are automatically skipped.

**Chunking:** Files are split into chunks of ~500 tokens with 50-token overlap. Code-aware chunking tries to keep functions and classes intact rather than splitting mid-block.

**Re-ingesting:** Ingesting the same source again updates it. GRIP deduplicates by source name.

---

### Searching

**API**

```bash
curl "http://localhost:7878/search?q=authentication+middleware&top_k=5"
```

**Response fields:**

| Field | Description |
|-------|-------------|
| `results` | Array of matching chunks with scores, source file, line number, and text |
| `confidence` | Overall result quality: `HIGH`, `MEDIUM`, `LOW`, or `NONE` |
| `latency_ms` | Query time in milliseconds |
| `expanded_query` | Your query plus co-occurrence terms GRIP added automatically |
| `session_id` | Session identifier for multi-turn continuity |

**Confidence levels:**

- **HIGH** — Strong matches with clear separation from weaker results. The top result is significantly better than alternatives.
- **MEDIUM** — Good matches found. Results are relevant but there may be ambiguity.
- **LOW** — Weak matches. Results may be tangentially related. Use with caution.
- **NONE** — No meaningful matches found. The query terms don't appear in your data. Tell your LLM to say "I don't know" rather than guess.

---

### Query Expansion (Co-occurrence)

After ingestion, GRIP builds a co-occurrence graph from your data. Words that frequently appear near each other become linked. When you search for "auth", GRIP automatically expands the query to include "authentication", "OAuth", "JWT", "token", "bearer" — whatever your specific codebase uses.

This is not a synonym dictionary. It's learned from your data. A medical corpus will learn that "MI" expands to "myocardial infarction". A legal corpus will learn that "tort" expands to "negligence", "liability", "damages". Your codebase will learn your team's vocabulary.

The expanded query appears in the `expanded_query` field of every search response so you can see exactly what GRIP did.

Co-occurrence builds automatically on first ingest. It improves as more data is added. No configuration needed.

---

### Sessions (Multi-Turn Search)

GRIP supports conversational retrieval through sessions. Start a session, search for something, then say "tell me more" or "what about error handling?" — GRIP carries context from the previous query.

**API**

```bash
# Turn 1
curl -X POST http://localhost:7878/query \
  -H "Content-Type: application/json" \
  -d '{"q": "how does authentication work?", "session_id": "my-session-1"}'

# Turn 2 — GRIP remembers the topic
curl -X POST http://localhost:7878/query \
  -H "Content-Type: application/json" \
  -d '{"q": "tell me more", "session_id": "my-session-1"}'

# Turn 3 — narrow within the same session
curl -X POST http://localhost:7878/query \
  -H "Content-Type: application/json" \
  -d '{"q": "what about token refresh?", "session_id": "my-session-1"}'
```

Session detection is automatic. Phrases like "tell me more", "go on", "what else", "expand on that", and "what about X?" are recognized as continuation queries.

Each session is identified by `session_id`. Use any string. Sessions expire after inactivity (default: 30 minutes).

---

### Asking Questions (LLM Integration)

The `/query` endpoint with `"answer": true` sends retrieved chunks to a configured LLM and returns a generated answer with citations.

**Configure an LLM first:**

```bash
# Ollama (local, free)
curl -X POST http://localhost:7878/config \
  -H "Content-Type: application/json" \
  -d '{"provider": "ollama", "model": "llama3.2"}'

# OpenAI-compatible (any endpoint)
curl -X POST http://localhost:7878/config \
  -H "Content-Type: application/json" \
  -d '{"provider": "openai", "model": "gpt-4", "api_key": "sk-..."}'

# Anthropic
curl -X POST http://localhost:7878/config \
  -H "Content-Type: application/json" \
  -d '{"provider": "anthropic", "model": "claude-sonnet-4-20250514", "api_key": "sk-ant-..."}'
```

**API**

```bash
curl -X POST http://localhost:7878/query \
  -H "Content-Type: application/json" \
  -d '{"q": "how does the auth middleware validate tokens?", "answer": true}'
```

The LLM receives your query, the top matching chunks, and the confidence level. When confidence is NONE, the LLM is instructed to acknowledge it doesn't have enough information rather than hallucinate.

An LLM is only needed for `"answer": true` queries. All other features (search, co-occurrence, sessions, confidence) work without any LLM.

---

### Plugins

GRIP uses a plugin architecture for sources, chunkers, LLM backends, and analyzers. All plugins are included — no separate installs.

**Source Plugins**

| Plugin | Trigger | Description |
|--------|---------|-------------|
| Local directory | `/path/to/dir` | Walks the directory, indexes all text files recursively |
| GitHub | `https://github.com/org/repo` | Clones the repo and indexes it. Works with any public repo |

GRIP auto-detects which source plugin to use based on the path you provide.

**Chunker Plugins**

| Plugin | Used For | Behavior |
|--------|----------|----------|
| Code-aware | `.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.c`, `.h`, etc. | Respects function and class boundaries. Avoids splitting mid-block |
| Generic | `.md`, `.txt`, `.rst`, `.yaml`, `.json`, etc. | Splits on paragraph boundaries at ~500 tokens per chunk |

GRIP selects the chunker automatically based on file extension. No configuration needed.

**LLM Backend Plugins**

| Plugin | Provider | Notes |
|--------|----------|-------|
| Ollama | Local models | Free, private, no API key. Requires [Ollama](https://ollama.com) running locally |
| OpenAI | GPT-4, GPT-3.5, etc. | Any OpenAI-compatible endpoint. Works with local servers like LM Studio, vLLM, text-generation-webui |
| Anthropic | Claude | Requires API key |
| Custom | Any HTTP endpoint | Set a custom base URL for self-hosted or alternative providers |

Configure via the `/config` endpoint. Only needed for LLM-powered answers — core retrieval works without any LLM.

**Analyzer Plugins**

Analyzers post-process search results. The built-in analyzer handles confidence scoring and reranking. The reranker (MiniLM, 22M parameters) is optional — if not available, GRIP falls back to BM25 scoring alone.

---

### Integrating GRIP Into Your Application

GRIP is a retrieval backend. Your application talks to it over HTTP. Here's how to build on top of it.

**Python — basic search**

```python
import requests

GRIP = "http://localhost:7878"

def search(query, top_k=5):
    r = requests.post(f"{GRIP}/search", json={"q": query, "top_k": top_k})
    data = r.json()
    return data["results"], data["confidence"]

results, confidence = search("authentication middleware")
for chunk in results:
    print(f"[{chunk['score']:.1f}] {chunk['source']}:{chunk.get('line', '')}")
    print(f"  {chunk['text'][:200]}")
```

**Python — RAG pipeline (retrieve + generate)**

```python
import requests

GRIP = "http://localhost:7878"

def ask_with_context(question):
    # Step 1: Retrieve relevant chunks
    search = requests.post(f"{GRIP}/search", json={"q": question, "top_k": 5}).json()

    # Step 2: Check confidence — don't hallucinate
    if search["confidence"] == "NONE":
        return "I don't have enough information to answer that."

    # Step 3: Build context from results
    context = "\n\n".join(
        f"[{r['source']}:{r.get('line', '')}]\n{r['text']}"
        for r in search["results"]
    )

    # Step 4: Send to your LLM (any provider, any framework)
    prompt = f"""Answer the question based on the context below.
If the context doesn't contain the answer, say so.

Context:
{context}

Question: {question}
"""
    # Replace with your LLM call:
    #   openai.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    #   anthropic.messages.create(model="claude-sonnet-4-20250514", messages=[{"role": "user", "content": prompt}])
    #   requests.post("http://localhost:11434/api/generate", json={"model": "llama3.2", "prompt": prompt})
    answer = call_your_llm(prompt)
    return answer
```

**Python — auto-ingest on file change**

```python
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

GRIP = "http://localhost:7878"

class ReindexHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.py', '.js', '.ts', '.md')):
            requests.post(f"{GRIP}/ingest", json={"paths": ["/code/my-project"]})
            print(f"Re-indexed after change to {event.src_path}")

observer = Observer()
observer.schedule(ReindexHandler(), "/code/my-project", recursive=True)
observer.start()
```

**JavaScript / Node.js**

```javascript
const GRIP = "http://localhost:7878";

async function search(query) {
  const params = new URLSearchParams({ q: query, top_k: 5 });
  const res = await fetch(`${GRIP}/search?${params}`);
  return res.json();
}

// Use in an Express route, Discord bot, Slack bot, VS Code extension, etc.
app.get("/ask", async (req, res) => {
  const { results, confidence } = await search(req.query.q);
  res.json({ results, confidence });
});
```

**cURL — CI/CD integration**

```bash
#!/bin/bash
# Re-index after every deploy
curl -X POST http://grip:7878/ingest \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/app"]}'

# Smoke test: verify critical code is findable
RESULT=$(curl -s "http://grip:7878/search?q=payment+processing&top_k=1")
CONFIDENCE=$(echo "$RESULT" | jq -r '.confidence')

if [ "$CONFIDENCE" = "NONE" ]; then
  echo "WARNING: payment processing code not found in index"
  exit 1
fi
```

**LangChain — drop-in retriever replacement**

Replace Pinecone, Chroma, or any vector store in your existing LangChain app:

```python
from langchain.schema import BaseRetriever, Document
import requests

class GRIPRetriever(BaseRetriever):
    grip_url: str = "http://localhost:7878"
    top_k: int = 5

    def _get_relevant_documents(self, query):
        r = requests.get(
            f"{self.grip_url}/search",
            params={"q": query, "top_k": self.top_k}
        )
        data = r.json()
        return [
            Document(
                page_content=chunk["text"],
                metadata={
                    "source": chunk["source"],
                    "line": chunk.get("line", ""),
                    "score": chunk["score"],
                    "confidence": data["confidence"],
                }
            )
            for chunk in data["results"]
        ]

# Use it anywhere you'd use a vector store retriever
retriever = GRIPRetriever()
chain = RetrievalQA.from_chain_type(llm=your_llm, retriever=retriever)
chain.run("how does authentication work?")
```

No embedding model. No vector database. No API keys for retrieval. Your existing LangChain prompts, chains, and agents work unchanged — GRIP just replaces the retrieval backend.

**LlamaIndex — same approach**

```python
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore, TextNode
import requests

class GRIPRetriever(BaseRetriever):
    def _retrieve(self, query_bundle):
        r = requests.post("http://localhost:7878/search",
            json={"q": query_bundle.query_str, "top_k": 5})
        data = r.json()
        return [
            NodeWithScore(
                node=TextNode(text=chunk["text"], metadata={"source": chunk["source"]}),
                score=chunk["score"]
            )
            for chunk in data["results"]
        ]
```

**Common integration patterns:**

| Pattern | How |
|---------|-----|
| LangChain RAG | `GRIPRetriever` replaces any vector store retriever — drop-in swap |
| LlamaIndex RAG | Custom `BaseRetriever` calls GRIP `/search` — same pattern |
| Chatbot / Q&A | Search GRIP → feed chunks to LLM → return answer with sources |
| Code search | Point your IDE or internal tool at `/search` |
| Documentation search | Ingest your docs folder, embed search in your docs site |
| CI/CD validation | Re-index on deploy, smoke test that critical code is indexed |
| Slack/Discord bot | Bot receives question → calls `/query` with `answer: true` → posts response |
| File watcher | Auto re-index when files change using watchdog or inotify |
| Multi-repo search | Ingest multiple repos as separate sources, search across all of them |

GRIP is a JSON API on localhost. Anything that can make HTTP requests can use it. No SDK required. No client library to install. No authentication for local access.

---

### Managing Sources

**List sources**

```bash
curl http://localhost:7878/sources
```

Returns each source with its name, chunk count, file count, and type (directory or git).

**Delete a source**

```bash
curl -X DELETE "http://localhost:7878/sources/my-project"
```

**Delete all sources**

```bash
curl -X DELETE http://localhost:7878/sources
```

**Free tier:** Deleting a source resets all co-occurrence and remember data for that source. This is the primary constraint of the free tier — learned relationships are lost on deletion.

**Licensed tiers:** Deleting a source removes the chunks but preserves all learned data. Co-occurrence edges and remember scores accumulated over time persist permanently.

---

### Stats and Health

**Stats**

```bash
curl http://localhost:7878/stats
```

```json
{
  "version": "0.2.0",
  "uptime_seconds": 70.2,
  "total_chunks": 4223,
  "chunk_limit": 10000,
  "total_sources": 2,
  "total_queries": 18,
  "avg_query_ms": 4.6,
  "llm_configured": false,
  "reranker_available": false,
  "tier": "free",
  "memory_warning": null
}
```

**Health**

```bash
curl http://localhost:7878/health
```

Returns `200 OK` with tier and status. Use for load balancer health checks and monitoring.

---

### API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ingest` | Add a source (local directory or GitHub URL) |
| `GET/POST` | `/search` | Search the index, returns ranked results |
| `POST` | `/query` | Search + optional LLM answer generation |
| `POST` | `/config` | Configure LLM provider and model |
| `GET` | `/sources` | List all ingested sources |
| `DELETE` | `/sources/{name}` | Delete a specific source |
| `DELETE` | `/sources` | Delete all sources |
| `GET` | `/stats` | System statistics and usage |
| `GET` | `/health` | Health check |

All endpoints accept and return JSON. CORS is enabled for browser-based access.

---

### Docker Configuration

**Environment variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `GRIP_LICENSE_KEY` | License key for paid tiers | None (free tier) |
| `GRIP_DATA_DIR` | Data storage directory | `/data` |

**Volumes**

| Mount | Purpose |
|-------|---------|
| `/data` | Index, co-occurrence graph, remember scores — **mount this to persist data** |
| `/code` | Your source files for ingestion |

**Ports**

The server listens on port 7878 inside the container. Map to any host port:

```bash
docker run -d -p 7878:7878 -v grip-data:/data griphub/grip:free
```

**Container lifecycle**

- All data persists in the `/data` volume across container restarts
- Stop and start containers freely — no data loss with a mounted volume
- Running without a volume mount means data is lost when the container stops

---

### Upgrading from Free to Licensed

No re-ingestion needed. No data migration. Just add your license key:

```bash
# Stop the free container
docker stop grip

# Start with license key (same data volume)
docker run -d -p 7878:7878 -v grip-data:/data \
  -e GRIP_LICENSE_KEY="GRIP-<your-key>" \
  --name grip griphub/grip:latest
```

Your existing index, queries, and sources carry over. The chunk limit increases to your licensed tier, and learning data is now preserved permanently through deletions.

---

### Troubleshooting

**"Chunk limit reached" on ingest**

You've hit the 10,000 chunk limit on the free tier. Delete unused sources to make room, or upgrade to a licensed tier for more capacity.

**"NONE" confidence on every search**

Your query terms don't appear in the indexed data. Check that ingestion completed successfully with `/stats`. Try broader search terms.

**LLM not responding for queries with `"answer": true`**

Verify your LLM is configured via `/config`. For Ollama, ensure it's running (`ollama serve`) and the model is pulled (`ollama pull llama3.2`). GRIP's core search works without any LLM — only answered queries require one.

**Co-occurrence not expanding queries**

Co-occurrence builds during ingestion. With very small corpora (under 50 chunks), there may not be enough data for meaningful co-occurrence edges. Ingest more data and the expansion graph will grow automatically.

**Container exits on startup**

Check Docker logs: `docker logs grip`. Common causes: port already in use, volume permissions, or (licensed tier) an invalid license key.

**Search is slow**

GRIP search is typically under 10ms. If you're seeing slow queries, check: very long query strings (200+ terms), system memory pressure, or disk I/O contention on the data volume. For very large corpora (500K+ chunks), consider a licensed tier for priority ingestion.

---

## License

See [LICENSE](./LICENSE) for full terms.

Free tier: evaluation and non-production use.  
Licensed tiers: production use within your organization.  
Accelerated engine: available under NDA.
