# AutoDiag AI → FuelTech AI Portfolio Project

**Project:** AI-powered diagnostic and tuning assistant for programmable ECU ecosystems  
**Target Roles:** AI Specialist — Conversational Systems | AI Specialist — Data Analysis & Specialized Models  
**Company:**   
**Author:** Guilherme  
**Status:** Planning

---

## 1. Strategic Alignment

This project is designed as a **direct capability demonstration** for both FuelTech AI roles. Every component maps to a specific job requirement.

### Role 1 — Conversational AI Systems

| Job Requirement | Project Component |
|-----------------|-------------------|
| RAG pipelines for large-scale technical docs | FuelTech doc corpus ingestion (manuals, FT Education, YT transcripts) |
| AI agent orchestration solving real user problems | Tool-calling agent: diagnose, explain, recommend tuning adjustments |
| Chat with memory, persistent context, personalization | Session memory tracking vehicle profile, tuning history, user skill level |
| Evaluate and integrate different LLMs (quality/cost/latency) | Benchmark matrix: GPT-4o-mini vs Claude Haiku vs Llama 3.2 3B vs Phi-3.5 |
| Automatic report generation from data | Telemetry summary reports from logged sensor sessions |
| Cost control strategies per user profile | Token budgeting: edge (free) vs cloud (metered), routing logic |
| Prompt engineering, function calling, tool use | Custom ReAct agent with structured tool definitions |

### Role 2 — Data Analysis & Specialized Models

| Job Requirement | Project Component |
|-----------------|-------------------|
| Anomaly detection in large data volumes | Sensor anomaly detection on telemetry streams (coolant, AFR, knock) |
| Fine-tune specialized models | Fine-tune small classifier on DTC pattern recognition |
| Actionable recommendations from raw data | "Your AFR is running lean at high RPM — check injector sizing" |
| Parsers/pipelines for diverse data formats | OBD-II PID decoder, FuelTech log parser, PDF/video transcript ingestion |
| Lightweight models on mobile/edge | Quantized LLM + anomaly detector on Raspberry Pi 5 |
| Edge/embedded deployment optimization | GGUF quantization, latency profiling, RAM budgeting |
| Validate AI outputs against real-world constraints | Cross-check recommendations against safe AFR/timing ranges |

---

## 2. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    EDGE DEVICE (Raspberry Pi 5 — 8GB)            │
│                                                                  │
│  ┌──────────────┐                                                │
│  │  OBD-II /    │    ┌─────────────────────────────────────────┐ │
│  │  ECU via     │───▶│  DATA INGESTION LAYER                  │ │
│  │  ELM327 BT   │    │                                         │ │
│  └──────────────┘    │  • python-obd: PID polling (RPM, AFR,   │ │
│                      │    MAP, IAT, coolant, knock, timing)     │ │
│                      │  • Log parser: FuelTech DataLog format   │ │
│                      │  • Anomaly detector: rolling-window      │ │
│                      │    statistical model on sensor streams   │ │
│                      └──────────┬──────────────────────────────┘ │
│                                 │                                 │
│  ┌──────────────────────────────▼──────────────────────────────┐ │
│  │  AI AGENT CORE                                              │ │
│  │                                                              │ │
│  │  ┌────────────────────┐  ┌────────────────────────────────┐ │ │
│  │  │  RAG ENGINE        │  │  AGENT (ReAct + Tool Calling)  │ │ │
│  │  │                    │  │                                │ │ │
│  │  │  Corpus:           │  │  Tools:                        │ │ │
│  │  │  • FT manuals      │  │  • read_sensor(name)           │ │ │
│  │  │  • FT Education    │  │  • read_dtc()                  │ │ │
│  │  │  • YT transcripts  │  │  • query_docs(query, top_k)    │ │ │
│  │  │  • DTC database    │  │  • analyze_trend(sensor, win)  │ │ │
│  │  │  • Tuning guides   │  │  • detect_anomaly(sensor)      │ │ │
│  │  │                    │  │  • generate_report(session_id)  │ │ │
│  │  │  ChromaDB + BM25   │  │  • get_vehicle_profile()       │ │ │
│  │  │  BGE-small embed.  │  │  • suggest_tuning(param, goal) │ │ │
│  │  └────────────────────┘  └────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  SESSION MEMORY                                        │ │ │
│  │  │  • Vehicle profile (engine, mods, ECU model)           │ │ │
│  │  │  • Conversation history (sliding window)               │ │ │
│  │  │  • Tuning session log (changes + outcomes)             │ │ │
│  │  │  • User skill level (beginner / tuner / engineer)      │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  LLM INFERENCE                                               │ │
│  │                                                               │ │
│  │  LOCAL: llama-cpp-python (Llama 3.2 3B Q4_K_M)              │ │
│  │         ↕ fallback / quality comparison                      │ │
│  │  CLOUD: OpenAI API / Anthropic API (metered, for complex Qs)│ │
│  │                                                               │ │
│  │  Router: complexity classifier → edge or cloud               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  UI: FastAPI + Web (phone connects via Pi WiFi AP)           │ │
│  │  • Chat interface with persistent session                    │ │
│  │  • Live sensor dashboard                                     │ │
│  │  • Session report export (PDF)                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Specification

