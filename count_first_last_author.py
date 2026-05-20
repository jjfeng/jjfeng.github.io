#!/usr/bin/env python3
"""Count publications where Jean Feng is first or last author."""

import re
from pathlib import Path


def parse_bib_entries(bib_content):
    """Parse BibTeX content and extract entries with their authors."""
    entries = []
    # Match @TYPE{key, ... } entries
    pattern = r'@\w+\{([^,]+),([^@]*?)(?=\n@|\Z)'
    matches = re.findall(pattern, bib_content, re.DOTALL)

    for key, content in matches:
        # Extract author field - handle multi-line authors
        author_match = re.search(r'author\s*=\s*["{](.+?)["}](?:,|\s*\n)', content, re.DOTALL | re.IGNORECASE)
        if author_match:
            author_str = author_match.group(1)
            # Clean up whitespace and newlines
            author_str = re.sub(r'\s+', ' ', author_str).strip()
            entries.append({'key': key.strip(), 'authors': author_str})

    return entries


def is_jean_feng(name):
    """Check if a name refers to Jean Feng."""
    name_lower = name.lower().strip()
    # Handle "Feng, Jean" or "Jean Feng" formats
    return 'feng, jean' in name_lower or 'jean feng' in name_lower


def get_first_last_authors(author_str):
    """Extract first and last authors from author string."""
    # Split by " and " to get individual authors
    authors = re.split(r'\s+and\s+', author_str)
    authors = [a.strip() for a in authors if a.strip()]

    if not authors:
        return None, None

    first_author = authors[0]
    last_author = authors[-1] if len(authors) > 1 else authors[0]

    return first_author, last_author


def main():
    base_path = Path(__file__).parent

    bib_files = ['publications.bib', 'publications_preprint.bib']

    total_pubs = 0
    first_author_count = 0
    last_author_count = 0
    first_or_last_count = 0

    results = {'first': [], 'last': [], 'both': []}

    for bib_file in bib_files:
        filepath = base_path / bib_file
        if not filepath.exists():
            print(f"Warning: {bib_file} not found")
            continue

        content = filepath.read_text()
        entries = parse_bib_entries(content)

        print(f"\n=== {bib_file} ===")
        print(f"Total entries: {len(entries)}")

        for entry in entries:
            total_pubs += 1
            first, last = get_first_last_authors(entry['authors'])

            is_first = is_jean_feng(first) if first else False
            is_last = is_jean_feng(last) if last else False

            if is_first and is_last:
                first_author_count += 1
                last_author_count += 1
                first_or_last_count += 1
                results['both'].append(entry['key'])
            elif is_first:
                first_author_count += 1
                first_or_last_count += 1
                results['first'].append(entry['key'])
            elif is_last:
                last_author_count += 1
                first_or_last_count += 1
                results['last'].append(entry['key'])

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total publications: {total_pubs}")
    print(f"Jean Feng as first author: {first_author_count}")
    print(f"Jean Feng as last author: {last_author_count}")
    print(f"Jean Feng as first OR last author: {first_or_last_count}")

    print("\n--- First author papers ---")
    for key in results['first']:
        print(f"  {key}")

    print("\n--- Last author papers ---")
    for key in results['last']:
        print(f"  {key}")

    print("\n--- Solo/both first and last ---")
    for key in results['both']:
        print(f"  {key}")


if __name__ == '__main__':
    main()
