---
name: course-review-agent
description: "Automated course content review, validation, and generation pipeline for EdTech SME work. Use this skill whenever the user mentions reviewing course content, validating technical accuracy of educational materials, creating course outlines, reviewing video scripts, generating quiz questions, testing code labs, or any work related to EdTech course development. Also trigger when user says 'review this course', 'validate this script', 'check this quiz', 'create a lab', 'course outline', 'learning objectives', or references GitHub/Stripe course work for the Upwork SME contract. This skill deploys AI agents to handle the bulk of content review, code validation, and feedback generation — reducing SME time to final review pass and video recording only."
---

# Course Content Review Agent Pipeline

## Overview

This skill automates the heavy lifting of EdTech SME course review work. It processes course materials through a multi-stage AI pipeline that handles technical accuracy validation, code testing, quiz verification, reading review, and structured feedback generation — leaving the human SME to focus on final sign-off, screencasts, and talking head videos.

## Architecture

```
Course Materials (scripts, readings, quizzes, labs, outlines)
    │
    ▼
┌─────────────────────────────────────────┐
│         INTAKE & CLASSIFICATION          │
│  Categorize input: script / reading /    │
│  quiz / lab / outline / code sample      │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────────┐
    ▼             ▼                 ▼
┌────────┐  ┌──────────┐  ┌──────────────┐
│ SCRIPT │  │ READING  │  │  QUIZ/ASSESS │
│ REVIEW │  │ REVIEW   │  │  VALIDATOR   │
│ AGENT  │  │ AGENT    │  │              │
└────┬───┘  └────┬─────┘  └──────┬───────┘
    │            │               │
    ▼            ▼               ▼
┌─────────────────────────────────────────┐
│          CODE & LAB VALIDATOR            │
│  Execute code samples, validate labs,    │
│  test all technical claims               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        FEEDBACK AGGREGATOR               │
│  Compile structured review document      │
│  with pass/fail/suggestions per item     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
         SME Final Review Pass
         (Human: ~15-30 min per course)
```

## Agent Definitions

### 1. Intake & Classification Agent

**Purpose:** Parse incoming course materials and route to appropriate review agents.

**Input:** File path(s) or pasted content
**Output:** Classified content map with routing assignments

**Process:**
1. Read all input files from the course package
2. Classify each file by type: `video_script`, `reading`, `quiz_practice`, `quiz_graded`, `lab`, `outline`, `code_sample`
3. Extract metadata: course title, domain, estimated duration, technology stack
4. Generate a course manifest (JSON) with file-to-agent routing
5. Pass to appropriate downstream agents

**Classification rules:**
- Files mentioning "Scene", "Visual", "Voiceover", "Cut to" → `video_script`
- Files > 800 words without scene directions → `reading`
- Files with numbered questions and answer options → `quiz_practice` or `quiz_graded`
- Files with step-by-step instructions mentioning terminals, repos, or environments → `lab`
- Files with "Learning Objectives", "Module", "Week" structure → `outline`
- Files that are primarily code (.py, .js, .sh, .yml, etc.) → `code_sample`

### 2. Script Review Agent

**Purpose:** Validate technical accuracy of video scripts (7-9 per course).

**Input:** Video script content, course domain, technology stack
**Output:** Structured review with line-by-line technical accuracy assessment

**Review checklist per script:**
- [ ] All technical claims are factually accurate
- [ ] Code snippets shown on screen are syntactically correct
- [ ] CLI commands shown will produce the described output
- [ ] Version numbers and tool references are current (search web if needed)
- [ ] Terminology is used correctly and consistently
- [ ] Logical flow supports the learning objective
- [ ] No deprecated features or APIs referenced
- [ ] Screenshots/visual descriptions match current UI (flag if unable to verify)

**Output format:**
```markdown
## Script Review: [Script Title]
### Overall Assessment: PASS / NEEDS REVISION / MAJOR ISSUES
### Technical Accuracy Score: X/10

#### Line-by-line findings:
- **[timestamp/section]**: [finding] → [suggested fix]

#### Suggested edits:
1. [edit with rationale]

#### Questions for course team:
1. [anything requiring clarification]
```

### 3. Reading Review Agent

**Purpose:** Validate technical accuracy of readings (4-6 per course, up to 1200 words each).

**Input:** Reading content, course domain, technology stack
**Output:** Structured review with accuracy assessment and improvement suggestions

**Review checklist per reading:**
- [ ] All technical claims verified
- [ ] Code samples tested and working
- [ ] Links/references are valid and current
- [ ] Terminology consistent with video scripts
- [ ] Reading supports and reinforces video content (not contradicting)
- [ ] Appropriate depth for target audience
- [ ] No outdated information (API versions, tool versions, UI changes)

**Output format:**
```markdown
## Reading Review: [Reading Title]
### Overall Assessment: PASS / NEEDS REVISION / MAJOR ISSUES
### Technical Accuracy Score: X/10

#### Findings:
- **[paragraph/section]**: [finding] → [suggested fix]

#### Content gaps identified:
1. [missing concept that should be covered]

#### Rewrite suggestions:
[If content gaps are significant, provide rewritten paragraphs]
```

### 4. Quiz & Assessment Validator

**Purpose:** Validate practice quizzes and graded assessments (5 files, 5-10 questions each).

**Input:** Quiz content with questions and answer options
**Output:** Per-question validation with correct answer verification

