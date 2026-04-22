# AURA — Automotive Understanding & Reasoning Agent

> Edge AI Copilot for Vehicle Diagnostics under Resource Constraints

**Vehicle:** VW Amarok V6 3.0 TDI (2021+, stock OEM ECU)  
**Target Roles:** AI Specialist — Conversational Systems | AI Specialist — Data Analysis & Specialized Models  
**Target Company:** FuelTech  
**Author:** Guilherme  
**Status:** Planning

---

## 1. Strategic Alignment

AURA demonstrates every core competency from both FuelTech AI roles using a real vehicle as the test platform. The Amarok V6 3.0 TDI is ideal: modern CAN bus with rich PID support, turbodiesel complexity (boost, EGT, DPF, injector balance), and a large Brazilian owner community generating domain-specific content for the RAG corpus.

Although the vehicle runs a stock OEM ECU (not FuelTech), the skills demonstrated are directly transferable: the diagnostic reasoning, document retrieval, sensor analysis, and edge deployment are ECU-agnostic. The project narrative to FuelTech: *"I built the AI layer your customers would interact with — here it is working on a real vehicle."*

### AURA Subsystems

| Subsystem | Scope |
|-----------|-------|
| **AURA Core** | Agent reasoning, tool orchestration, ReAct loop |
| **AURA Sense** | OBD-II telemetry ingestion, anomaly detection |
| **AURA RAG** | Document corpus, embeddings, hybrid retrieval |
| **AURA Edge** | Quantized LLM, Pi 5 deployment, cost routing |
| **AURA Voice** | STT/TTS loop, hands-free interaction |

### Role 1 — Conversational AI Systems

| Job Requirement | AURA Component |
|-----------------|----------------|
| RAG pipelines for large-scale technical docs | AURA RAG: VW/Amarok manuals, TDI docs, diesel guides, community knowledge |
| AI agent orchestration solving real user problems | AURA Core: tool-calling agent — diagnose DTCs, explain sensor data, recommend maintenance |
| Chat with memory, persistent context, personalization | AURA Core: vehicle profile, session history, user skill adaptation |
| Evaluate and integrate different LLMs (quality/cost/latency) | AURA Edge: benchmark matrix — edge models vs cloud APIs on automotive QA |
| Automatic report generation from data | AURA Core: telemetry session reports with anomaly flags and maintenance recommendations |
| Cost control strategies per user profile | AURA Edge: edge/cloud routing based on query complexity |
| Prompt engineering, function calling, tool use | AURA Core: custom ReAct agent with 8 structured tools |

### Role 2 — Data Analysis & Specialized Models

| Job Requirement | AURA Component |
|-----------------|----------------|
| Anomaly detection in large data volumes | AURA Sense: real-time detection on diesel sensors (EGT, boost, DPF differential pressure) |
| Fine-tune specialized models | Fine-tuned DTC classifier / severity ranker on labeled automotive data |
| Actionable recommendations from raw data | "Boost pressure dropping at altitude — turbo actuator may need inspection" |
| Parsers/pipelines for diverse data formats | AURA Sense: OBD-II PID decoder, VW-specific extended PIDs, PDF manual parser, forum scraper |
| Lightweight models on mobile/edge | AURA Edge: quantized LLM + anomaly detector on Raspberry Pi 5 |
| Edge/embedded deployment optimization | AURA Edge: GGUF quantization, latency profiling, RAM budgeting |
| Validate AI outputs against real-world constraints | Cross-check against VW service intervals, safe operating ranges for 3.0 TDI |

---

## 2. Language Strategy

| Language | Role | Priority | Implementation Phase |
|----------|------|----------|---------------------|
| English | Primary — all core logic, prompts, tool definitions, eval datasets, agent reasoning | MVP | Phases 1–4 |
| Brazilian Portuguese | Support — user-facing responses, RAG corpus (forums, manuals), STT/TTS | MVP (secondary) | Phases 1–4 |
| Spanish | Future — extends market reach (FuelTech has strong LatAm presence) | Post-MVP | Phase 7+ |

**Architecture implications:**

- **Agent system prompt and tool schemas:** English only. The LLM reasons in English regardless of user language — this maximizes tool-calling reliability on small edge models.
- **Language detection + response routing:** Detect user input language → agent reasons in English internally → generates response in detected language.
- **RAG corpus:** Bilingual (en + pt-br). English corpus is the quality baseline (OBD-II specs, TDI technical docs, SAE standards). Portuguese corpus adds community knowledge (forums, YouTube, VW BR manuals). Metadata tag `language` on every chunk; retrieval filters by detected query language with English fallback.
- **Embeddings:** `BAAI/bge-m3` (multilingual) over `bge-small-en` — small accuracy cost on English, large gain on Portuguese retrieval. Evaluate both in Phase 1.
- **STT:** Whisper handles pt-br natively with strong accuracy. No additional work needed.
- **TTS:** Piper has pt-br voice models. English and Portuguese supported out of the box.
- **Eval datasets:** 80+ queries — 60% English, 40% Portuguese. Measure retrieval and generation quality per language separately.

**Spanish expansion (Phase 7+):**
- Add es corpus (FuelTech has Spanish-speaking customers across LatAm)
- Whisper and Piper both support Spanish — no model changes needed
- BGE-m3 already covers Spanish embeddings
- Main work: curate Spanish automotive corpus, extend eval dataset, test retrieval quality

