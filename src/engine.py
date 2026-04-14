#!/usr/bin/env python3
"""
Course Review Agent Pipeline — Core Engine
Routes course materials through AI-powered review agents.
"""

import os
import sys
import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

# ── Logging Setup ──────────────────────────────────────────
def setup_logging(course_name: str = "default", verbose: bool = True) -> logging.Logger:
    """Configure verbose logging for the review pipeline."""
    log_dir = Path("output/logs") / course_name
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"{timestamp}.log"
    
    logger = logging.getLogger("course-review")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # File handler — always verbose
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(fh)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(ch)
    
    logger.info(f"Logging initialized — file: {log_file}")
    return logger


# ── File Classification ────────────────────────────────────
SCRIPT_MARKERS = ["scene", "visual", "voiceover", "cut to", "narrator", "on screen", "b-roll"]
QUIZ_MARKERS = ["question", "correct answer", "option a", "option b", "choose the", "which of the following"]
LAB_MARKERS = ["step 1", "step 2", "terminal", "run the following", "clone the repo", "open your terminal"]
OUTLINE_MARKERS = ["learning objectives", "module", "week", "course outline", "by the end of this"]

def classify_file(filepath: Path, logger: logging.Logger) -> str:
    """Classify a course material file by type.
    
    Returns one of: video_script, reading, quiz_practice, quiz_graded, 
                     lab, outline, code_sample, unknown
    """
    logger.info(f"Classifying file: {filepath.name}")
    
    ext = filepath.suffix.lower()
    
    # Code files by extension
    code_extensions = {".py", ".js", ".ts", ".sh", ".bash", ".yml", ".yaml", 
                       ".json", ".rb", ".go", ".rs", ".java", ".c", ".cpp",
                       ".dockerfile", ".tf", ".hcl"}
    if ext in code_extensions:
        logger.info(f"  → code_sample (by extension: {ext})")
        return "code_sample"
    
    # Read content for text-based classification
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace").lower()
    except Exception as e:
        logger.error(f"  → Failed to read file: {e}")
        return "unknown"
    
    word_count = len(content.split())
    logger.debug(f"  Word count: {word_count}")
    
    # Score each category
    scores = {
        "video_script": sum(1 for m in SCRIPT_MARKERS if m in content),
        "quiz": sum(1 for m in QUIZ_MARKERS if m in content),
        "lab": sum(1 for m in LAB_MARKERS if m in content),
        "outline": sum(1 for m in OUTLINE_MARKERS if m in content),
    }
    
    logger.debug(f"  Classification scores: {scores}")
    
    # Determine type
    max_score = max(scores.values())
    if max_score == 0:
        # No markers found — classify by length
        if word_count > 800:
            result = "reading"
        elif word_count > 200:
            result = "reading"  # Short reading
        else:
            result = "unknown"
    elif scores["video_script"] == max_score:
        result = "video_script"
    elif scores["quiz"] == max_score:
        # Distinguish practice from graded
        if "graded" in content or "final" in content or "assessment" in content:
            result = "quiz_graded"
        else:
            result = "quiz_practice"
    elif scores["lab"] == max_score:
        result = "lab"
    elif scores["outline"] == max_score:
        result = "outline"
    else:
        result = "reading"
    
    logger.info(f"  → {result} (score: {max_score})")
    return result


def build_course_manifest(course_dir: Path, logger: logging.Logger) -> dict:
    """Scan a course directory and build a manifest of all materials.
    
    Returns:
        {
            "course_dir": str,
            "timestamp": str,
            "files": [
                {"path": str, "name": str, "type": str, "size": int, "hash": str}
            ],
            "summary": {"video_scripts": int, "readings": int, ...}
        }
    """
    logger.info(f"Building course manifest for: {course_dir}")
    
    manifest = {
        "course_dir": str(course_dir),
        "timestamp": datetime.now().isoformat(),
        "files": [],
        "summary": {}
    }
    
    type_counts = {}
    
    # Scan all files
    for filepath in sorted(course_dir.rglob("*")):
        if filepath.is_dir():
            continue
        if filepath.name.startswith("."):
            continue
            
        file_type = classify_file(filepath, logger)
        
        # Hash for change detection
        file_hash = hashlib.md5(filepath.read_bytes()).hexdigest()
        
        manifest["files"].append({
            "path": str(filepath.relative_to(course_dir)),
            "name": filepath.name,
            "type": file_type,
            "size": filepath.stat().st_size,
            "hash": file_hash,
        })
        
        type_counts[file_type] = type_counts.get(file_type, 0) + 1
    
    manifest["summary"] = type_counts
    
    logger.info(f"Manifest complete: {len(manifest['files'])} files")
    for ftype, count in type_counts.items():
        logger.info(f"  {ftype}: {count}")
    
    return manifest


# ── Review Prompt Templates ────────────────────────────────
SCRIPT_REVIEW_PROMPT = """You are a Subject Matter Expert reviewing a video script for technical accuracy.

Course Domain: {domain}
Technology Stack: {tech_stack}

Review this video script and produce a structured review following this EXACT format:

## Script Review: {title}
### Overall Assessment: PASS / NEEDS REVISION / MAJOR ISSUES
### Technical Accuracy Score: X/10

#### Line-by-line findings:
- **[section/timestamp]**: [finding] → [suggested fix]

#### Suggested edits:
1. [edit with rationale]

#### Questions for course team:
1. [anything requiring clarification]

IMPORTANT RULES:
- Verify every technical claim. If you cannot verify, flag it with ⚠️ HUMAN REVIEW
- Check all code snippets for syntax errors
- Check all CLI commands for correct syntax
- Flag any deprecated features or outdated API references
- Flag terminology inconsistencies

---
SCRIPT CONTENT:
{content}
"""