### 3.1 Document Corpus (RAG)

| Source | Type | Acquisition | Notes |
|--------|------|-------------|-------|
| FuelTech product manuals | PDF | Public downloads from fueltech.com | FT600, FT550, FT450, PowerFT |
| FT Education | Video transcripts | YouTube API → Whisper transcription | Official training content |
| FuelTech YouTube channel | Video transcripts | YouTube API → Whisper | Technical tutorials, product demos |
| OBD-II DTC database | Structured data | Public OBD-II PID/DTC specs | P0xxx, P1xxx codes |
| Tuning community knowledge | Forum posts / guides | Curated from public forums | AFR tables, timing maps, boost curves |
| SAE J1979 / ISO 15031 | Reference | Public summaries | OBD-II protocol spec |

**Chunking strategy:**
- **Manuals:** Section-aware splitting (respect heading hierarchy), ~512 tokens/chunk
- **Video transcripts:** Topic-segmented (detect topic shifts via embedding similarity), timestamped
- **DTC database:** One chunk per code (structured: code + description + causes + symptoms + fix)
- **Tuning guides:** Paragraph-level with metadata (engine type, ECU model, modification context)

**Metadata per chunk:** source_type, document_title, section_path, ecu_model (if applicable), language (pt/en)

### 3.2 RAG Pipeline

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Embeddings | `BAAI/bge-small-en-v1.5` (33M) | Runs on Pi, strong for retrieval |
| Multilingual alt. | `BAAI/bge-m3` if pt-br retrieval quality is insufficient | FuelTech docs are mixed pt/en |
| Vector DB | ChromaDB (SQLite backend) | Zero infra, persistent, ARM-compatible |
| Keyword search | `rank_bm25` | DTC codes are exact-match (P0301, not "misfire") |
| Retrieval | Hybrid: dense (0.7) + BM25 (0.3), reciprocal rank fusion | Best of both for mixed query types |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-2-v2` (optional) | Only if latency < 300ms on Pi |
| Eval | Precision@5, MRR, Hit Rate on 80+ labeled queries | Bilingual eval set (pt + en) |

### 3.3 Agent Design

**Architecture:** Custom ReAct loop. No LangChain — demonstrates understanding of internals (interview differentiator).

**Tools:**

| Tool | Signature | Purpose | Maps to Role |
|------|-----------|---------|-------------|
| `read_sensor` | (name: str) → value, unit, range, status | Real-time OBD-II read | Role 2 |
| `read_dtc` | () → List[DTC] | Active fault codes | Role 1+2 |
| `query_docs` | (query: str, top_k: int, filter: dict) → chunks[] | RAG retrieval | Role 1 |
| `analyze_trend` | (sensor: str, window_sec: int) → stats + trend | Temporal analysis | Role 2 |
| `detect_anomaly` | (sensor: str) → anomaly_flag, details | Statistical anomaly detection | Role 2 |
| `generate_report` | (session_id: str) → markdown/PDF | Session summary report | Role 1 |
| `get_vehicle_profile` | () → VehicleProfile | Stored vehicle metadata | Role 1 |
| `suggest_tuning` | (param: str, goal: str) → recommendation | Domain-specific recommendation | Role 1+2 |

**Agent loop constraints:**
- Max 6 tool calls per turn
- Timeout: 45s total per turn (edge), 15s (cloud)
- Safety rails: never recommend timing/AFR values outside documented safe ranges
- Confidence tagging: high/medium/low on every recommendation

### 3.4 Session Memory & Personalization

```python
@dataclass
class VehicleProfile:
    make: str
    model: str
    year: int
    engine: str              # "2.0T", "LS3 6.2L", etc.
    ecu: str                 # "FT600", "FT550", "PowerFT"
    modifications: list[str] # ["turbo upgrade", "injectors 1000cc", "flex fuel"]
    known_issues: list[str]  # persisted across sessions

