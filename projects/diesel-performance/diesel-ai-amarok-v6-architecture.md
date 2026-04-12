# AutoDiag AI — FuelTech Portfolio Project (Amarok V6 Edition)

**Project:** AI-powered diagnostic assistant for turbodiesel truck  
**Vehicle:** VW Amarok V6 3.0 TDI (2021+, stock OEM ECU)  
**Target Roles:** Especialista de IA — Sistemas Conversacionais | Especialista de IA — Análise de Dados & Modelos Especializados  
**Target Company:** FuelTech  
**Author:** Guilherme  
**Status:** Planning

---

## 1. Strategic Alignment

This project demonstrates every core competency from both FuelTech AI roles using a real vehicle as the test platform. The Amarok V6 3.0 TDI is ideal: modern CAN bus with rich PID support, turbodiesel complexity (boost, EGT, DPF, injector balance), and a large Brazilian owner community generating domain-specific content for the RAG corpus.

Although the vehicle runs a stock OEM ECU (not FuelTech), the skills demonstrated are directly transferable: the diagnostic reasoning, document retrieval, sensor analysis, and edge deployment are ECU-agnostic. The project narrative to FuelTech: *"I built the AI layer your customers would interact with — here it is working on a real vehicle."*

### Role 1 — Conversational AI Systems

| Job Requirement | Project Component |
|-----------------|-------------------|
| RAG pipelines for large-scale technical docs | VW/Amarok service manuals, TDI technical docs, diesel tuning guides, community knowledge |
| AI agent orchestration solving real user problems | Tool-calling agent: diagnose DTCs, explain sensor data, recommend maintenance |
| Chat with memory, persistent context, personalization | Vehicle profile (Amarok V6 specs), session history, user skill adaptation |
| Evaluate and integrate different LLMs (quality/cost/latency) | Benchmark matrix: edge models vs cloud APIs on automotive QA |
| Automatic report generation from data | Telemetry session reports with anomaly flags and maintenance recommendations |
| Cost control strategies per user profile | Edge/cloud routing based on query complexity |
| Prompt engineering, function calling, tool use | Custom ReAct agent with 8 structured tools |

### Role 2 — Data Analysis & Specialized Models

| Job Requirement | Project Component |
|-----------------|-------------------|
| Anomaly detection in large data volumes | Real-time anomaly detection on diesel-specific sensors (EGT, boost, DPF differential pressure) |
| Fine-tune specialized models | Fine-tuned DTC classifier / severity ranker on labeled automotive data |
| Actionable recommendations from raw data | "Boost pressure dropping at altitude — turbo actuator may need inspection" |
| Parsers/pipelines for diverse data formats | OBD-II PID decoder, VW-specific extended PIDs, PDF manual parser, forum scraper |
| Lightweight models on mobile/edge | Quantized LLM + anomaly detector on Raspberry Pi 5 |
| Edge/embedded deployment optimization | GGUF quantization, latency profiling, RAM budgeting |
| Validate AI outputs against real-world constraints | Cross-check against VW service intervals, safe operating ranges for 3.0 TDI |


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
│  │  OBD-II port │───▶│  DATA INGESTION LAYER                  │ │
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
│  │  AI AGENT CORE                                              │ │
│  │                                                              │ │
│  │  ┌────────────────────┐  ┌────────────────────────────────┐ │ │
│  │  │  RAG ENGINE        │  │  AGENT (ReAct + Tool Calling)  │ │ │
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
│  │  │  BGE-small embed.  │  │                                │ │ │
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
│  │  LLM INFERENCE                                               │ │
│  │  LOCAL: llama-cpp-python (Llama 3.2 3B Q4_K_M)              │ │
│  │  CLOUD: OpenAI / Anthropic API (fallback for complex Qs)    │ │
│  │  Router: complexity classifier → edge or cloud               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  UI: FastAPI + Web (phone connects via Pi WiFi AP)           │ │
│  │  • Chat interface with persistent session                    │ │
│  │  • Live sensor dashboard (boost, EGT, oil temp, DPF)        │ │
│  │  • Session report export (PDF)                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

