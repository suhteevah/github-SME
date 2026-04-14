#!/usr/bin/env python3
"""
Review an entire course package through the agent pipeline.

Usage:
    python scripts/review_course.py <course_dir> [--domain GitHub] [--output output/] [--verbose]
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from engine import (setup_logging, build_course_manifest, get_review_prompt, 
                    save_review, compile_reviews)


def main():
    parser = argparse.ArgumentParser(description="Review a full course package")
    parser.add_argument("course_dir", help="Path to course materials directory")
    parser.add_argument("--domain", default="GitHub", help="Course domain")
    parser.add_argument("--tech-stack", default="Git, GitHub, GitHub Actions, GitHub CLI",
                        help="Technology stack")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--verbose", action="store_true", default=True)
    args = parser.parse_args()
    
    course_dir = Path(args.course_dir)
    if not course_dir.is_dir():
        print(f"ERROR: Directory not found: {course_dir}")
        sys.exit(1)
    
    course_name = course_dir.name
    logger = setup_logging(course_name=course_name, verbose=args.verbose)
    output_dir = Path(args.output) / course_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"{'='*60}")
    logger.info(f"COURSE REVIEW PIPELINE — {course_name}")
    logger.info(f"Domain: {args.domain}")
    logger.info(f"Tech Stack: {args.tech_stack}")
    logger.info(f"Output: {output_dir}")
    logger.info(f"{'='*60}")
    
    # ── Phase 1: Intake & Classification ──
    logger.info("PHASE 1: Intake & Classification")
    manifest = build_course_manifest(course_dir, logger)
    
    manifest_file = output_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info(f"Manifest saved: {manifest_file}")
    
    # ── Phase 2: Generate Review Prompts ──
    logger.info("PHASE 2: Generating review prompts")
    prompts_dir = output_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    
    reviewable_types = {"video_script", "reading", "quiz_practice", "quiz_graded", "lab"}
    review_queue = []
    skipped = []
    
    for file_info in manifest["files"]:
        filepath = course_dir / file_info["path"]
        file_type = file_info["type"]
        
        if file_type not in reviewable_types:
            logger.info(f"SKIP (no review agent): {file_info['name']} ({file_type})")
            skipped.append(file_info)
            continue
        
        content = filepath.read_text(encoding="utf-8", errors="replace")
        prompt = get_review_prompt(
            file_type=file_type,
            content=content,
            title=filepath.stem,
            domain=args.domain,
            tech_stack=args.tech_stack,
        )
        
        if prompt:
            prompt_file = prompts_dir / f"prompt_{filepath.stem}.md"
            prompt_file.write_text(prompt, encoding="utf-8")
            review_queue.append({
                "source": str(filepath),
                "type": file_type,
                "prompt_file": str(prompt_file),
                "status": "pending",
            })
            logger.info(f"QUEUED: {file_info['name']} → {file_type}")
    
    # ── Phase 3: Execute Reviews ──
    logger.info(f"PHASE 3: Review execution")
    logger.info(f"  Queued: {len(review_queue)} files")
    logger.info(f"  Skipped: {len(skipped)} files")
    
    # Save the review queue for processing
    queue_file = output_dir / "review_queue.json"
    queue_file.write_text(json.dumps(review_queue, indent=2), encoding="utf-8")
    
    print(f"\n{'='*60}")
    print(f"COURSE REVIEW PIPELINE — {course_name}")
    print(f"{'='*60}")
    print(f"\n📋 Manifest: {manifest_file}")
    print(f"📝 Review prompts: {prompts_dir}/")
    print(f"📊 Review queue: {queue_file}")
    print(f"\n   Files to review: {len(review_queue)}")
    print(f"   Files skipped:   {len(skipped)}")
    print(f"\n   Summary by type:")
    for ftype, count in manifest["summary"].items():
        status = "→ REVIEW" if ftype in reviewable_types else "→ SKIP"
        print(f"     {ftype}: {count} {status}")
    
    print(f"\n{'='*60}")
    print(f"NEXT STEPS:")
    print(f"{'='*60}")
    print(f"\n  1. Process each prompt through Claude inference:")
    print(f"     for f in {prompts_dir}/prompt_*.md; do")
    print(f'       claude -p "$(cat $f)" > {output_dir}/reviews/$(basename $f)')
    print(f"     done")
    print(f"\n  2. Or route through OpenClaw for automatic batch processing")
    print(f"\n  3. After reviews complete, compile:")
    print(f"     python scripts/compile_reviews.py {output_dir}/reviews/")
    print(f"\n  4. Run quality gates:")
    print(f"     python scripts/validate_links.py {course_dir}")
    print(f"     python scripts/check_versions.py {course_dir}")
    print(f"\n  5. Human final review pass (15-30 min)")
    print(f"  6. Record screencasts and talking head videos")
    

if __name__ == "__main__":
    main()