**Why English-first matters for FuelTech:** Their technical documentation (ECU manuals, FT Education) is primarily in English and Portuguese. The AI roles require English intermediário. Demonstrating a system that reasons in English but responds in the user's language shows production-grade multilingual design, not just a translated UI.

---

## 3. Vehicle Platform: VW Amarok V6 3.0 TDI

### Why this vehicle works well

- **Rich sensor set:** Modern VAG diesel exposes extensive PIDs via OBD-II and VAG-specific UDS protocols
- **Turbodiesel complexity:** Boost control, EGT management, DPF regeneration, injector balance — more interesting telemetry than a naturally aspirated gasoline engine
- **Large Brazilian community:** Amarok is very popular in BR; extensive Portuguese-language forum content, YouTube channels, and owner knowledge bases for RAG corpus
- **Real maintenance scenarios:** DPF issues, AdBlue warnings, turbo actuator problems, injector coding — common Amarok V6 issues that make compelling demo scenarios

### Expected OBD-II PID Availability

**Standard OBD-II (ELM327 compatible):**

| PID | Sensor | Diagnostic Value |
|-----|--------|-----------------|
| 0x0C | Engine RPM | Baseline |
| 0x0D | Vehicle speed | Baseline |
| 0x05 | Coolant temperature | Overheating detection |
| 0x0B | Intake manifold pressure (MAP) | Boost pressure monitoring |
| 0x0F | Intake air temperature | Intercooler efficiency |
| 0x10 | MAF air flow rate | Air system health |
| 0x11 | Throttle position | Driver demand correlation |
| 0x2F | Fuel tank level | Baseline |
| 0x5C | Engine oil temperature | Critical for diesel longevity |
| 0x5E | Fuel consumption rate | Efficiency analysis |

**Diesel-specific (Mode 01 extended):**

| PID | Sensor | Diagnostic Value |
|-----|--------|-----------------|
| 0x1C | OBD compliance type | Protocol identification |
| 0x21 | Distance with MIL on | Urgency assessment |
| 0x4F | Max values (MAF, MAP, etc.) | Capacity reference |
| 0x70 | Boost pressure control | Turbo performance |
| 0x7C | DPF temperature | Regen cycle monitoring |
| 0x7E | DPF differential pressure | DPF clogging detection |

**VAG-specific (UDS, requires python-can + extended adapter):**

| Parameter | Access | Notes |
|-----------|--------|-------|
| Injector correction values | UDS 0x22 | Per-cylinder balance |
| EGT (exhaust gas temperature) | UDS 0x22 | Turbo/DPF health |
| AdBlue level & quality | UDS 0x22 | SCR system status |
| DPF soot loading % | UDS 0x22 | Regen prediction |
| Turbo actuator position | UDS 0x22 | Turbo health |
| Glow plug status | UDS 0x22 | Cold start diagnostics |

> **Note:** Standard ELM327 covers Mode 01 PIDs. VAG-specific UDS PIDs require either (a) an OBDEleven/VCDS-style adapter, or (b) a CAN bus adapter with python-can. Phase 1-2 will use standard PIDs; VAG-extended is a stretch goal.

### Critical First Step

**Before buying any hardware**, install a free OBD-II app (Torque, Car Scanner) with a cheap ELM327 and run a full PID scan on the Amarok. Document which PIDs respond. This determines which demo scenarios are feasible.

---

## 4. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    EDGE DEVICE (Raspberry Pi 5 — 8GB)            │
│                                                                  │
│  ┌──────────────┐                                                │
│  │  Amarok V6   │    ┌─────────────────────────────────────────┐ │
│  │  OBD-II port │───▶│  AURA SENSE (Data Ingestion)           │ │
│  │  ELM327 BT   │    │                                         │ │
│  └──────────────┘    │  • python-obd: standard PID polling     │ │
│                      │  • Diesel telemetry: boost, oil temp,   │ │
│                      │    DPF temp, fuel rate                   │ │
│                      │  • Anomaly detector: rolling-window      │ │
│                      │    stats on critical diesel parameters   │ │
│                      │  • Session logger: time-series to SQLite │ │
│                      └──────────┬──────────────────────────────┘ │
│                                 │                                 │
│  ┌──────────────────────────────▼──────────────────────────────┐ │
│  │  AURA CORE (Agent + Reasoning)                              │ │
│  │                                                              │ │
│  │  ┌────────────────────┐  ┌────────────────────────────────┐ │ │
│  │  │  AURA RAG          │  │  AGENT (ReAct + Tool Calling)  │ │ │
│  │  │                    │  │                                │ │ │
│  │  │  Corpus:           │  │  Tools:                        │ │ │
│  │  │  • VW service docs │  │  • read_sensor(name)           │ │ │
│  │  │  • Amarok forums   │  │  • read_dtc()                  │ │ │
│  │  │  • TDI tech guides │  │  • query_docs(query, top_k)    │ │ │
│  │  │  • DTC database    │  │  • analyze_trend(sensor, win)  │ │ │
│  │  │  • YT transcripts  │  │  • detect_anomaly(sensor)      │ │ │
│  │  │  • Owner community │  │  • generate_report(session_id)  │ │ │
│  │  │                    │  │  • get_vehicle_profile()       │ │ │
│  │  │  ChromaDB + BM25   │  │  • check_maintenance(km)       │ │ │
│  │  │  BGE-m3 embed.     │  │                                │ │ │
│  │  └────────────────────┘  └────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  SESSION MEMORY                                        │ │ │
│  │  │  • Vehicle: Amarok V6 3.0 TDI, km, service history    │ │ │
│  │  │  • Conversation history (sliding window)               │ │ │
│  │  │  • Maintenance log (oil changes, DPF regens, etc.)     │ │ │
│  │  │  • User skill level (owner / mechanic / engineer)      │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  AURA EDGE (LLM Inference + Routing)                        │ │
│  │  LOCAL: llama-cpp-python (Llama 3.2 3B Q4_K_M)              │ │
│  │  CLOUD: OpenAI / Anthropic API (fallback for complex Qs)    │ │
│  │  Router: complexity classifier → edge or cloud               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  AURA VOICE (Phase 5-6)                                     │ │
│  │  STT: whisper.cpp (local) | TTS: Piper / cloud fallback     │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  UI: FastAPI + Web (phone connects via Pi WiFi AP)           │ │
│  │  • "Ask AURA" chat interface with persistent session         │ │
│  │  • Live sensor dashboard (boost, EGT, oil temp, DPF)        │ │
│  │  • AURA Report export (PDF)                                  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

