# CLAUDE.md — Course Review Agent Pipeline

## Project Identity

This is the **Course Review Agent Pipeline** — an AI-powered content review and validation system built for EdTech SME contract work. It processes course materials (video scripts, readings, quizzes, labs, code samples) through a multi-agent pipeline that handles technical accuracy validation, code execution testing, quiz answer verification, and structured feedback generation.

The human SME (Matt Gates) focuses exclusively on: final review pass, screencast recording, talking head videos, and client communication. Everything else is automated.

## Owner

- **Matt Gates** — Technical Director, Ridge Cell Repair LLC
- GitHub: github.com/suhteevah
- Contract: Upwork SME engagement for EdTech platform (GitHub-focused courses)
- Agent ecosystem: OpenClaw (routes inference through local GPU fleet)

## Tech Stack

- **Language:** Rust-first for agents, Python for glue scripts and quick automation, Shell for orchestration
- **Inference:** Anthropic Claude API (via OpenClaw tier router — P40s for heavy, RTX 3070 Ti for fast, RTX 3050 for portable)
- **Document generation:** docx-js (Node.js) for all .docx output
- **Code execution:** Sandboxed bash environments for lab validation
- **Web verification:** Web search + fetch for link checking, version validation, API currency
- **Logging:** Verbose logging EVERYWHERE. Every agent action, every file processed, every decision made — logged with timestamps.

## Architecture

```
course-review-agent/
├── CLAUDE.md                    # This file
├── HANDOFF.md                   # Session handoff state
├── Cargo.toml                   # Workspace root (if Rust agents)
├── config/
│   ├── agent_config.toml        # Agent routing, model selection, temperature settings
│   └── course_domains.toml      # Domain-specific review criteria (GitHub, Stripe, etc.)
├── src/
│   ├── intake/                  # Intake & Classification Agent
│   │   ├── mod.rs
│   │   ├── classifier.rs        # File type classification logic
│   │   └── manifest.rs          # Course manifest generation
│   ├── reviewers/
│   │   ├── mod.rs
│   │   ├── script_reviewer.rs   # Video script technical accuracy
│   │   ├── reading_reviewer.rs  # Reading content validation
│   │   ├── quiz_validator.rs    # Quiz answer key verification
│   │   └── lab_validator.rs     # Code execution & lab walkthrough
│   ├── executor/
│   │   ├── mod.rs
│   │   ├── sandbox.rs           # Sandboxed code execution
│   │   └── environment.rs       # Environment setup (git, docker, tools)
│   ├── aggregator/
│   │   ├── mod.rs
│   │   └── feedback.rs          # Compile all reviews into single document
│   ├── output/
│   │   ├── mod.rs
│   │   ├── docx_generator.rs    # Generate .docx review documents
│   │   └── screencast_prep.rs   # Generate screencast scripts & demo environments
│   └── main.rs                  # CLI entrypoint
├── scripts/
│   ├── review_course.py         # Quick-start: feed a course folder, get a review
│   ├── review_single.py         # Review a single file (script/reading/quiz/lab)
│   ├── generate_lab.py          # Generate a hands-on lab from objectives
│   ├── incorporate_feedback.py  # Apply client/internal feedback to documents
│   ├── validate_links.py        # Check all URLs in course materials
│   ├── check_versions.py        # Verify all tool/API version references are current
│   └── prep_screencast.py       # Generate screencast script + demo environment
├── templates/
│   ├── review_document.md       # Template for compiled review output
│   ├── script_review.md         # Per-script review template
│   ├── reading_review.md        # Per-reading review template
│   ├── quiz_review.md           # Per-quiz review template
│   ├── lab_review.md            # Per-lab review template
│   └── screencast_script.md     # Screencast preparation template
├── tests/
│   ├── test_classifier.rs       # Classification unit tests
│   ├── test_quiz_validator.rs   # Quiz validation tests
│   ├── fixtures/                # Sample course materials for testing
│   │   ├── sample_script.md
│   │   ├── sample_reading.md
│   │   ├── sample_quiz.md
│   │   └── sample_lab.md
│   └── integration/
│       └── test_full_pipeline.rs
├── output/                      # Generated review documents land here
└── courses/                     # Course packages dropped here for processing
    └── .gitkeep
```

## Coding Standards

### Rust
- Edition 2021, async with Tokio
- `anyhow` for error handling, `tracing` for structured logging
- Every function that touches I/O logs entry, exit, and any errors
- No `unwrap()` in production code — always handle errors explicitly
- Modules organized by agent responsibility

