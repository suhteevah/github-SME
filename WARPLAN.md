# WAR PLAN — SME Discussion Call
**Call:** Discussion with SME — GitHub
**When:** Saturday April 11, 05:30 IST (~8:00 PM EDT Friday April 10)
**Duration:** 30 min
**Meet:** https://meet.google.com/ton-aqcr-sjh
**Dial-in:** +1 267-401-1462, PIN: 550 512 234#
**Contact:** Priyasha Sharma

---

## OBJECTIVE

Demonstrate SME authority across the 7 assigned courses, lock in top-5 course assignments, push for Special tier ($360/course), and walk out with a first course package. Secondary: commit to the 1-min intro video by end of weekend.

---

## THE POSITION

**7 courses, 4 domains, all GitHub-tool-focused:**

| # | Domain | Course | Duration | Priority |
|---|--------|--------|----------|----------|
| 1 | DevOps & Automation | **Manage Code with Git Bots** | 1.5h | #1 |
| 2 | API & App Engineering | **Build & Document Microservice** | 2h | #2 |
| 3 | Distributed AI | **Scale Tasks Asynchronously** | 1.5h | #3 |
| 4 | Observability & Governance | **Enforce AI Guardrails** | 1.5h | #4 |
| 5 | DevOps & Automation | **Test Agent Outputs** | 1.5h | #5 |
| 6 | DevOps & Automation | Automate Issue Summaries | 1.5h | #6 |
| 7 | Observability & Governance | Trace & Scale Latency | 1.5h | #7 |

**Revenue math:** Top 5 × $360 = **$1,800** at Special tier. All 7 = **$2,520**.

---

## SECRET WEAPON — WHAT YOU'VE ALREADY BUILT

You don't just talk about these topics — you have a working AI agent pipeline that embodies most of them. Reference it naturally:

- **Course review agent pipeline** — 6 specialized agents, 6 content types, 6 quality gates
- **OpenClaw inference fleet** — multi-GPU tiered routing (P40 / RTX 3070 Ti / RTX 3050)
- **Automated file classification** via marker scoring
- **Quality gates:** code execution, link validation, version checks, terminology consistency
- **Domain-configurable** review criteria (GitHub, Stripe)

**The one-liner if they ask "why you":**
> "I don't just review course content — I built an AI agent pipeline that validates every code sample, every quiz answer, every link, and every version reference before I start my human review pass. You're getting the SME AND the infrastructure."

---

## COURSE-BY-COURSE DAY ONE SKELETONS

These are your Day 1 (first 20-30 min of content) talking points for each course. Walk in ready to pitch any of them off-the-cuff.

---

### COURSE 1 — Manage Code with Git Bots (1.5h)

**Learning objectives (Day 1):**
- Define what a "Git bot" is and distinguish bots from manual automation
- Identify the 3 bot architectures: GitHub Apps, GitHub Actions, Webhooks
- Build a working auto-labeling bot in < 15 min

**Opening hook:**
> "Every team has the same problem: PRs pile up, humans get tired, and the 3 AM bug slips through because nobody noticed the typo in the config file. Bots don't get tired. They don't skip the boring checks. Today we're going to build the first member of your tireless team."

**Day 1 concepts:**
1. **What is a Git bot?** — Any automated actor with a GitHub identity that can read/write repo state
2. **Three architectures:**
   - GitHub Actions (runs in workflow runners, simplest)
   - GitHub Apps (first-class bot identity, required for cross-repo or marketplace)
   - Webhooks + custom server (most flexible, most ops burden)
3. **The bot-human collaboration model** — bots handle the repetitive 80%, humans make the judgment calls on the 20%

**Day 1 hands-on lab (working code):**
```yaml
# .github/workflows/auto-label.yml
name: Auto-label PRs
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

```yaml
# .github/labeler.yml
documentation:
  - changed-files:
    - any-glob-to-any-file: ['docs/**', '**/*.md']
backend:
  - changed-files:
    - any-glob-to-any-file: 'src/api/**'
tests:
  - changed-files:
    - any-glob-to-any-file: 'tests/**'