---

## 5. Document Corpus (RAG)

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

### Diesel-Specific Anomaly Detection

| Sensor | Anomaly Type | Method | Alert Example |
|--------|-------------|--------|---------------|
| Boost pressure | Underboost / overboost | Expected vs actual MAP at RPM/load | "Boost 15% below target at 3k RPM — check turbo actuator" |
| Oil temperature | Overheat trend | Gradient threshold (>2°C/min sustained) | "Oil temp rising fast — reduce load, check oil level" |
| DPF diff. pressure | Clogging trend | Rolling mean increase over sessions | "DPF pressure trending up — forced regen may be needed soon" |
| Coolant temperature | Thermostat stuck | Flat-line detection (never reaching operating temp) | "Coolant not reaching 90°C after 15min — thermostat stuck open?" |
| Fuel rate | Efficiency degradation | Session-over-session comparison at similar driving patterns | "Fuel consumption up 12% vs last month at similar load" |
| Intake air temp | Intercooler degradation | IAT vs ambient delta at boost | "Intake air 25°C above ambient under boost — intercooler efficiency degraded" |

---

## 7. Session Memory & Personalization

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
    current_km: int = 0          # updated each session via OBD PID
    modifications: list = field(default_factory=list)  # stock
    service_history: list = field(default_factory=list)
    known_issues: list = field(default_factory=list)

@dataclass  
class SessionContext:
    vehicle: VehicleProfile
    user_skill: str              # "owner" | "mechanic" | "engineer"
    conversation_history: list   # sliding window, last 20 turns
    session_telemetry: dict      # sensor time-series for this session
    active_dtcs: list
    previous_reports: list       # links to past session reports