---

## 5. Document Corpus (AURA RAG)

| Source | Type | Language | Acquisition |
|--------|------|----------|-------------|
| VW Amarok owner's manual | PDF | pt-br | Public download / scan |
| VW 3.0 TDI V6 (EA897) service documentation | PDF | en/de | Public technical references |
| Amarok V6 common issues database | Structured | pt-br | Curated from forums + YouTube |
| OBD-II DTC database (diesel-specific) | Structured | en | Public P0xxx/P2xxx codes |
| VW-specific DTC database | Structured | en | P-codes + VAG fault codes |
| Amarok community forums | Web scrape | pt-br | AmarokV6.com.br, ForumAmarok, ClubAmarok |
| YouTube: Amarok V6 maintenance channels | Transcripts | pt-br | Whisper transcription |
| Diesel engine fundamentals | PDF/web | en/pt | Common rail, DPF, SCR, turbo docs |
| VW service interval tables | Structured | pt-br | Official VW BR maintenance schedule |
| TDI tuning & diagnostics guides | PDF/web | en | Public technical content |

**Estimated corpus size:** ~500-800 chunks after processing.

**Chunking strategy:**
- **Service manuals:** Section-aware (respect chapter/section hierarchy), ~512 tokens
- **Forum posts:** Thread-level with question/answer pairing preserved
- **YouTube transcripts:** Topic-segmented via embedding similarity, with timestamps
- **DTC database:** One chunk per code: code + description + causes + symptoms + fix + Amarok-specific notes
- **Maintenance schedule:** Structured by km interval: what's due, what to check, VW part numbers

**Metadata per chunk:** source_type, language, vehicle_applicability (Amarok V6 specific vs general TDI vs generic diesel), km_range (if maintenance-related)

---

## 6. Agent Tools

| Tool | Signature | Purpose |
|------|-----------|---------|
| `read_sensor` | (name: str) → {value, unit, normal_range, status} | Live OBD-II read |
| `read_dtc` | () → List[{code, description, severity}] | Active + pending DTCs |
| `query_docs` | (query: str, top_k: int, lang: str) → chunks[] | RAG retrieval |
| `analyze_trend` | (sensor: str, window_sec: int) → {min, max, mean, σ, trend, plot_data} | Temporal stats |
| `detect_anomaly` | (sensor: str) → {flag: bool, type, details} | Statistical anomaly |
| `generate_report` | (session_id: str) → report_path | PDF session report |
| `get_vehicle_profile` | () → VehicleProfile | Stored vehicle data |
| `check_maintenance` | (current_km: int) → {due: list, upcoming: list, overdue: list} | VW service schedule lookup |

### Diesel-Specific Anomaly Detection (AURA Sense)

| Sensor | Anomaly Type | Method | Alert Example |
|--------|-------------|--------|---------------|
| Boost pressure | Underboost / overboost | Expected vs actual MAP at RPM/load | "AURA detected boost 15% below target at 3k RPM — check turbo actuator" |
| Oil temperature | Overheat trend | Gradient threshold (>2°C/min sustained) | "AURA detected oil temp rising fast — reduce load, check oil level" |
| DPF diff. pressure | Clogging trend | Rolling mean increase over sessions | "AURA detected DPF pressure trending up — forced regen may be needed soon" |
| Coolant temperature | Thermostat stuck | Flat-line detection (never reaching operating temp) | "Coolant not reaching 90°C after 15min — thermostat stuck open?" |
| Fuel rate | Efficiency degradation | Session-over-session comparison at similar driving patterns | "Fuel consumption up 12% vs last month at similar load" |
| Intake air temp | Intercooler degradation | IAT vs ambient delta at boost | "Intake air 25°C above ambient under boost — intercooler efficiency degraded" |

---

## 7. Evaluation & Observability

### 7.1 Core Metrics

