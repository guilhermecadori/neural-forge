# diesel-performance

> **Status:** Planning — no implementation yet.

AURA (Automotive Understanding & Reasoning Agent) — an edge AI copilot for vehicle diagnostics under resource constraints, built around a VW Amarok V6 3.0 TDI as the test platform. Combines OBD-II telemetry ingestion, a RAG corpus over automotive documentation, a quantized LLM on a Raspberry Pi 5, and an STT/TTS voice loop.

## Architecture

Full subsystem breakdown (AURA Core, Sense, RAG, Edge, Voice) and role-alignment rationale live in [`AURA-diesel-ai-amarok-v6-architecture.md`](AURA-diesel-ai-amarok-v6-architecture.md).

## Next steps

Once implementation starts, this README will be replaced with the standard 5-section project README (Problem & Business Metric, Architecture, Prerequisites, Installation & Setup with `dvc pull`, Results) defined in [`templates/ml-project/README.md`](../../templates/ml-project/README.md).
