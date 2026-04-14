#!/usr/bin/env python3
"""
Validate all URLs found in course materials.

Usage:
    python scripts/validate_links.py <course_dir> [--verbose]
"""

import argparse
import re
import sys
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from engine import setup_logging


URL_PATTERN = re.compile(
    r'https?://[^\s\)\]\}\"\'<>,;]+',
    re.IGNORECASE
)


def extract_urls(filepath: Path) -> list[str]:
    """Extract all URLs from a file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    
    urls = URL_PATTERN.findall(content)
    # Clean trailing punctuation
    cleaned = []
    for url in urls:
        url = url.rstrip(".")
        url = url.rstrip(")")
        url = url.rstrip("]")
        cleaned.append(url)
    return cleaned


def check_url(url: str, timeout: int = 10) -> tuple[bool, str]:
    """Check if a URL is reachable. Returns (is_valid, status_message)."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, method="HEAD", headers={
            "User-Agent": "CourseReviewAgent/1.0 (link-validator)"
        })
        response = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return True, f"HTTP {response.status}"
    except urllib.error.HTTPError as e:
        if e.code in (403, 405):
            # Some servers block HEAD requests
            return True, f"HTTP {e.code} (likely valid, blocks HEAD)"
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Validate URLs in course materials")
    parser.add_argument("course_dir", help="Path to course materials")
    parser.add_argument("--verbose", action="store_true", default=True)
    args = parser.parse_args()
    
    course_dir = Path(args.course_dir)
    if not course_dir.is_dir():
        print(f"ERROR: Not a directory: {course_dir}")
        sys.exit(1)
    
    logger = setup_logging(course_name="link_validation", verbose=args.verbose)
    logger.info(f"=== Link Validation: {course_dir} ===")
    
    # Collect all URLs
    all_urls = {}  # url -> [source files]
    for filepath in sorted(course_dir.rglob("*")):
        if filepath.is_dir() or filepath.name.startswith("."):
            continue
        urls = extract_urls(filepath)
        for url in urls:
            if url not in all_urls:
                all_urls[url] = []
            all_urls[url].append(str(filepath.relative_to(course_dir)))
    
    logger.info(f"Found {len(all_urls)} unique URLs across course materials")
    
    # Validate each URL
    results = {"valid": [], "invalid": [], "uncertain": []}
    
    for url, sources in sorted(all_urls.items()):
        is_valid, status = check_url(url)
        
        result = {
            "url": url,
            "status": status,
            "sources": sources,
        }
        
        if is_valid:
            results["valid"].append(result)
            logger.info(f"  ✅ {url} — {status}")
        elif "blocks HEAD" in status:
            results["uncertain"].append(result)
            logger.warning(f"  ⚠️  {url} — {status}")
        else:
            results["invalid"].append(result)
            logger.error(f"  ❌ {url} — {status}")
    
    # Report
    print(f"\n{'='*60}")
    print(f"LINK VALIDATION REPORT")
    print(f"{'='*60}")
    print(f"\n  Total URLs: {len(all_urls)}")
    print(f"  ✅ Valid:     {len(results['valid'])}")
    print(f"  ⚠️  Uncertain: {len(results['uncertain'])}")
    print(f"  ❌ Invalid:   {len(results['invalid'])}")
    
    if results["invalid"]:
        print(f"\n  BROKEN LINKS:")
        for r in results["invalid"]:
            print(f"    ❌ {r['url']}")
            print(f"       Status: {r['status']}")
            print(f"       Found in: {', '.join(r['sources'])}")
    
    if results["uncertain"]:
        print(f"\n  NEEDS MANUAL CHECK:")
        for r in results["uncertain"]:
            print(f"    ⚠️  {r['url']}")
            print(f"       Status: {r['status']}")
    
    # Quality gate
    if results["invalid"]:
        print(f"\n  ❌ QUALITY GATE: FAIL — {len(results['invalid'])} broken links found")
        sys.exit(1)
    else:
        print(f"\n  ✅ QUALITY GATE: PASS — All links valid")


if __name__ == "__main__":
    main()