| Layer | Metric | Target | Method |
|-------|--------|--------|--------|
| **AURA RAG** | Precision@5 | >0.80 | Hand-labeled eval set (80+ queries) |
| **AURA RAG** | MRR | >0.75 | Same eval set |
| **AURA RAG** | Hit Rate | >0.90 | Same eval set |
| **AURA Core** | Tool selection accuracy | >0.90 | Labeled query→expected_tool pairs |
| **AURA Core** | Tool execution success rate | >0.95 | Automated (tool returns valid output) |
| **AURA Core** | Hallucination rate | <0.10 | Manual review on 50+ diagnostic responses |
| **AURA Edge** | End-to-end latency (p50) | <8s edge, <4s cloud | Automated timing |
| **AURA Edge** | End-to-end latency (p95) | <15s edge, <8s cloud | Automated timing |
| **AURA Edge** | Router accuracy | >0.85 | Labeled simple/medium/complex queries |
| **AURA Sense** | Anomaly detection precision | >0.85 | Labeled anomaly scenarios (real + simulated) |
| **AURA Sense** | Anomaly detection recall | >0.80 | Same dataset |
| **AURA Edge** | Peak RAM usage | <7 GB | Profiling under sustained load |

### 7.2 Structured Logging

Every agent turn is logged end-to-end:

```
timestamp
→ user_query (text or STT transcript)
→ detected_language
→ complexity_classification (simple / medium / complex)
→ routing_decision (edge / cloud)
→ retrieved_chunks[] (query, top_k, scores)
→ tool_calls[] (name, input, output, latency_ms)
→ llm_call (model, prompt_tokens, completion_tokens, latency_ms)
→ final_response (spoken + detailed)
→ confidence_tag (high / medium / low)
→ total_latency_ms
```

Stored in SQLite alongside telemetry data.

### 7.3 Evaluation per Language

All metrics measured separately for English and Portuguese:

| Metric | English | Portuguese | Delta |
|--------|---------|------------|-------|
| RAG Precision@5 | TBD | TBD | TBD |
| Tool selection accuracy | TBD | TBD | TBD |
| Hallucination rate | TBD | TBD | TBD |

If Portuguese delta is >15% on any metric, investigate: embedding model choice, corpus quality, or prompt engineering.

---

## 8. Failure Handling & Safety

### 8.1 Uncertainty Estimation

Every AURA response includes a confidence tag:

| Confidence | Criteria | Behavior |
|------------|----------|----------|
| **HIGH** | DTC found + RAG chunks match + sensor data corroborates | Normal response |
| **MEDIUM** | Partial evidence (RAG match but no sensor confirmation, or vice versa) | Response + caveat: "AURA recommends verifying with a mechanic" |
| **LOW** | No RAG match, ambiguous sensor data, or conflicting evidence | "AURA doesn't have enough data to diagnose this confidently. Recommend professional inspection." |

### 8.2 Safety Rails (Automotive-Specific)

- **Never recommend** timing/AFR/boost values outside documented safe ranges for the EA897 3.0 TDI
- **Never recommend** clearing DTCs without diagnosing root cause first
- **Never recommend** ignoring safety-critical warnings (overheating, oil pressure, DPF critical)
- **Always escalate** to human mechanic for: structural/braking concerns, airbag codes, emissions tampering
- **Validate** all maintenance recommendations against official VW service intervals

### 8.3 Failure Modes & Handling

| Failure | Detection | AURA Behavior |
|---------|-----------|---------------|
| OBD-II connection lost | Sensor timeout | "AURA lost connection to vehicle. Check ELM327 adapter." |
| No DTCs but user reports problem | Empty DTC read + user symptom | Symptom-based RAG lookup; recommend manual inspection |
| RAG returns irrelevant chunks | Low cosine similarity scores | Fall back to LLM general knowledge with low-confidence tag |
| LLM hallucinates a DTC code | Code not in DTC database | Post-generation validation: check all cited codes exist |
| Edge model gives incoherent response | Heuristic: response too short, no tool calls, gibberish | Auto-retry on cloud model |
| Conflicting sensor data | e.g., high boost + low RPM (physically impossible) | Flag as sensor error, don't diagnose |

---

## 9. Inference Profiling & Model Optimization (AURA Edge)

### 9.1 Quantization Comparison

| Model | Quant | Size (disk) | RAM (loaded) | Tokens/sec (Pi 5) | Tool-calling reliability | Quality score |
|-------|-------|-------------|--------------|-------------------|--------------------------|--------------|
| Llama 3.2 3B | Q4_K_M | ~1.8 GB | ~2.1 GB | TBD | TBD | TBD |
| Llama 3.2 3B | Q5_K_M | ~2.1 GB | ~2.5 GB | TBD | TBD | TBD |
| Llama 3.2 3B | Q8_0 | ~3.2 GB | ~3.6 GB | TBD | TBD | TBD |
| Phi-3.5-mini | Q4_K_M | ~2.2 GB | ~2.5 GB | TBD | TBD | TBD |

### 9.2 Latency Profiling (p50 / p95)

| Component | Target |
|-----------|--------|
| Embedding (single query) | <100ms |
| ChromaDB retrieval (top 5) | <200ms |
| BM25 retrieval | <50ms |
| Hybrid fusion + rerank | <300ms |
| LLM first token (edge) | <3000ms |
| LLM full response (edge) | <12000ms |
| LLM first token (cloud) | <1000ms |
| Tool execution (read_sensor) | <500ms |
| Total turn (edge) | <15000ms |
| Total turn (cloud) | <8000ms |