```

**Personalization:**
- `owner`: Portuguese, plain language, "leve ao mecânico" recommendations, safety-first
- `mechanic`: Technical pt-br, part numbers, diagnostic procedures, tool references
- `engineer`: Raw data, statistical details, CAN protocol references, English technical terms

---

## 8. LLM Evaluation & Cost Routing

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

---

## 9. Phased Build Plan

### Phase 1: PID Discovery + RAG Pipeline (Weeks 1–2)
> **Deliverable:** Validated PID list for your Amarok + working RAG over diesel/Amarok docs.

- [ ] **Week 1 Day 1:** Buy cheap ELM327 BT + install Torque/Car Scanner → full PID scan on Amarok
- [ ] Document every responding PID with values at idle and driving
- [ ] Collect corpus: Amarok manual, TDI docs, DTC databases, forum threads, YT transcripts
- [ ] Implement chunking pipeline (section-aware + DTC-structured + forum Q&A pairs)
- [ ] Embed + store in ChromaDB, implement hybrid retrieval
- [ ] Build eval dataset: 80+ queries (pt + en), Amarok-specific and general diesel
- [ ] Measure Precision@5, MRR, Hit Rate — iterate
- [ ] Benchmark 4 LLMs on 30 automotive diagnostic questions

### Phase 2: Agent + Live OBD-II + Memory (Weeks 3–4)
> **Deliverable:** Agent on laptop connected to Amarok via ELM327, full tool suite working.

- [ ] Implement all 8 tools with python-obd backend
- [ ] Build ReAct agent loop (custom, no LangChain)
- [ ] Implement session memory + vehicle profile (hardcoded Amarok V6 specs)
- [ ] Implement diesel anomaly detection (boost, oil temp, DPF pressure, coolant)
- [ ] Implement maintenance schedule checker (VW intervals for Amarok)
- [ ] Implement report generation
- [ ] Test in car: idle diagnostics, driving session, DTC scenarios
- [ ] Log all agent traces for debugging

### Phase 3: Edge Deployment + Router (Weeks 5–6)
> **Deliverable:** Full system on Pi 5, mounted in Amarok, phone UI via WiFi.

- [ ] Set up Pi 5, llama-cpp-python ARM, port full stack
- [ ] Implement edge/cloud complexity router
- [ ] Profile: latency per tool, RAM usage, thermal under sustained use
- [ ] Build FastAPI web UI: chat + live sensor dashboard
- [ ] Configure Pi as WiFi AP (phone connects to "AutoDiag-Amarok")
- [ ] Mount Pi in car (12V→USB-C power from accessory outlet)
- [ ] Stress test: 30+ min drive with continuous monitoring
- [ ] Document edge vs cloud accuracy delta

### Phase 4: Demo Video + Portfolio (Week 7)
> **Deliverable:** Video recorded in/with the Amarok + polished GitHub repo.

**Video script outline:**
1. Hardware overview: Pi 5 + ELM327 + Amarok engine bay shot
2. Connection: plug ELM327, boot Pi, phone connects to WiFi
3. Demo 1: "What's the status of my truck?" → agent reads sensors, reports health
4. Demo 2: Simulate/trigger a DTC → agent diagnoses with RAG context
5. Demo 3: "Analyze my boost pressure from this drive" → trend analysis + anomaly check
6. Demo 4: "When is my next service?" → maintenance schedule from km reading
7. Show generated PDF report
8. Architecture walkthrough (brief, screen recording of code/diagram)

- [ ] Record and edit video (5-8 min target)
- [ ] Clean GitHub repo: README, architecture diagram, benchmarks, setup guide
- [ ] Technical blog post
- [ ] Publish, share with FuelTech

### Phase 5: Voice Input — Hands-Free Queries (Week 8)
> **Deliverable:** Speak to the system, read the answer on screen. Hands-free in-car interaction.  
> **Hardware:** Pi 5 (existing) + USB microphone (~R$30-50)

**Interaction flow:**
```
Driver speaks → USB mic → Whisper.cpp (local STT) → Agent → Text on phone screen
```

- [ ] Install whisper.cpp ARM build on Pi 5
- [ ] Benchmark STT models on Pi: tiny (~1s), base (~2-3s), small (~5-8s) — pick best latency/accuracy tradeoff
- [ ] Test Portuguese recognition quality (Whisper is strong in pt-br)
- [ ] Implement push-to-talk via web UI button (phone screen) or wake word
- [ ] Add voice activity detection (VAD) with Silero VAD to auto-detect speech boundaries
- [ ] Integrate into FastAPI: mic stream → STT → agent pipeline → text response
- [ ] Test in-car with engine running (road noise, diesel idle noise, A/C fan)
- [ ] Profile total latency: speech end → response displayed

**Model sizing on Pi 5 (RAM budget):**

| Whisper Model | Size | RAM | Latency (5s audio, Pi 5) | Portuguese Quality |
|---------------|------|-----|--------------------------|-------------------|
| tiny | 39M | ~150 MB | ~1s | Acceptable for short commands |
| base | 74M | ~300 MB | ~2-3s | Good |
| small | 244M | ~800 MB | ~5-8s | Very good |

> With LLM (3B Q4 ≈ 2GB) + ChromaDB + Whisper base, total RAM ~3.5-4GB — fits in 8GB Pi 5.

**Wake word options (stretch):**
- OpenWakeWord (local, ~50MB) — custom "Hey Amarok" trigger
- Simple alternative: physical button on dashboard, or tap phone screen

### Phase 6: Voice-to-Voice — Full Conversational Loop (Weeks 9-10)
> **Deliverable:** Speak a question, hear the answer. True conversational AI copilot in the truck.  
> **This is the "wow factor" demo phase.**

**Interaction flow:**
```
Driver speaks → Whisper.cpp (STT) → Agent → TTS engine → Car speakers / Bluetooth
```

**The TTS challenge on edge:**

Running quality TTS on Pi 5 alongside the LLM and Whisper is the hardest resource constraint in the project. Options in order of feasibility:

| TTS Option | Location | Quality | Latency | RAM | Cost |
|------------|----------|---------|---------|-----|------|
| Piper TTS | Edge (Pi 5) | Good (pt-br voices available) | ~1-2s for short responses | ~100-200 MB | Free |
| Coqui XTTS-v2 | Edge (needs GPU) | Excellent, natural | Too slow on Pi 5 CPU | ~2 GB | Free |
| OpenAI TTS API | Cloud | Excellent | ~1s + network | 0 (cloud) | ~$0.015/1K chars |
| ElevenLabs API | Cloud | Best quality | ~1-2s + network | 0 (cloud) | ~$0.018/1K chars |
| Edge TPU / Coral accelerator | Edge | Good | ~0.5-1s | Offloaded | ~R$300-500 |

**Recommended path:** Start with **Piper TTS** (local, free, has pt-br voices). If quality is insufficient for the demo, fall back to **OpenAI TTS API** for the video recording.

- [ ] Install Piper TTS on Pi 5, test pt-br voice models
- [ ] Implement response summarization: full text → short spoken summary (agent generates both)
- [ ] Audio output routing: Pi 5 → Bluetooth to Amarok's stereo, or 3.5mm to aux input
- [ ] Implement streaming TTS: start speaking as tokens generate (reduces perceived latency)
- [ ] Profile end-to-end latency: speech end → first audio output
- [ ] Handle long responses: speak summary, display full detail on phone screen
- [ ] Test in-car: engine noise, speaker volume, conversation flow
- [ ] Record demo video with voice-to-voice interaction

**Response strategy for voice output:**

The agent should generate two response formats per turn:
```python
@dataclass
class AgentResponse:
    spoken: str    # Short, conversational — what gets sent to TTS
    detailed: str  # Full text with data tables, stats — displayed on screen