@dataclass
class SessionContext:
    vehicle: VehicleProfile
    user_skill: str          # "beginner" | "tuner" | "engineer"
    conversation_history: list[dict]  # sliding window, last 20 turns
    tuning_log: list[dict]   # {timestamp, parameter, old_value, new_value, outcome}
    active_dtcs: list[str]
```

**Personalization logic:**
- `beginner`: plain language, safety warnings prominent, no raw values
- `tuner`: technical but practical, AFR/timing references, actionable
- `engineer`: raw data, statistical details, confidence intervals

This directly addresses the Role 1 requirement: *"chat com memória, contexto persistente e personalização."*

### 3.5 Anomaly Detection (Role 2 Focus)

Lightweight statistical model running on sensor streams:

| Method | Use Case | Implementation |
|--------|----------|---------------|
| Z-score (rolling window) | Sudden spikes (knock, coolant temp) | NumPy, 30s window |
| IQR-based | Outlier detection on steady-state data | Pandas |
| Gradient threshold | Rapid rate-of-change (coolant rising fast) | NumPy diff |
| Fine-tuned classifier (stretch) | Pattern recognition on DTC sequences | Small MLP or decision tree on labeled DTC history |

**Alert pipeline:** sensor stream → rolling stats → threshold check → if anomaly: interrupt agent with priority alert → agent explains + recommends action.

### 3.6 LLM Evaluation & Cost Control

**Benchmark matrix (to be filled during Phase 1):**

| Model | Params | Quant | Location | Latency (TTFT) | Quality (eval score) | Cost/query |
|-------|--------|-------|----------|----------------|---------------------|------------|
| Llama 3.2 3B | 3B | Q4_K_M | Edge | TBD | TBD | $0 |
| Phi-3.5-mini | 3.8B | Q4_K_M | Edge | TBD | TBD | $0 |
| GPT-4o-mini | — | — | Cloud | TBD | TBD | ~$0.0003 |
| Claude 3.5 Haiku | — | — | Cloud | TBD | TBD | ~$0.0005 |

**Router logic:**
```
if query_complexity == "simple" (DTC lookup, sensor read):
    → edge model (free)
elif query_complexity == "medium" (diagnosis with context):
    → edge model, fallback to cloud if confidence < threshold
elif query_complexity == "complex" (multi-sensor analysis, tuning recommendation):
    → cloud model (metered)
```

This directly demonstrates the Role 1 requirement: *"definir estratégias de controle de custos de IA para diferentes perfis de usuário."*

### 3.7 Report Generation

Automatic session reports from telemetry data:

```markdown
# Diagnostic Session Report
**Vehicle:** 2019 VW Golf GTI — FT550  
**Date:** 2026-04-10 | **Duration:** 23 min  

## Active DTCs
- P0300: Random Misfire — cleared after spark plug inspection

## Sensor Summary
| Sensor | Min | Max | Mean | Anomalies |
|--------|-----|-----|------|-----------|
| RPM | 780 | 6,200 | 2,340 | 0 |
| AFR | 11.2 | 14.7 | 13.8 | 2 (lean at 5k+ RPM) |
| Coolant | 82°C | 97°C | 91°C | 0 |
| Knock | 0° | 3.2° | 0.4° | 1 (at 5,800 RPM) |

## AI Recommendations
1. AFR lean at high RPM — review fuel map above 5,000 RPM, consider injector upgrade
2. Knock detected at 5,800 RPM — retard timing 2° in that cell, re-test
3. Coolant within range but trending high — monitor during summer