### 9.3 Memory Budget (Pi 5 — 8 GB)

| Component | Estimated RAM | Notes |
|-----------|--------------|-------|
| OS + Python runtime | ~500 MB | Ubuntu Server minimal |
| LLM (Q4_K_M, mmap) | ~2.1 GB | Memory-mapped |
| ChromaDB + embeddings index | ~300 MB | Depends on corpus size |
| BGE-m3 embedding model | ~500 MB | Loaded for query embedding |
| Whisper base (Phase 5+) | ~300 MB | Only when voice active |
| Piper TTS (Phase 6+) | ~150 MB | Only when voice active |
| FastAPI + web server | ~100 MB | |
| Anomaly detection buffers | ~50 MB | Rolling windows |
| **Total (text mode)** | **~3.5 GB** | Comfortable headroom |
| **Total (voice mode)** | **~4.0 GB** | Still fits with margin |

### 9.4 Trade-off Decisions (Documented)

| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| Model size | 1B / 3B / 7B | 3B Q4 | 7B exceeds Pi 5 RAM; 1B too weak for tool-calling |
| Embeddings | bge-small-en / bge-m3 | bge-m3 | Multilingual retrieval required; en-only fails on pt-br corpus |
| Retrieval | Dense-only / BM25-only / Hybrid | Hybrid (0.7/0.3) | DTC codes need exact match (BM25); descriptions need semantic (dense) |
| Vector DB | ChromaDB / FAISS / Qdrant | ChromaDB | SQLite backend, zero infra, ARM-compatible, persistent |
| Agent framework | LangChain / LlamaIndex / Custom | Custom ReAct | Demonstrates internals understanding; no dependency bloat on edge |
| Time-series storage | SQLite / InfluxDB / TimescaleDB | SQLite | Single-file, zero infra, sufficient for session-level data |
| Reranker | With / Without | Without (default) | Latency budget on Pi 5; add only if retrieval quality insufficient |
| Context window | 2048 / 4096 / 8192 | 4096 | Enough for RAG chunks + agent history; doesn't explode latency |

---

## 10. Simulation Mode

Since real faults are hard to trigger on a healthy vehicle, AURA includes a simulation layer for controlled evaluation and demo reliability.

### 10.1 Synthetic Anomaly Injection

```python
class AuraSenseSimulator:
    """Injects synthetic anomalies into real or recorded telemetry streams."""
    
    def inject_underboost(self, stream, start_sec, severity):
        """Gradually reduce MAP readings to simulate turbo actuator failure."""
    
    def inject_dpf_clog(self, stream, rate):
        """Increase DPF differential pressure over sessions."""
    
    def inject_coolant_overheat(self, stream, gradient):
        """Ramp coolant temp at specified deg C/min."""
    
    def inject_dtc(self, code, freeze_frame):
        """Add synthetic DTC with associated sensor snapshot."""
```

### 10.2 Session Replay

Record real driving sessions → replay through AURA Core for:
- Regression testing after agent changes
- Benchmarking retrieval quality on real-world queries
- Comparing edge vs cloud accuracy on identical inputs
- Demo reliability (guaranteed interesting data for video recording)

### 10.3 Evaluation Harness

```
Labeled test cases:
  - 30 DTC scenarios (code + expected diagnosis + expected tools)
  - 20 anomaly scenarios (sensor pattern + expected detection)
  - 30 general queries (maintenance, explanation, sensor interpretation)

Run all → score → compare across model versions / quantization levels
```

---

## 11. Session Memory & Personalization

```python
@dataclass
class VehicleProfile:
    make: str = "Volkswagen"
    model: str = "Amarok"
    variant: str = "V6 3.0 TDI"
    year: int = 2021
    engine_code: str = "EA897"
    power: str = "258 cv (overboost)"
    transmission: str = "8AT"
    fuel: str = "Diesel S-10"
    current_km: int = 0
    modifications: list = field(default_factory=list)
    service_history: list = field(default_factory=list)
    known_issues: list = field(default_factory=list)

@dataclass  
class SessionContext:
    vehicle: VehicleProfile
    user_skill: str              # "owner" | "mechanic" | "engineer"
    conversation_history: list   # sliding window, last 20 turns
    session_telemetry: dict      # sensor time-series for this session
    active_dtcs: list
    previous_reports: list       # links to past AURA Reports
```

**Personalization:**
- `owner`: Portuguese, plain language, "leve ao mecânico" recommendations, safety-first
- `mechanic`: Technical pt-br, part numbers, diagnostic procedures, tool references
- `engineer`: Raw data, statistical details, CAN protocol references, English technical terms

---

## 12. LLM Evaluation & Cost Routing (AURA Edge)

| Model | Location | Target Use | Eval Criteria |
|-------|----------|-----------|---------------|
| Llama 3.2 3B Q4 | Edge | Simple DTCs, sensor reads, maintenance lookup | Latency, tool-calling reliability |
| Phi-3.5-mini Q4 | Edge | Alternative benchmark | Same |
| GPT-4o-mini | Cloud | Complex diagnosis, multi-sensor correlation | Accuracy, reasoning depth |
| Claude 3.5 Haiku | Cloud | Alternative benchmark | Same |

**Router:**
```
simple (DTC lookup, single sensor, maintenance schedule) → edge
medium (diagnosis with 2-3 sensors + docs) → edge, fallback cloud if low confidence
complex (multi-sensor correlation, trend analysis, tuning advice) → cloud
```