```

**Day 1 takeaway:** "You now have a bot that labels every PR automatically based on which files changed. Tomorrow we'll teach it to comment, assign reviewers, and enforce rules."

**Your credibility drop:**
> "I'm literally running an agent pipeline that classifies files by type and routes them to specialized reviewers — this is the same pattern this course teaches, just applied to course content instead of code."

---

### COURSE 2 — Build & Document Microservice (2h)

**Learning objectives (Day 1):**
- Distinguish monolith from microservice and identify when to split
- Define service boundaries using the single-responsibility principle
- Scaffold a FastAPI service with auto-generated OpenAPI documentation

**Opening hook:**
> "In 2008, Netflix was a monolith. One codebase, one deploy, one database. By 2012, they were running 500+ microservices. What changed? Scale broke them. But here's the thing nobody tells you: most teams don't actually need microservices. Today we're going to build one anyway — because you need to know HOW before you can decide WHEN."

**Day 1 concepts:**
1. **Monolith vs microservice** — coupling, deployability, team boundaries
2. **The service boundary question** — if you can't describe what a service does in one sentence, it's too big
3. **The API contract IS the product** — internal consumers trust your docs or they don't use your service
4. **OpenAPI (fka Swagger)** — the contract format that generates docs, SDKs, and tests for free

**Day 1 hands-on lab (working code):**
```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(
    title="Task Service",
    description="A minimal task management microservice",
    version="0.1.0",
)

class Task(BaseModel):
    id: str
    title: str
    done: bool = False

class TaskCreate(BaseModel):
    title: str

_tasks: dict[str, Task] = {}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    """Create a new task."""
    task = Task(id=str(uuid4()), title=payload.title)
    _tasks[task.id] = task
    return task

@app.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    """List all tasks."""
    return list(_tasks.values())

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    """Retrieve a task by id."""
    if task_id not in _tasks:
        raise HTTPException(404, "Task not found")
    return _tasks[task_id]
```

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
# Open http://localhost:8000/docs — live OpenAPI documentation, FREE
```

**Day 1 takeaway:** "You have a running microservice with interactive API docs. Your docs are generated from code, so they can never drift. Tomorrow: service-to-service communication and contract testing."

**Your credibility drop:**
> "My review pipeline itself follows microservice principles — each agent has a single responsibility, a defined API contract, and they compose into a larger workflow. That's the pattern this course teaches."

---

### COURSE 3 — Scale Tasks Asynchronously (1.5h)

**Learning objectives (Day 1):**
- Distinguish synchronous from asynchronous execution models
- Identify which tasks benefit from async (I/O-bound) vs not (CPU-bound without workers)
- Build a working async task queue using Python + Redis

**Opening hook:**
> "Imagine a restaurant with one waiter. A customer orders a steak. The waiter walks to the kitchen, waits 20 minutes, brings the steak back. Meanwhile, 30 customers are standing at the door. That's synchronous execution. Now imagine the waiter takes the order, hands it to the kitchen, and immediately takes the next order. The kitchen calls when food is ready. That's async. Today we're building the async waiter."

**Day 1 concepts:**
1. **The blocking problem** — every sync I/O call freezes the entire thread
2. **Two async models:**
   - **Event loop** (Python asyncio, Node.js) — single thread, cooperative
   - **Task queue + workers** (Celery, RQ, Sidekiq) — distributed, durable
3. **When to use which:** event loop for high-concurrency web servers; task queue for long-running background work
4. **Durability matters** — if your queue loses tasks on restart, you don't have async, you have hope

**Day 1 hands-on lab (working code):**
```python
# tasks.py
from celery import Celery
import time

app = Celery('tasks', broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task
def process_image(image_url: str) -> dict:
    """Simulate a slow image processing job."""
    time.sleep(5)  # stand-in for real work
    return {"url": image_url, "status": "processed"}
```

```python
# dispatch.py
from tasks import process_image

# Fire off 10 jobs — returns immediately, work happens in workers
jobs = [process_image.delay(f"img_{i}.jpg") for i in range(10)]

# Collect results when you actually need them
for job in jobs:
    print(job.get(timeout=30))
```

```bash
# Terminal 1: start Redis
redis-server

# Terminal 2: start Celery worker
celery -A tasks worker --loglevel=info

# Terminal 3: dispatch jobs
python dispatch.py
```

**Day 1 takeaway:** "You have a working async task queue. Ten image jobs finish in ~5 seconds instead of 50. Tomorrow: scaling workers, retries, and dead-letter queues."

**Your credibility drop:**
> "I run a multi-GPU inference fleet — OpenClaw — that routes tasks asynchronously by complexity tier. Heavy analysis to P40s, quick checks to RTX 3070 Ti, portable work to RTX 3050. This isn't theory for me, it's my day job."

---

### COURSE 4 — Enforce AI Guardrails (1.5h)

**Learning objectives (Day 1):**
- Define the 4 categories of AI failures: hallucination, injection, leakage, drift
- Identify where guardrails belong: input, output, runtime, observability
- Build a working guardrail layer that blocks PII leakage from an LLM response

