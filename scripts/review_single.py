#!/usr/bin/env python3
"""
Review a single course material file through the agent pipeline.

Usage:
    python scripts/review_single.py <filepath> [--type video_script|reading|quiz|lab] [--domain GitHub] [--verbose]
"""

import argparse
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from engine import setup_logging, classify_file, get_review_prompt, save_review


def main():
    parser = argparse.ArgumentParser(description="Review a single course material file")
    parser.add_argument("filepath", help="Path to the file to review")
    parser.add_argument("--type", choices=["video_script", "reading", "quiz_practice", "quiz_graded", "lab", "outline", "code_sample"],
                        help="Override auto-classification")
    parser.add_argument("--domain", default="GitHub", help="Course domain (default: GitHub)")
    parser.add_argument("--tech-stack", default="Git, GitHub, GitHub Actions, GitHub CLI",
                        help="Technology stack for the course")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--verbose", action="store_true", default=True, help="Verbose logging")
    args = parser.parse_args()
    
    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    
    logger = setup_logging(course_name="single_review", verbose=args.verbose)
    logger.info(f"=== Single File Review: {filepath.name} ===")
    
    # Classify
    if args.type:
        file_type = args.type
        logger.info(f"File type override: {file_type}")
    else:
        file_type = classify_file(filepath, logger)
    
    # Read content
    content = filepath.read_text(encoding="utf-8", errors="replace")
    logger.info(f"File loaded: {len(content)} chars, {len(content.split())} words")
    
    # Generate review prompt
    prompt = get_review_prompt(
        file_type=file_type,
        content=content,
        title=filepath.stem,
        domain=args.domain,
        tech_stack=args.tech_stack,
    )
    
    if prompt is None:
        logger.warning(f"No review prompt available for type: {file_type}")
        logger.info("File types with review support: video_script, reading, quiz_practice, quiz_graded, lab")
        print(f"\nNo review agent for file type '{file_type}'. Supported: video_script, reading, quiz, lab")
        sys.exit(0)
    
    # Output the prompt for now (will be routed to Claude API when integrated with OpenClaw)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    prompt_file = output_dir / f"prompt_{filepath.stem}.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    logger.info(f"Review prompt generated: {prompt_file}")
    
    print(f"\n✅ Review prompt generated: {prompt_file}")
    print(f"   File type: {file_type}")
    print(f"   Domain: {args.domain}")
    print(f"   Words: {len(content.split())}")
    print(f"\n   To execute review, pipe this prompt through Claude:")
    print(f"   cat {prompt_file} | claude -p 'Review this course material'")
    print(f"\n   Or run through OpenClaw inference router for automatic processing.")


if __name__ == "__main__":
    main()