### Python (glue scripts)
- Python 3.10+
- Type hints on all function signatures
- `logging` module with verbose output by default
- Scripts are standalone — each can be run independently from CLI
- All scripts accept `--verbose` flag

### Document Generation
- All .docx output uses docx-js patterns from `/mnt/skills/public/docx/SKILL.md`
- Review documents use consistent heading hierarchy and formatting
- Tables use DXA widths (never percentages)
- Arial font, professional styling consistent with Matt's other deliverables

## Agent Behavior Rules

1. **Never rubber-stamp content.** Every review must contain real findings from actual validation. If the content is perfect, say so explicitly with evidence — don't just say "looks good."

2. **Execute all code.** No code sample passes review without being actually executed. If execution requires an environment the agent can't set up, flag it explicitly with the exact requirements.

3. **Verify all technical claims.** If a script says "GitHub Actions supports matrix strategies for parallel testing," verify it. If a reading says "The latest version of the GitHub CLI is X.Y.Z," check it. Use web search for anything time-sensitive.

4. **Flag, don't guess.** If something can't be verified or the agent is uncertain, flag it for human review rather than making an assumption. The flag format is: `⚠️ HUMAN REVIEW: [reason]`

5. **Maintain consistent terminology.** Track all technical terms used across a course and flag inconsistencies. If Script 3 calls it "GitHub Actions workflow" and Reading 2 calls it "GitHub Actions pipeline," that's a finding.

6. **Log everything.** Every agent action produces a log entry with timestamp, agent name, input file, action taken, and result. Logs go to `output/logs/[course-name]/[timestamp].log`

7. **Structured output always.** Every agent produces output in the defined template format. No freeform text dumps. The Feedback Aggregator expects structured input.

## Quality Gates (MUST PASS before submission)

- [ ] All code samples execute successfully (or are flagged with specific errors)
- [ ] All quiz answer keys verified correct
- [ ] All URLs validated (no dead links)
- [ ] All version numbers verified current (via web search)
- [ ] No inconsistent terminology across course materials
- [ ] Review document compiles cleanly as .docx
- [ ] Human SME has completed final review pass (15-30 min)

## CLI Usage

```bash
# Full course review
python scripts/review_course.py ./courses/github-actions-cicd/ --output ./output/

# Single file review
python scripts/review_single.py ./courses/script_03.md --type video_script

# Generate a lab
python scripts/generate_lab.py --topic "GitHub Actions CI Pipeline" --duration 45min --output ./output/

# Incorporate feedback
python scripts/incorporate_feedback.py ./output/review_v1.docx --feedback ./feedback_round1.md

# Prep screencast
python scripts/prep_screencast.py ./courses/github-actions-cicd/ --episode 3 --output ./output/screencasts/

# Validate all links
python scripts/validate_links.py ./courses/github-actions-cicd/

# Check version references
python scripts/check_versions.py ./courses/github-actions-cicd/
```

## Integration with OpenClaw

The course review agents plug into the existing OpenClaw infrastructure:

- **Inference routing:** All LLM calls go through OpenClaw Core's tier-based router
  - Heavy review (full script analysis, reading validation): P40 tier
  - Quick checks (link validation, version lookup): RTX 3070 Ti tier
  - Portable/lightweight (quiz answer verification): RTX 3050 tier
- **Monitoring:** Agent performance metrics exported to Grafana via Prometheus
  - Review time per file
  - Issues found per course
  - Code execution pass/fail rates
  - Human override rate (how often SME changes agent recommendations)
- **Logging:** All agent logs flow through the standard OpenClaw logging pipeline

## Course Domain Configuration

Each course domain (GitHub, Stripe, etc.) has domain-specific review criteria:

### GitHub Domain
- Verify all `git` commands produce expected output
- Verify all GitHub CLI (`gh`) commands are current syntax
- Verify all GitHub Actions YAML is valid workflow syntax
- Verify all API endpoints match current GitHub REST/GraphQL API
- Verify all UI references match current GitHub web interface
- Check for deprecated features (classic tokens vs fine-grained, etc.)

### Stripe Domain (future)
- Verify all API endpoints match current Stripe API version
- Verify all code samples use current SDK syntax
- Verify webhook event names are current
- Check for deprecated payment method types

## Session Handoff

When switching between Claude Code sessions, update HANDOFF.md with:
- Current course being reviewed
- Files completed vs remaining
- Blocking issues awaiting human input
- Next action for incoming session

## Revenue Target

- 5 courses × $360 (Special tier) = $1,800
- Agent pipeline reduces personal time to ~3-4 hours per course
- Effective rate: $90-120/hr on human time
- Total human time across all 5 courses: ~15-20 hours
- Timeline: 3 months, flexible schedule