**Opening hook:**
> "Last year, Air Canada was ordered by a Canadian tribunal to honor a refund policy that their AI chatbot invented. The chatbot hallucinated a bereavement policy that didn't exist. The court ruled Air Canada was liable for what its bot said. This is the world we're living in now — your LLM is a legal entity you're responsible for. Guardrails are how you stay out of court."

**Day 1 concepts:**
1. **The 4 AI failure modes:**
   - **Hallucination** — confidently wrong output
   - **Prompt injection** — user overrides system instructions
   - **Data leakage** — model exposes PII, secrets, or training data
   - **Drift** — model behavior changes over time or across versions
2. **Where guardrails live:**
   - **Input guardrails** — validate before sending to model (schema, PII, toxicity)
   - **Output guardrails** — validate model responses (format, groundedness, safety)
   - **Runtime guardrails** — rate limits, cost caps, circuit breakers
   - **Observability guardrails** — detect drift and anomalies after the fact
3. **Deterministic vs probabilistic enforcement** — regex/schema checks are free and reliable; LLM-as-judge is powerful but itself fallible

**Day 1 hands-on lab (working code):**
```python
# guardrails.py
import re
from dataclasses import dataclass
from typing import Callable

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_RE = re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

@dataclass
class GuardrailViolation(Exception):
    category: str
    detail: str

def redact_pii(text: str) -> str:
    """Output guardrail: redact PII from model responses."""
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = SSN_RE.sub("[SSN]", text)
    return text

def block_injection(user_input: str) -> None:
    """Input guardrail: block obvious prompt injection attempts."""
    patterns = [
        "ignore previous instructions",
        "disregard the above",
        "system prompt",
        "you are now",
    ]
    lowered = user_input.lower()
    for pattern in patterns:
        if pattern in lowered:
            raise GuardrailViolation("injection", f"Matched: {pattern}")

def enforce_length(text: str, max_chars: int = 2000) -> None:
    """Runtime guardrail: cap input length to control cost."""
    if len(text) > max_chars:
        raise GuardrailViolation("length", f"{len(text)} > {max_chars}")

# Usage
def safe_llm_call(user_input: str, llm: Callable[[str], str]) -> str:
    enforce_length(user_input)
    block_injection(user_input)
    raw_response = llm(user_input)
    return redact_pii(raw_response)
```

**Day 1 takeaway:** "You have three working guardrails: input validation, injection detection, and output redaction. Tomorrow: groundedness checking, LLM-as-judge evaluation, and observability."

**Your credibility drop:**
> "My content review pipeline has guardrails at every layer — low-temperature inference for accuracy-critical work, mandatory human escalation flags, and quality gates that block submission until all checks pass. Guardrails aren't optional for production AI."

---

### COURSE 5 — Test Agent Outputs (1.5h)

**Learning objectives (Day 1):**
- Explain why traditional unit testing fails for LLM-generated output
- Distinguish deterministic assertions from semantic evaluation
- Build a golden-dataset regression harness with pytest

**Opening hook:**
> "If I ask an LLM 'what's the capital of France' ten times, I might get 'Paris', 'Paris.', 'The capital of France is Paris', or 'Paris is the capital.' All correct. All different strings. Your `assertEqual` just died. Today we're going to talk about how to actually test the thing that refuses to give you the same answer twice."

**Day 1 concepts:**
1. **The determinism problem** — LLMs are stochastic; strict equality assertions are brittle
2. **Three evaluation strategies:**
   - **Deterministic checks** — schema, format, required fields (fast, cheap, high-signal)
   - **Semantic similarity** — embedding distance from reference (moderate cost)
   - **LLM-as-judge** — use another LLM to grade the response (expensive, powerful, itself fallible)
3. **Golden datasets** — curated input/output pairs that represent your quality bar
4. **Regression testing for agents** — run the dataset after every prompt or model change, flag any drop in pass rate