```

Example:
- **Spoken:** "Sua Amarok está saudável. Sem códigos de falha. Próxima troca de óleo em 2.800 quilômetros."
- **Detailed:** [Full sensor table, maintenance breakdown, recommendations — on phone screen]

This avoids TTS reading out tables and statistics, which sounds terrible.

---

## Hardware Upgrade Path for Voice-to-Voice

### Tier 1: Minimal Voice (Phase 5 only) — +R$50

| Component | Cost | Purpose |
|-----------|------|---------|
| USB microphone (condenser, omnidirectional) | ~R$30-50 | Speech capture in cabin |

### Tier 2: Full Voice-to-Voice on Pi 5 (Phase 6) — +R$150-250

| Component | Cost | Purpose |
|-----------|------|---------|
| USB microphone | ~R$30-50 | Speech capture |
| 3.5mm aux cable or BT audio transmitter | ~R$20-40 | Audio out to Amarok stereo |
| (Optional) USB sound card | ~R$30 | Better audio I/O than Pi's onboard |
| (Optional) Small speaker (for standalone mode) | ~R$50-80 | If not using car stereo |

### Tier 3: Performance Upgrade for Real-Time Voice (Phase 6+) — +R$800-2500

If Pi 5 CPU can't handle Whisper + LLM + TTS concurrently:

| Component | Cost | Benefit |
|-----------|------|---------|
| Coral USB Accelerator (Edge TPU) | ~R$300-500 | Offload Whisper inference to dedicated TPU |
| NVIDIA Jetson Orin Nano (8GB) | ~R$1500-2500 | GPU inference for all models; 10-20x faster TTS/STT |
| NVMe SSD hat for Pi 5 | ~R$150-200 | Faster model loading, swap performance |

> **Honest assessment:** Voice-to-voice with Piper TTS on Pi 5 is feasible but will have noticeable latency (~5-8s total from speech end to audio start). The Jetson Orin Nano would bring this under 3s but nearly triples the hardware budget. For the demo video, you can mitigate perceived latency with a "thinking" audio cue while the agent processes.

### Target End-to-End Latency (Voice-to-Voice)

| Stage | Pi 5 (CPU only) | Pi 5 + Coral TPU | Jetson Orin Nano |
|-------|-----------------|------------------|------------------|
| STT (Whisper, 5s audio) | ~2-3s (base) | ~0.5-1s (offloaded) | ~0.3-0.5s |
| Agent + RAG + Tools | ~3-5s | ~3-5s | ~2-3s |
| TTS (Piper, short response) | ~1-2s | ~1-2s | ~0.5-1s |
| **Total** | **~6-10s** | **~4.5-8s** | **~3-4.5s** |

> For reference: Alexa/Google Assistant target <3s. 6-10s is usable but not snappy. The "thinking chime" UX pattern helps.

---

## 10. Demo Scenarios (Amarok-Specific)

### Scenario 1: Owner, routine check (Portuguese)
```
User: Como está meu carro?