**Measurable router outcomes:**
- Classification accuracy on labeled query set
- Cost savings vs full-cloud baseline (% of queries handled on edge)
- Latency improvement for simple queries (edge vs cloud)
- Quality delta: edge vs cloud on same queries

---

## 13. Phased Build Plan

### Phase 1: PID Discovery + AURA RAG (Weeks 1-2)
> **Deliverable:** Validated PID list for the Amarok + working AURA RAG over diesel/Amarok docs.

- [ ] **Week 1 Day 1:** Buy cheap ELM327 BT + install Torque/Car Scanner → full PID scan on Amarok
- [ ] Document every responding PID with values at idle and driving
- [ ] Collect corpus: Amarok manual, TDI docs, DTC databases, forum threads, YT transcripts
- [ ] Implement chunking pipeline (section-aware + DTC-structured + forum Q&A pairs)
- [ ] Embed + store in ChromaDB, implement hybrid retrieval
- [ ] Build eval dataset: 80+ queries (pt + en), Amarok-specific and general diesel
- [ ] Measure Precision@5, MRR, Hit Rate — iterate
- [ ] Benchmark 4 LLMs on 30 automotive diagnostic questions

### Phase 2: AURA Core + Live OBD-II + Memory (Weeks 3-4)
> **Deliverable:** Agent on laptop connected to Amarok via ELM327, full tool suite working.

- [ ] Implement all 8 tools with python-obd backend
- [ ] Build ReAct agent loop (custom, no LangChain)
- [ ] Implement session memory + vehicle profile (hardcoded Amarok V6 specs)
- [ ] Implement AURA Sense: diesel anomaly detection (boost, oil temp, DPF pressure, coolant)
- [ ] Implement maintenance schedule checker (VW intervals for Amarok)
- [ ] Implement AURA Report generation
- [ ] Implement simulation mode (anomaly injection + session replay)
- [ ] Implement structured logging (full agent trace per turn)
- [ ] Implement failure handling (confidence tags, safety rails, sensor validation)
- [ ] Test in car: idle diagnostics, driving session, DTC scenarios
- [ ] Run evaluation harness: 80 test cases, measure all core metrics

### Phase 3: AURA Edge Deployment + Router (Weeks 5-6)
> **Deliverable:** Full system on Pi 5, mounted in Amarok, phone UI via WiFi.

- [ ] Set up Pi 5, llama-cpp-python ARM, port full stack
- [ ] Implement edge/cloud complexity router
- [ ] Run inference profiling: quantization comparison, tokens/sec, cold/warm start
- [ ] Profile: latency per component (p50/p95), RAM usage, thermal under sustained use
- [ ] Build FastAPI web UI: "Ask AURA" chat + live sensor dashboard
- [ ] Configure Pi as WiFi AP (phone connects to "AURA-Amarok")
- [ ] Mount Pi in car (12V→USB-C power from accessory outlet)
- [ ] Stress test: 30+ min drive with continuous monitoring
- [ ] Document edge vs cloud accuracy delta
- [ ] Measure router accuracy, cost savings vs full-cloud baseline

### Phase 4: Demo Video + Portfolio (Week 7)
> **Deliverable:** Video recorded in/with the Amarok + polished GitHub repo.

**Video script outline:**
1. Hardware overview: Pi 5 + ELM327 + Amarok engine bay shot
2. Connection: plug ELM327, boot Pi, phone connects to WiFi
3. Demo 1: "What's the status of my truck?" → AURA reads sensors, reports health
4. Demo 2: Simulated DTC → AURA diagnoses with RAG context
5. Demo 3: "Analyze my boost pressure from this drive" → AURA trend analysis + anomaly check
6. Demo 4: "When is my next service?" → AURA maintenance schedule from km reading
7. Show generated AURA Report (PDF)
8. Architecture walkthrough (brief, screen recording of code/diagram)

- [ ] Record and edit video (5-8 min target)
- [ ] Clean GitHub repo: README, architecture diagram, benchmarks, setup guide
- [ ] Technical blog post
- [ ] Publish, share with FuelTech

### Phase 5: AURA Voice — Hands-Free Queries (Week 8)
> **Deliverable:** Speak to AURA, read the answer on screen.  
> **Hardware:** Pi 5 (existing) + USB microphone (~R$30-50)

```
Driver speaks → USB mic → Whisper.cpp (local STT) → AURA Core → Text on phone screen
```

- [ ] Install whisper.cpp ARM build on Pi 5
- [ ] Benchmark STT models: tiny (~1s), base (~2-3s), small (~5-8s)
- [ ] Test Portuguese recognition quality
- [ ] Implement push-to-talk or "Hey AURA" wake word (OpenWakeWord)
- [ ] Add VAD with Silero VAD
- [ ] Integrate into FastAPI: mic stream → STT → AURA Core → text response
- [ ] Test in-car with engine running
- [ ] Profile total latency: speech end → response displayed

### Phase 6: AURA Voice-to-Voice (Weeks 9-10)
> **Deliverable:** Full voice loop. Speak a question, hear the answer through the car speakers.

```
Driver speaks → Whisper.cpp (STT) → AURA Core → TTS → Car speakers / Bluetooth
```

