# IRIS v2 — Project Charter

*Signed between Krasus (student, builder) and Claude (mentor, guide). Carried forward from the KaliRisk pact, formally written down 25 September 2026.*

---

## 0. The Pact (unchanged from KaliRisk — this is the whole reason it survives)

Krasus's rules — I accept all of them, same as before:

1. **Go slow.** Teach step by step, grade 3 pupil pace. Every line of code, every function, gets explained — not just shown.
2. **Teach architecture, don't just apply it.** Before we pick a pattern, Krasus learns what the different options are and *why* we're rejecting the others.
3. **Be a mentor, not a robot.** Explanations, analogies, patience. No dumping jargon and walking off.
4. **Architecture integrity.** Once we agree on a structure, we do not abandon it halfway through because it's inconvenient one afternoon. If we ever want to change it, we stop, discuss it properly, and consciously decide — never drift.
5. **Muscle memory.** Krasus types every line himself in his own IDE. Claude shows code in conversation for teaching purposes; he never copy-pastes it into the project.
6. **This is a marathon, not a sprint.** Months, not days. Depth over speed, every time.

My commitments as mentor:

- I will never silently skip a concept because "it's obvious." If something is foundational, we stop and build it properly.
- I will always explain **why**, not just **what** — every decision gets a reason you can repeat back to someone else.
- I will flag it clearly whenever we're about to touch something that breaks our architecture, so drift never sneaks in unnoticed.
- I will use analogies from everyday life (matatus, dukas, caretakers, post offices, school marks) to ground abstract software/finance ideas — and for anything outside econometrics home turf (Docker, Kafka, infra), the plain picture always comes before the jargon.

**Signed:** Krasus ✍️ — Claude 🤖 (mentor mode, permanently on for this project)

---

## 1. The Problem (in plain language first)

You already built and shipped IRIS once — a big 8-model econometric stack analyzing 53 years of Kenya's economy, producing automated policy briefs for the Central Bank's decision-makers. IRIS v2 is not "IRIS but bigger." It's a **rebuild**, done the KaliRisk way — layered, disciplined, tested at every step, nothing tangled.

**Who it's for, this time:** not the Central Bank — they have their own technical teams and aren't a realistic paying customer. This time, IRIS v2 is for people who manage real money: pension funds, banks, asset managers. People who need a real, defensible answer to "if the macro-economy shifts, how much of my portfolio's value is at risk?"

**The eventual dream:** feed IRIS v2 a portfolio's asset allocation, feed it a macro shock scenario, and it outputs Value at Risk, Expected Shortfall, and duration exposure — a genuine macro-aware risk engine.

**But that dream is locked behind one honest, narrow question first.** Before touching forecasting or risk numbers, we must prove something much smaller: **does Kenya's Central Bank Rate (CBR) actually, measurably move KCB Group's share price**, with real statistical confidence — not a "looks like it on a chart" hand-wave. One macro factor. One asset. One rigorous yes-or-no.

Three possible outputs were considered for v1 — (A) the statistical relationship itself, (B) a forecast, (C) a risk/VaR number. B and C are **gated** on A being genuinely significant first. Building a forecast or a risk number on top of an unproven relationship would mean building on sand.

---

## 2. The Data & Statistics Model (the "physics" of this project, no code yet)

This is the world's ground truth — true regardless of what code we write.