Agent: [read_sensor("RPM") → 780]
       [read_sensor("COOLANT_TEMP") → 91°C]
       [read_sensor("OIL_TEMP") → 88°C]
       [read_sensor("INTAKE_MANIFOLD_PRESSURE") → 101 kPa]
       [read_sensor("FUEL_RATE") → 1.2 L/h]
       [read_dtc() → nenhum código ativo]
       [get_vehicle_profile() → 47.200 km]
       [check_maintenance(47200) → óleo do motor em 2.800 km]

Agent: Sua Amarok está saudável! Resumo rápido:

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

Agent: [read_dtc() → P0299: Turbo/Supercharger Underboost]
       [read_sensor("INTAKE_MANIFOLD_PRESSURE") → 85 kPa at 2500 RPM]
       [query_docs("P0299 underboost Amarok V6 3.0 TDI causas") → 3 chunks]
       [analyze_trend("INTAKE_MANIFOLD_PRESSURE", 60) → consistently low]

Agent: Código P0299 confirmado — turbo entregando pressão abaixo do
esperado. Na Amarok V6, o MAP deveria estar em ~180-220 kPa a 2.500 RPM
com carga. Está lendo 85 kPa (basicamente pressão atmosférica — sem boost).

Diagnóstico por ordem de probabilidade no 3.0 TDI:

1. **Atuador da turbina (VTG):** problema mais comum na EA897. Verificar
   se o atuador elétrico responde — teste com VCDS/OBDEleven no bloco
   de medição do turbo.
2. **Vazamento no sistema de pressão:** verificar mangueiras do
   intercooler, braçadeiras, e a tubulação entre turbo e coletor.
3. **Válvula de alívio (wastegate):** pode estar travada aberta.
4. **Sensor MAP defeituoso:** menos provável se o motor realmente
   não tem força, mas vale descartar.

Procedimento recomendado: com motor em marcha lenta, fechar a saída do
intercooler e acelerar brevemente — se o turbo gera pressão, o problema
é vazamento downstream. Se não gera, o problema é no turbo/atuador.

Quer que eu gere um relatório com esses dados para o cliente?
```

### Scenario 3: Engineer, data analysis
```
User: Show me DPF health analysis from today's drive.

Agent: [analyze_trend("DPF_DIFFERENTIAL_PRESSURE", full_session)]
       [analyze_trend("DPF_TEMPERATURE", full_session)]
       [detect_anomaly("DPF_DIFFERENTIAL_PRESSURE")]
       [query_docs("DPF differential pressure normal range 3.0 TDI")]