**Validation per question:**
- [ ] Question is technically accurate
- [ ] Marked correct answer IS actually correct
- [ ] All distractors (wrong answers) are plausibly wrong (not obviously wrong)
- [ ] No ambiguous questions with multiple valid answers
- [ ] Question tests the stated learning objective
- [ ] Question difficulty is appropriate for the course level
- [ ] No trick questions or poorly worded stems

**Output format:**
```markdown
## Quiz Review: [Quiz Title]
### Overall Assessment: PASS / NEEDS REVISION

#### Question-by-question:
**Q1:** [question stem]
- Marked answer: [X] → CORRECT / INCORRECT
- Issue: [if any]
- Suggestion: [if any]

#### Summary:
- Questions validated: X/Y
- Issues found: Z
- Recommended changes: [list]
```

### 5. Code & Lab Validator

**Purpose:** Actually execute code samples, test lab workflows, validate technical claims.

**Input:** Code files, lab instructions, environment requirements
**Output:** Execution results with pass/fail per step

**Process:**
1. Set up required environment (install dependencies, clone repos)
2. Execute each code sample in isolation
3. Walk through lab instructions step-by-step, executing each command
4. Capture all output, errors, and screenshots
5. Compare actual output to expected output described in materials
6. Flag any discrepancies

**Output format:**
```markdown
## Lab Validation: [Lab Title]
### Environment: [tools/versions used]
### Overall: PASS / FAIL

#### Step-by-step execution:
**Step 1:** [instruction]
- Command: `[command executed]`
- Expected: [what the lab says should happen]
- Actual: [what actually happened]
- Status: ✅ PASS / ❌ FAIL / ⚠️ DIFFERS

#### Issues found:
1. [step X fails because...]

#### Environment notes:
- [any setup requirements not mentioned in lab]
```

### 6. Feedback Aggregator

**Purpose:** Compile all agent outputs into a single structured review document.

**Input:** All agent review outputs
**Output:** Single professional review document ready for submission

**Document structure:**
```markdown
# Course Review: [Course Title]
## Reviewer: Matt Gates
## Date: [date]
## Overall Assessment: READY / NEEDS REVISION / MAJOR REWORK

### Executive Summary
[2-3 sentence overall assessment]

### Outline Review
[outline findings]

### Video Script Reviews
[compiled script reviews]

### Reading Reviews
[compiled reading reviews]

### Quiz & Assessment Reviews
[compiled quiz reviews]

### Lab Validation Results
[compiled lab results]

### Recommendations
[prioritized list of changes needed]

### Sign-off
[ready for final SME review and video recording]
```

## Workflow Commands

### Full Course Review
```
Input: course package (folder of files)
Command: "Review this course package"
Process: Runs all agents in sequence, produces compiled review document
Output: Single .docx review document + per-file feedback files
```

### Single File Review
```
Input: individual file (script, reading, quiz, lab)
Command: "Review this [script/reading/quiz/lab]"
Process: Classifies and runs appropriate agent
Output: Structured review for that file
```

### Generate Lab
```
Input: course outline + learning objectives
Command: "Generate a hands-on lab for [topic]"
Process: Creates step-by-step lab with tested code
Output: Lab document with validated instructions
```

### Generate Learning Objectives
```
Input: course title + domain + duration
Command: "Generate learning objectives for [course]"
Process: Creates Bloom's taxonomy-aligned objectives
Output: Structured learning objectives document
```

### Incorporate Feedback
```
Input: review document + client/internal feedback
Command: "Incorporate this feedback into [document]"
Process: Applies feedback, tracks changes, produces revised version
Output: Updated document with change log
```

## Screencast & Video Prep

The pipeline does NOT automate video recording — that's the human SME's job. But it DOES prepare:

1. **Screencast script + demo environment** — For each screencast, the pipeline prepares:
   - A clean demo environment with all required tools installed
   - A step-by-step script of exactly what to show on screen
   - Pre-validated commands that will work when executed live
   - Expected output for each step so the SME knows what to expect

2. **Talking head bullet points** — For each talking head segment:
   - Key points to hit (derived from script review)
   - Technical terms to pronounce correctly
   - Timing targets per segment
   - Transition notes between segments

## Quality Gates

Before any review document is submitted to the client:

1. **All code must execute successfully** — No untested code samples
2. **All quiz answers must be verified** — No incorrect answer keys
3. **All links must be validated** — No dead links
4. **All version numbers must be current** — Web search verification
5. **Human SME must do a final 15-30 minute review pass** — Read the compiled review, spot-check 2-3 items, approve or flag

## File Output

All review documents are saved as .docx files using the docx skill patterns.
For .docx generation technical details, always read: `/mnt/skills/public/docx/SKILL.md`

## Integration with OpenClaw

This skill is designed to run through the OpenClaw inference stack:
- **Heavy review work** (script analysis, reading validation, quiz checking) → Routes through P40 or equivalent for long-context processing
- **Code execution** (lab validation, code testing) → Runs on local machine via bash
- **Web verification** (link checking, version validation) → Uses web_search and web_fetch tools
- **Document generation** → Uses docx-js via the docx skill

## Important Notes

- Every review must contain REAL findings from actual validation — never rubber-stamp content
- If code fails to execute, report the actual error — don't assume it works
- If a technical claim can't be verified, flag it explicitly rather than guessing
- The SME's reputation is on the line — quality gates exist for a reason
- Target turnaround: full course review in < 2 hours of agent processing time
- Human SME time per course: 30-60 minutes (final review + screencast/video recording)