- [ ] Install Piper TTS on Pi 5, test pt-br voice models
- [ ] Implement dual response: spoken summary (TTS) + detailed text (screen)
- [ ] Audio output: Pi 5 → Bluetooth to Amarok stereo, or 3.5mm aux
- [ ] Implement streaming TTS (reduce perceived latency)
- [ ] Profile end-to-end: speech end → first audio output
- [ ] Test in-car: engine noise, speaker volume, conversation flow
- [ ] Record demo video with voice-to-voice interaction

---

## 14. Hardware Upgrade Path

### Tier 1: MVP (Phases 1-4) — R$690

| Component | Cost |
|-----------|------|
| Raspberry Pi 5 8GB | ~R$500 |
| MicroSD 64GB A2 | ~R$50 |
| ELM327 Bluetooth v2.1 | ~R$40 |
| USB-C PD car charger | ~R$60 |
| Case + active cooling | ~R$40 |

### Tier 2: Voice Input (Phase 5) — +R$50

| Component | Cost |
|-----------|------|
| USB microphone | ~R$30-50 |

### Tier 3: Voice-to-Voice (Phase 6) — +R$150-250

| Component | Cost |
|-----------|------|
| USB microphone | ~R$30-50 |
| 3.5mm aux / BT audio transmitter | ~R$20-40 |
| (Optional) USB sound card | ~R$30 |
| (Optional) Small speaker | ~R$50-80 |

### Tier 4: Performance (Phase 6+) — +R$800-2500

| Component | Cost | Benefit |
|-----------|------|---------|
| Coral USB Accelerator | ~R$300-500 | Offload Whisper to Edge TPU |
| NVIDIA Jetson Orin Nano 8GB | ~R$1500-2500 | GPU inference, 10-20x faster |
| NVMe SSD hat for Pi 5 | ~R$150-200 | Faster model loading |
| OBDEleven adapter | ~R$350 | VAG-specific UDS PIDs |

### Voice-to-Voice Latency Targets

| Stage | Pi 5 (CPU) | Pi 5 + Coral | Jetson Orin Nano |
|-------|------------|--------------|------------------|
| STT (5s audio) | ~2-3s | ~0.5-1s | ~0.3-0.5s |
| AURA Core + RAG | ~3-5s | ~3-5s | ~2-3s |
| TTS (short) | ~1-2s | ~1-2s | ~0.5-1s |
| **Total** | **~6-10s** | **~4.5-8s** | **~3-4.5s** |

---

## 15. Demo Scenarios (Amarok-Specific)

### Scenario 1: Owner, routine check (Portuguese)
```
User: Como está meu carro?

AURA: [read_sensor("RPM") → 780]
      [read_sensor("COOLANT_TEMP") → 91°C]
      [read_sensor("OIL_TEMP") → 88°C]
      [read_sensor("INTAKE_MANIFOLD_PRESSURE") → 101 kPa]
      [read_sensor("FUEL_RATE") → 1.2 L/h]
      [read_dtc() → nenhum código ativo]
      [get_vehicle_profile() → 47.200 km]
      [check_maintenance(47200) → óleo do motor em 2.800 km]

AURA: Sua Amarok está saudável! Resumo rápido:

  ✓ Motor em marcha lenta normal (780 RPM)
  ✓ Temperatura do líquido de arrefecimento: 91°C (normal)
  ✓ Temperatura do óleo: 88°C (normal)
  ✓ Sem códigos de falha ativos
  ✓ Consumo em marcha lenta: 1.2 L/h (dentro do esperado para o V6 TDI)

  ⚠ Próxima troca de óleo em ~2.800 km (revisão aos 50.000 km).
     Além do óleo e filtro, essa revisão inclui filtro de combustível
     e verificação do sistema AdBlue.

  Quer que eu monitore algo específico durante a próxima viagem?
```

### Scenario 2: Mechanic, boost issue diagnosis
```
User: Cliente reclamando de perda de potência na Amarok V6. O que verificar?

AURA: [read_dtc() → P0299: Turbo/Supercharger Underboost]
      [read_sensor("INTAKE_MANIFOLD_PRESSURE") → 85 kPa at 2500 RPM]
      [query_docs("P0299 underboost Amarok V6 3.0 TDI causas") → 3 chunks]
      [analyze_trend("INTAKE_MANIFOLD_PRESSURE", 60) → consistently low]

AURA: Código P0299 confirmado — turbo entregando pressão abaixo do
esperado. Na Amarok V6, o MAP deveria estar em ~180-220 kPa a 2.500 RPM
com carga. Está lendo 85 kPa (basicamente pressão atmosférica — sem boost).

Diagnóstico por ordem de probabilidade no 3.0 TDI:

1. Atuador da turbina (VTG): problema mais comum na EA897. Verificar
   se o atuador elétrico responde — teste com VCDS/OBDEleven.
2. Vazamento no sistema de pressão: verificar mangueiras do
   intercooler, braçadeiras, tubulação entre turbo e coletor.
3. Válvula de alívio (wastegate): pode estar travada aberta.
4. Sensor MAP defeituoso: menos provável se o motor realmente
   não tem força, mas vale descartar.

Confidence: HIGH | AURA recommends generating a report for the client.
```