Agent: DPF analysis — 45-minute session (mixed urban/highway):

  Differential Pressure:
    μ = 8.2 kPa | σ = 2.1 kPa | min = 3.1 | max = 14.8
    Trend: stable (no sustained increase)
    Anomalies: 0

  DPF Temperature:
    μ = 340°C | σ = 85°C | peak = 620°C (passive regen detected at km 23)
    Regen duration: ~8 min, temperature profile normal

  Assessment:
    DPF differential pressure within healthy range (<15 kPa baseline).
    No soot accumulation trend detected across last 3 sessions.
    Passive regeneration occurred — exhaust temp reached 620°C which
    is normal for EA897 passive regen cycle.

    Soot loading estimate (from diff pressure curve): ~35-40%.
    Active regen typically triggers at ~45% on this ECU calibration.
    Next active regen likely within 500-800 km if driving pattern
    continues.

  No action required.
```

---

## 11. Hardware & Cost

| Component | Est. Cost (BRL) | Notes |
|-----------|-----------------|-------|
| Raspberry Pi 5 8GB | ~R$500 | |
| MicroSD 64GB A2 | ~R$50 | |
| ELM327 Bluetooth v2.1 | ~R$40 | For PID discovery + Phase 1-2 |
| USB-C PD car charger | ~R$60 | 12V cigarette lighter → USB-C |
| Case + active cooling | ~R$40 | |
| **Total (MVP)** | **~R$690** | |
| (Optional) OBDEleven adapter | ~R$350 | For VAG-specific UDS PIDs (stretch goal) |

---

## 12. Tech Stack

```
Language:           Python 3.11+
OBD-II:             python-obd + ELM327 Bluetooth
                    (stretch: python-can + OBDEleven for VAG UDS)
Transcription:      OpenAI Whisper (corpus ingestion)
STT (live):         whisper.cpp (ARM build, base model for Pi 5)
TTS:                Piper TTS (local, pt-br) / OpenAI TTS API (cloud fallback)
VAD:                Silero VAD (voice activity detection)
Embeddings:         sentence-transformers (BGE-small-en-v1.5 or BGE-m3 for bilingual)
Vector DB:          ChromaDB (local, SQLite)
Keyword search:     rank_bm25
LLM (edge):         llama-cpp-python → Llama 3.2 3B Q4_K_M
LLM (cloud):        OpenAI / Anthropic API (metered fallback)
Agent:              Custom ReAct (no LangChain)
Anomaly detection:  NumPy/SciPy (z-score, gradient, IQR)
Telemetry storage:  SQLite (time-series per session)
Web UI:             FastAPI + HTMX
Reports:            Jinja2 → Markdown → PDF (weasyprint)
Hardware:           Raspberry Pi 5 8GB + ELM327 v2.1 + USB mic
OS:                 Ubuntu Server 24.04 (arm64)
```

---

## 13. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Amarok V6 limited standard PIDs | Fewer demo scenarios | PID scan is Phase 1 Day 1; adapt scope to available data |
| Boost/DPF PIDs not on standard OBD-II | Lose best diesel scenarios | Budget for OBDEleven (~R$350) as stretch; design demos around available PIDs |
| 3B model weak at tool-calling in Portuguese | Agent unreliable in pt-br | Test bilingual early; cloud fallback for pt-br complex queries |
| Pi 5 thermal throttling in car (Brazilian summer) | Degraded performance | Active cooling + mount in shaded/ventilated spot, not engine bay |
| Forum content low quality for RAG | Poor retrieval on community queries | Curate aggressively; label quality tiers in metadata |
| Scope creep | Never ships | Phase 1 RAG alone is a credible application artifact |
| FuelTech hires before project complete | Missed window | Apply after Phase 1 with RAG demo; continue building in parallel |
| Whisper pt-br accuracy with diesel engine noise | Poor STT in car | Test with engine on before committing to voice; fallback to text input |
| Pi 5 RAM exhausted (LLM + Whisper + TTS + ChromaDB) | OOM crashes | Profile aggressively; mmap models; drop to Whisper tiny if needed |
| Voice-to-voice latency too high (>10s) | Poor UX | Implement "thinking" audio cue; speak short summary, display full detail |
| Piper TTS pt-br voice quality insufficient | Unprofessional demo | Fall back to OpenAI TTS API for video recording |