READING_REVIEW_PROMPT = """You are a Subject Matter Expert reviewing a technical reading for accuracy.

Course Domain: {domain}
Technology Stack: {tech_stack}

Review this reading and produce a structured review following this EXACT format:

## Reading Review: {title}
### Overall Assessment: PASS / NEEDS REVISION / MAJOR ISSUES
### Technical Accuracy Score: X/10

#### Findings:
- **[paragraph/section]**: [finding] → [suggested fix]

#### Content gaps identified:
1. [missing concept that should be covered]

#### Rewrite suggestions:
[If content gaps are significant, provide rewritten paragraphs]

IMPORTANT RULES:
- Verify every technical claim
- Test all code samples mentally for correctness
- Check that links/references would be valid
- Flag outdated information
- Assess appropriate depth for target audience

---
READING CONTENT:
{content}
"""

QUIZ_REVIEW_PROMPT = """You are a Subject Matter Expert validating a quiz/assessment.

Course Domain: {domain}
Technology Stack: {tech_stack}

Validate every question and produce a structured review following this EXACT format:

## Quiz Review: {title}
### Overall Assessment: PASS / NEEDS REVISION

#### Question-by-question:
**Q1:** [question stem]
- Marked answer: [X] → CORRECT / INCORRECT
- Issue: [if any]
- Suggestion: [if any]

[repeat for each question]

#### Summary:
- Questions validated: X/Y
- Issues found: Z
- Recommended changes: [list]

IMPORTANT RULES:
- Verify the marked correct answer IS actually correct
- Check all distractors are plausibly wrong (not obviously wrong)
- Flag ambiguous questions with multiple valid answers
- Flag trick questions or poorly worded stems
- Assess difficulty appropriateness

---
QUIZ CONTENT:
{content}
"""

LAB_REVIEW_PROMPT = """You are a Subject Matter Expert validating a hands-on lab.

Course Domain: {domain}
Technology Stack: {tech_stack}

Walk through every step of this lab and validate it. Produce a structured review:

## Lab Validation: {title}
### Environment Required: [tools/versions needed]
### Overall: PASS / FAIL

#### Step-by-step validation:
**Step 1:** [instruction]
- Command: `[command to execute]`
- Expected: [what the lab says should happen]
- Validation: ✅ CORRECT / ❌ ISSUE / ⚠️ NEEDS TESTING
- Notes: [any issues]

[repeat for each step]

#### Issues found:
1. [step X has issue because...]

#### Missing setup requirements:
- [any environment setup not mentioned in lab]

IMPORTANT RULES:
- Validate every command for correct syntax
- Flag any commands that would fail without specific prerequisites
- Check that the lab flow is logical and sequential
- Verify that outputs described match what commands would actually produce
- Flag any security concerns (hardcoded credentials, sudo usage, etc.)

---
LAB CONTENT:
{content}
"""


def get_review_prompt(file_type: str, content: str, title: str, 
                      domain: str = "GitHub", tech_stack: str = "Git, GitHub, GitHub Actions") -> str:
    """Get the appropriate review prompt for a file type."""
    prompts = {
        "video_script": SCRIPT_REVIEW_PROMPT,
        "reading": READING_REVIEW_PROMPT,
        "quiz_practice": QUIZ_REVIEW_PROMPT,
        "quiz_graded": QUIZ_REVIEW_PROMPT,
        "lab": LAB_REVIEW_PROMPT,
    }
    
    template = prompts.get(file_type)
    if not template:
        return None
    
    return template.format(
        content=content,
        title=title,
        domain=domain,
        tech_stack=tech_stack,
    )


# ── Review Result Storage ──────────────────────────────────
def save_review(review_text: str, source_file: str, output_dir: Path, 
                logger: logging.Logger) -> Path:
    """Save a review result to the output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate output filename
    source_name = Path(source_file).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"review_{source_name}_{timestamp}.md"
    
    output_file.write_text(review_text, encoding="utf-8")
    logger.info(f"Review saved: {output_file}")
    
    return output_file


def compile_reviews(review_files: list[Path], course_name: str, 
                    output_dir: Path, logger: logging.Logger) -> Path:
    """Compile all individual reviews into a single course review document."""
    logger.info(f"Compiling {len(review_files)} reviews for course: {course_name}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    compiled = f"""# Course Review: {course_name}
## Reviewer: Matt Gates
## Date: {timestamp}

---

"""
    
    for review_file in sorted(review_files):
        content = review_file.read_text(encoding="utf-8")
        compiled += content + "\n\n---\n\n"
    
    compiled += """## Quality Gate Checklist

- [ ] All code samples execute successfully
- [ ] All quiz answer keys verified correct
- [ ] All URLs validated
- [ ] All version numbers verified current
- [ ] No inconsistent terminology
- [ ] Human SME final review complete

## Sign-off

Reviewed by Matt Gates, Subject Matter Expert
"""
    
    output_file = output_dir / f"course_review_{course_name}_{timestamp}.md"
    output_file.write_text(compiled, encoding="utf-8")
    logger.info(f"Compiled review saved: {output_file}")
    
    return output_file


# ── Main Entry Point ───────────────────────────────────────
if __name__ == "__main__":
    print("Course Review Agent Pipeline — Core Engine")
    print("Use scripts/review_course.py or scripts/review_single.py to run reviews.")
    print()
    print("Available commands:")
    print("  python scripts/review_course.py <course_dir>    — Full course review")
    print("  python scripts/review_single.py <file>          — Single file review")
    print("  python scripts/validate_links.py <course_dir>   — Link validation")
    print("  python scripts/check_versions.py <course_dir>   — Version check")
    print("  python scripts/generate_lab.py --topic <topic>  — Generate lab")
    print("  python scripts/prep_screencast.py <course_dir>  — Screencast prep")