### Scenario 3: Engineer, data analysis
```
User: Show me DPF health analysis from today's drive.

AURA: [analyze_trend("DPF_DIFFERENTIAL_PRESSURE", full_session)]
      [analyze_trend("DPF_TEMPERATURE", full_session)]
      [detect_anomaly("DPF_DIFFERENTIAL_PRESSURE")]
      [query_docs("DPF differential pressure normal range 3.0 TDI")]

AURA: DPF analysis — 45-minute session (mixed urban/highway):

  Differential Pressure:
    μ = 8.2 kPa | σ = 2.1 kPa | min = 3.1 | max = 14.8
    Trend: stable (no sustained increase)
    Anomalies: 0

  DPF Temperature:
    μ = 340°C | σ = 85°C | peak = 620°C (passive regen at km 23)
    Regen duration: ~8 min, temperature profile normal

  Assessment:
    DPF differential pressure within healthy range (<15 kPa baseline).
    No soot accumulation trend across last 3 sessions.
    Passive regeneration occurred — 620°C is normal for EA897.
    Soot loading estimate: ~35-40%.
    Next active regen likely within 500-800 km.

  Confidence: HIGH | No action required.
```

---

## 16. Repository Strategy

### Public: `aura-core` (GitHub, AGPL-3.0)

> "Reference architecture for edge AI diagnostic systems"

```
/aura-core
  /aura_core       # Agent, ReAct loop, tool definitions
  /aura_rag        # Chunking, embedding, retrieval pipeline
  /aura_sense      # Telemetry ingestion, anomaly detection
  /aura_edge       # Quantization, routing, profiling utilities
  /simulation      # Anomaly injection, session replay, mock telemetry
  /evaluation      # Eval harness structure, metric definitions
  /docs            # Architecture diagrams, design decisions
  /tests
  README.md
  LICENSE          # AGPL-3.0
```

**Includes:** Architecture, generic pipeline code, simulation mode, mock data, eval framework structure.

**Excludes:** Curated datasets, tuned prompts, real telemetry, exact thresholds, production configs, polished UI.

### Private: `aura-pro` (local / private repo)

- Curated Amarok V6 corpus (cleaned, labeled, quality-tiered)
- Labeled evaluation datasets (80+ queries with ground truth)
- Optimized prompts and router thresholds
- Real driving session recordings
- Anomaly detection calibration values
- Production UI
- Performance benchmark raw data

### Build in Public

**Share:** Architecture decisions, aggregate benchmarks, trade-off analyses, failure mode write-ups.

**Don't share:** Raw datasets, exact prompts, full pipeline configs, real telemetry data.

---

## 17. Tech Stack

```
Language:           Python 3.11+
OBD-II:             python-obd + ELM327 Bluetooth
                    (stretch: python-can + OBDEleven for VAG UDS)
Transcription:      OpenAI Whisper (corpus ingestion)
STT (live):         whisper.cpp (ARM build, base model)
TTS:                Piper TTS (local, pt-br) / OpenAI TTS API (cloud fallback)
VAD:                Silero VAD
Embeddings:         sentence-transformers (BAAI/bge-m3 multilingual)
Vector DB:          ChromaDB (local, SQLite)
Keyword search:     rank_bm25
LLM (edge):         llama-cpp-python → Llama 3.2 3B Q4_K_M
LLM (cloud):        OpenAI / Anthropic API (metered fallback)
Agent:              Custom ReAct (no LangChain)
Anomaly detection:  NumPy/SciPy (z-score, gradient, IQR)
Telemetry storage:  SQLite (time-series per session)
Logging:            SQLite (structured agent traces)
Web UI:             FastAPI + HTMX
Reports:            Jinja2 → Markdown → PDF (weasyprint)
Hardware:           Raspberry Pi 5 8GB + ELM327 v2.1 + USB mic
OS:                 Ubuntu Server 24.04 (arm64)
```

---

## 18. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Amarok V6 limited standard PIDs | Fewer demo scenarios | PID scan is Phase 1 Day 1; adapt scope to available data |
| Boost/DPF PIDs not on standard OBD-II | Lose best diesel scenarios | Budget for OBDEleven (~R$350) as stretch |
| 3B model weak at tool-calling in Portuguese | Agent unreliable in pt-br | Test bilingual early; cloud fallback for pt-br complex queries |
| Pi 5 thermal throttling in car (Brazilian summer) | Degraded performance | Active cooling + shaded mount location |
| Forum content low quality for RAG | Poor retrieval | Curate aggressively; label quality tiers in metadata |
| Scope creep | Never ships | Phase 1 AURA RAG alone is a credible artifact |
| FuelTech hires before project complete | Missed window | Apply after Phase 1 with RAG demo; continue in parallel |
| Whisper pt-br accuracy with engine noise | Poor STT in car | Test with engine on before committing; fallback to text |
| Pi 5 RAM exhausted | OOM crashes | Profile aggressively; mmap models; drop to Whisper tiny |
| Voice-to-voice latency >10s | Poor UX | "Thinking" audio cue; short spoken summary + full text on screen |
| Piper TTS pt-br quality insufficient | Unprofessional demo | Fall back to OpenAI TTS API for video |
| AURA hallucinates unsafe recommendation | Safety risk | Confidence tags + safety rails + post-generation validation |
| Real faults unavailable for demo | Boring video | Simulation mode: anomaly injection + session replay |
| Someone clones repo and competes | IP loss | AGPL-3.0; keep data/configs/prompts private |