### 2.1 The two raw ingredients
- **CBR (Central Bank Rate):** ~124 historical rows, one row per MPC rate-decision meeting, irregular intervals (the MPC doesn't meet on a fixed schedule — roughly six times a year).
- **KCB share price:** one new row per trading day on the Nairobi Securities Exchange.

### 2.2 Core concept: forward-fill alignment
CBR doesn't change daily — it's like a speed-limit sign: it stays exactly the same, day after day, until the MPC officially changes it. To compare CBR against KCB's daily price, we **forward-fill** CBR into a daily series: every day between two MPC meetings just repeats the last known rate. This is the bridge that lets two differently-paced datasets sit side by side.

### 2.3 Core concept: is the relationship real, or coincidental?
Two series can *look* related on a chart purely by chance — both trending upward over years, say, without one actually causing or predicting the other. The rigorous version of "does CBR move KCB" is a **cointegration test**: a formal statistical check for whether two series share a genuine long-run relationship, not just a visual coincidence. We build the full intuition for this properly in Phase 5, with its own plain-language analogy — we don't need the deep mechanics yet, only the shape of the question: real relationship, or illusion?

---

## 3. Software System Architecture (decided, and why)

Same layered discipline as KaliRisk, extended with a streaming ingestion layer because this time data arrives as **events**, not a static CSV we load once.

```
CSV sources → feed producer → Kafka topics → consumer → MySQL (raw) → stats logic → FastAPI → Streamlit
```

**The analogy:** think of a small estate. A **caretaker** (Zookeeper) keeps order. A **post office** (Kafka) sorts incoming letters into labeled pigeonholes. A **records office** (MySQL) writes things down permanently. Further inside the compound, a **back-office analyst** (the `core/` stats layer) does the real econometric thinking — and never once needs to know how the letters arrived. A **front counter** (FastAPI) is the only one allowed to ask the analyst for answers. A **reception display** (Streamlit) shows those answers to visitors — it never walks to the back office itself.

**Our rule going forward, same spirit as KaliRisk's domain-layer rule:** `core/` (the statistics — alignment, cointegration testing) must NEVER import anything about Kafka, MySQL, or HTTP. It must be pure, testable Python that could run with zero broker and zero database connection, fed nothing but a clean pandas DataFrame.

Repo skeleton (already built):
```
iris_v2/
├── ingestion/       ← producer, consumer, toy sandbox
├── data_access/     ← the only code allowed to speak SQL
├── core/            ← alignment.py, cointegration.py — pure logic
├── api/             ← FastAPI, serves core's results only
├── dashboard/       ← Streamlit, talks to api only
├── config/
├── tests/
└── docker-compose.yml
```

---

## 4. Data Engineering Architecture

- **Raw zone:** the MySQL tables the Kafka consumer writes into (`raw_cbr_events`, `raw_kcb_ticks`) — untouched, append-only, exactly as the events arrived. Never edited, same golden rule as KaliRisk's `data/raw/`.
- **Processed zone (Phase 4, not yet built):** the forward-filled, daily-aligned series — a clean DataFrame ready for the statistical test.
- **The golden rule carried over from KaliRisk:** chronological integrity is sacred. No peeking, no shuffling dates out of order, at any stage.

---

## 4.5 What is "the product," for v1?

Deliberately humble, matching the narrowed scope: a clear, honest statistical report answering one question — is CBR → KCB a genuine relationship? Presented via the FastAPI + Streamlit pair, not a full risk dashboard yet. The full two-view (single-relationship / portfolio) dashboard, live what-if sliders, and VaR outputs are **future scope**, unlocked only once Option A is proven and Phases 7+ begin.

---

## 5. Chronological Implementation Roadmap

| Phase | What we build | Status |
|---|---|---|
| **0** | This charter | ✅ Done |
| **1** | Project skeleton — folders, git, Kafka + Zookeeper + MySQL via Docker | ✅ Done — repo restructured, FX experiment removed, layered folders created, `docker-compose.yml` hand-typed and all three containers confirmed running, `toy_producer.py`/`toy_consumer.py` proved a message genuinely travels producer → Kafka → consumer (also surfaced the at-least-once delivery lesson) |
| **2** | Data contract — exact schema for CBR events and KCB ticks | 🔄 Starting next |
| **3** | Validation | Not started |
| **4** | Feature engineering — forward-fill + daily alignment | Not started |
| **5** | The core statistical test — Option A, cointegration | Not started |
| **6** | Reporting the result | Not started |
| **7+** | Gated forecasting/risk work — Options B/C, unlocked only if Phase 5 is genuinely significant | Locked |

We do not jump ahead. Phase 2 does not start until Phase 1 is genuinely solid. That's the whole point of the pact.

---

## Next session

Continuing **Phase 1**: `docker-compose.yml`, hand-typed, one house at a time. Zookeeper's image is named — his door number (`ports`) comes next.
