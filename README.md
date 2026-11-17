# 🤖 Developer Profile Intake Assistant

An autonomous, conversational intake assistant powered by a local LLM (`llama.cpp`) and enforced by strict **Pydantic v2** data models. 

Instead of forcing users through rigid, multi-field web forms, this system engages in natural terminal dialogue to gather professional developer profiles. It autonomously detects when the intake session is complete, switches the LLM into a deterministic extraction engine, enforces strict JSON grammar constraints, and validates the output against complex cross-field business rules.

---

## 🏗️ System Architecture & Data Pipeline

The application operates in two distinct phases using a single local inference server:

```text
┌───────────────────┐    Phase 1: Conversational Intake (Temp: 0.7)    ┌───────────────────┐
│                   │ ◄──────────────────────────────────────────────► │                   │
│   Terminal User   │                                                  │  llama.cpp Server │
│    (main.py)      │    Phase 2: Autonomous "Thank you!" Trigger      │ (localhost:8080)  │
└─────────┬─────────┘ ───────────────────────────────────────────────► └─────────┬─────────┘
          │                                                                      │
          │ Passes Chat Transcript                                 Enforces JSON Schema
          ▼                                                                      ▼
┌───────────────────┐   json.loads()   ┌───────────────┐  model_validate() ┌────────────────┐
│   extractor.py    │ ───────────────► │  Python Dict  │ ────────────────► │ DeveloperProfile│
└───────────────────┘                  └───────────────┘                   │   (models.py)   │
                                                                           └────────┬────────┘
                                                                                    │
                                                                                    ▼
                                                                            Pristine JSON Output