**Day 1 hands-on lab (working code):**
```python
# test_agent.py
import json
import pytest
from pathlib import Path

# Your agent under test
def classify_intent(user_message: str) -> dict:
    # ... real implementation calls LLM ...
    return {"intent": "greeting", "confidence": 0.95}

# Golden dataset — what "correct" looks like
GOLDEN = [
    {"input": "hello there", "expected_intent": "greeting"},
    {"input": "cancel my order", "expected_intent": "cancellation"},
    {"input": "where is my package", "expected_intent": "shipping_status"},
    {"input": "thanks bye", "expected_intent": "farewell"},
]

@pytest.mark.parametrize("case", GOLDEN)
def test_intent_classification(case):
    result = classify_intent(case["input"])

    # Deterministic checks first — schema and required fields
    assert "intent" in result, "Missing required 'intent' field"
    assert "confidence" in result, "Missing required 'confidence' field"
    assert 0 <= result["confidence"] <= 1, "Confidence out of range"

    # Semantic check — expected intent matches
    assert result["intent"] == case["expected_intent"], \
        f"Expected {case['expected_intent']}, got {result['intent']}"

def test_golden_dataset_pass_rate():
    """Track overall pass rate — fail the build if it drops below threshold."""
    passed = sum(1 for case in GOLDEN
                 if classify_intent(case["input"])["intent"] == case["expected_intent"])
    pass_rate = passed / len(GOLDEN)
    assert pass_rate >= 0.90, f"Pass rate {pass_rate:.0%} below 90% threshold"
```

```bash
pytest test_agent.py -v
# Run this after every prompt change. If pass rate drops, investigate BEFORE shipping.
```

**Day 1 takeaway:** "You have a regression harness. Every prompt change gets measured against the golden set. You'll catch regressions before your users do. Tomorrow: LLM-as-judge, embedding-based eval, and continuous evaluation in production."

**Your credibility drop:**
> "I'm literally building an agent testing pipeline right now — my course review agents have quality gates that verify code execution, link validity, and version currency before any output is accepted. I live this problem."

---

## SMART QUESTIONS TO ASK THE PANEL

Pick 3-4 based on how the call flows:

1. **"What's the target audience level — are learners expected to have prior CI/CD and Git experience, or are we starting from zero?"**
2. **"How much creative latitude do I have on lab design, or is there a prescribed format I should match?"**
3. **"What's the review cycle — how many rounds of feedback per deliverable, and what's the typical turnaround?"**
4. **"Are the screencasts expected to stay on GitHub.com specifically, or can I do CLI-heavy demos showing the GitHub CLI and API?"**
5. **"Is there an existing style guide or example course I should reference to match tone and depth?"**
6. **"What's the delivery format — do you need raw scripts, recorded video, or both per module?"**
7. **"For the talking head videos, is there a specific length target per course?"**

---

## MOVES TO MAKE

1. **Lead with enthusiasm on courses 1-5.** Mention you've already thought through Day 1 for each and are ready to start immediately.
2. **Demonstrate don't claim.** Reference the OpenClaw fleet and review pipeline naturally — not as a pitch, but as context for how you think about these problems.
3. **Push for Special tier** indirectly: emphasize depth across AI + DevOps + API engineering + observability. That combo is rare.
4. **Ask one smart question early** to signal engagement, then let them drive.
5. **Commit to the intro video** by end of weekend if they bring it up.

---

## MOVES TO AVOID

- Don't oversell on courses 6-7 — take them if offered, but don't volunteer
- Don't frame the agent pipeline as a time-saver for YOU (sounds like cutting corners) — frame it as infrastructure that ensures QUALITY
- Don't negotiate rate unless they bring it up first
- Don't badmouth other SMEs or pre-judge course quality before seeing materials
- Don't over-apologize about the intro video — commit and move on

---

## IF THEY ASK "WHY SHOULD WE PICK YOU?"

> "Three things. One: I've worked in DevOps, distributed AI, and API engineering professionally, which covers all four of your course domains — that's rare in a single SME. Two: I built and run an AI inference fleet that handles real production workloads, so when I teach async task scaling or AI guardrails, I'm teaching from lived experience, not from a textbook. Three: I've already built tooling that validates course content automatically — code execution, link checks, version currency, terminology consistency — which means my review process catches things human reviewers miss. You're not just hiring a reviewer, you're hiring a reviewer with infrastructure."

---

## LOGISTICS CHECKLIST

- [ ] Google Meet link tested (join 5 min early)
- [ ] Backup phone dial-in saved
- [ ] WARPLAN.md open in a second monitor
- [ ] Water within reach
- [ ] Quiet room, closed door
- [ ] Phone on silent
- [ ] HANDOFF.md reviewed for course list context
- [ ] Mentally rehearsed the "why you" one-liner

---

## POST-CALL ACTIONS

1. Update HANDOFF.md with: tier assigned, courses assigned, next blocker
2. Save any new memory facts to `C:\Users\Matt\.claude\projects\J--github-SME\memory\`
3. Record the 1-min C# audition intro video (if not already done)
4. Wait for first course package, then run it through the pipeline