## Session Transcript
[Condensed conversation log]
```

Directly maps to: *"construir geração automática de relatórios e análises a partir de dados."*

---

## 4. Hardware & Estimated Cost

| Component | Est. Cost (BRL) | Notes |
|-----------|-----------------|-------|
| Raspberry Pi 5 8GB | ~R$500 | Mandatory for 3B model Q4 |
| MicroSD 64GB A2 | ~R$50 | Fast I/O for model loading |
| ELM327 Bluetooth v2.1 | ~R$40 | Verify genuine chip |
| USB-C PD power supply | ~R$60 | Car cigarette lighter adapter |
| Case + active cooling | ~R$40 | Required under sustained inference |
| (Optional) 3.5" LCD | ~R$80 | Standalone display |
| **Total** | **~R$770** | ~$150 USD |

---

## 5. Phased Build Plan

### Phase 1: RAG Pipeline + LLM Evaluation (Weeks 1–2)
> **Deliverable:** Working RAG system over FuelTech-domain docs with quantitative eval.  
> **Role alignment:** Role 1 core competency.

- [ ] Collect corpus: download FT manuals (FT600, FT550, FT450), scrape FT Education transcripts, build DTC database
- [ ] Implement domain-aware chunking (section-based for manuals, topic-based for transcripts, structured for DTCs)
- [ ] Embed with BGE-small, store in ChromaDB, implement hybrid retrieval
- [ ] Build bilingual eval dataset: 80+ queries (pt + en) with expected retrievals
- [ ] Measure Precision@5, MRR, Hit Rate — iterate on chunking/retrieval
- [ ] Benchmark LLM quality: test 4 models on 30 diagnostic questions, score accuracy
- [ ] Document all architecture decisions and tradeoffs

### Phase 2: Agent + OBD-II + Memory (Weeks 3–4)
> **Deliverable:** Tool-calling agent with session memory, running on laptop + ELM327.  
> **Role alignment:** Role 1 (agent, memory, personalization) + Role 2 (sensor data).

- [ ] Set up python-obd + ELM327, validate sensor reads on your car
- [ ] Implement all 8 tool functions
- [ ] Build ReAct agent loop with function calling
- [ ] Implement session memory (vehicle profile, conversation history, skill-based personalization)
- [ ] Implement anomaly detection on sensor streams (z-score, gradient threshold)
- [ ] Test end-to-end scenarios: DTC diagnosis, live monitoring, tuning Q&A
- [ ] Implement report generation from session data
- [ ] Log all agent traces

### Phase 3: Edge Deployment + Cost Routing (Weeks 5–6)
> **Deliverable:** Full system on Raspberry Pi 5 with edge/cloud routing.  
> **Role alignment:** Role 2 (edge deployment, optimization) + Role 1 (cost control).

- [ ] Set up Pi 5, install llama-cpp-python ARM build
- [ ] Port full stack to Pi, benchmark latency per component
- [ ] Implement complexity-based router (edge vs cloud)
- [ ] Profile RAM: model + ChromaDB + anomaly detector + web server
- [ ] Implement WiFi AP + FastAPI web UI
- [ ] Optimize: tune chunk count, context window, quantization level
- [ ] Document edge vs cloud accuracy delta on eval set
- [ ] Stress test: 30-min driving session, thermal + latency monitoring

### Phase 4: Demo & Portfolio (Week 7)
> **Deliverable:** Video demo + GitHub repo + technical write-up.

- [ ] Record video: hardware → car connection → live diagnostic conversation → report generation
- [ ] README with architecture diagram, setup, benchmarks
- [ ] Technical blog post: design decisions, FuelTech domain alignment, tradeoffs
- [ ] Clean repo: tests, CI, Docker for non-Pi environments
- [ ] Publish GitHub, LinkedIn post, send to FuelTech recruiters

---

## 6. Key Differentiators for FuelTech Application

1. **Domain specificity:** Built on FuelTech's actual product ecosystem, not generic OBD-II
2. **Both roles in one project:** RAG + agents + memory (Role 1) AND edge deployment + anomaly detection + fine-tuning (Role 2)
3. **Production thinking:** Cost routing, safety rails, personalization by user skill — not a toy demo
4. **Bilingual:** System handles pt-br and English queries and documentation
5. **Quantitative rigor:** Every design choice backed by benchmark data
6. **Mathematical background:** Anomaly detection and optimization decisions grounded in your applied math training

---

## 7. Example Interactions (Demo Script)

### Scenario 1: Beginner user, check engine light
```
User: Meu carro acendeu a luz do motor, o que pode ser?

Agent: [read_dtc() → P0171: System Too Lean Bank 1]
Agent: [query_docs("P0171 sistema muito pobre banco 1 causas") → 3 chunks]
Agent: [read_sensor("SHORT_FUEL_TRIM_1") → +14.2%]

Agent: Seu carro está com o código P0171 — isso significa que a mistura
de combustível está pobre (pouco combustível para o ar que entra).

O trim de combustível está em +14.2%, que é alto. As causas mais comuns:
1. Vazamento de vácuo no coletor de admissão
2. Sensor MAF sujo
3. Problema no regulador de pressão de combustível

Recomendo começar verificando se há algum vazamento de vácuo — é a causa
mais comum e mais fácil de checar. Quer que eu explique como fazer?
```

### Scenario 2: Tuner, performance analysis
```
User: I'm seeing knock at high RPM. Can you analyze my last session?

Agent: [get_vehicle_profile() → Golf GTI, FT550, turbo upgrade]
Agent: [analyze_trend("KNOCK_RETARD", 300) → peaks at 5.5k-6.2k RPM]
Agent: [analyze_trend("AFR", 300) → lean excursion at same RPM range]
Agent: [query_docs("FT550 knock retard tuning high RPM turbo") → 2 chunks]

Agent: Your knock data shows retard events concentrated between 5,500
and 6,200 RPM. Cross-referencing with AFR, you're going lean in that
range (14.0-14.3 where target should be ~11.8 for boosted WOT).

This is consistent with insufficient fueling at high RPM — likely your
injectors are maxing out. With your FT550:

1. Check injector duty cycle in FTManager at 6k RPM — if >85%, you need
   larger injectors
2. Short-term fix: retard timing 2-3° in cells above 5,500 RPM
3. Your AFR target table may need enrichment in that zone

Confidence: HIGH — the lean AFR + knock correlation is a well-documented
pattern with upgraded turbo setups.

Session report generated. Want me to export it?
```

### Scenario 3: Engineer, data deep dive
```
User: Show me statistical analysis of coolant temp over the session.

Agent: [analyze_trend("COOLANT_TEMP", full_session)]
Agent: [detect_anomaly("COOLANT_TEMP")]

Agent: Coolant temperature analysis (23-minute session):

  μ = 91.3°C | σ = 4.2°C | min = 82°C | max = 97°C
  Trend: +0.08°C/min (slow upward drift)
  Anomalies: 0 (all values within 2σ)

  Distribution: approximately normal, slight right skew (0.3)
  consistent with gradual heat soak under mixed driving.

  The upward drift is within normal range but worth monitoring in
  sustained high-load scenarios. Your thermostat appears to be
  regulating correctly (no step-function behavior).
```

---

## 8. Tech Stack

```
Language:           Python 3.11+
OBD-II:             python-obd + ELM327 Bluetooth
Transcription:      OpenAI Whisper (for YT corpus ingestion)
Embeddings:         sentence-transformers (BGE-small-en-v1.5)
Vector DB:          ChromaDB (local, SQLite)
Keyword search:     rank_bm25
LLM (edge):         llama-cpp-python → Llama 3.2 3B Q4_K_M
LLM (cloud):        OpenAI / Anthropic API (metered)
Agent framework:    Custom ReAct (no LangChain)
Anomaly detection:  NumPy/SciPy (z-score, gradient, IQR)
Web UI:             FastAPI + HTMX
Report generation:  Jinja2 → Markdown → PDF (via weasyprint)
Hardware:           Raspberry Pi 5 8GB + ELM327 v2.1
OS:                 Ubuntu Server 24.04 (arm64)
```

---

## 9. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| 3B model weak at tool-calling | Agent unreliable | Edge/cloud router; cloud fallback for complex queries |
| FuelTech docs insufficient for rich RAG | Poor retrieval | Supplement with community forums, YT transcripts, DTC databases |
| ELM327 clone chip | Unreliable data | Buy verified; test early |
| Pi 5 RAM too tight | Can't run full stack | Profile Phase 1; mmap model; reduce embedding dim |
| Car has limited PID support | Boring demo | Check PID support first with free OBD app |
| Scope creep | Never ships | Phase 4 is a hard deadline — demo what's working |
| FuelTech hires before project is done | Missed window | Phase 1 alone is a credible application artifact |
