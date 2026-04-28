import re

files_to_convert = ["publications.bib", "publications_preprint.bib", "abstracts.bib"]

def process_bib_file(content):
    """Process a bib file: add stars for co-first authors and underline my name."""
    # Split into entries (each starts with @)
    entries = re.split(r'(?=@)', content)
    processed_entries = []

    for entry in entries:
        if not entry.strip():
            processed_entries.append(entry)
            continue

        # Check for cofirst field
        cofirst_match = re.search(r'cofirst\s*=\s*(\d+)', entry)

        if cofirst_match:
            n_cofirst = int(cofirst_match.group(1))

            # Find and process the author field (may span multiple lines)
            author_match = re.search(r'(author\s*=\s*["{])(.+?)(["}]\s*,)', entry, re.DOTALL)
            if author_match:
                prefix = author_match.group(1)
                authors_str = author_match.group(2)
                suffix = author_match.group(3)

                # Split authors by " and " (preserving the separator)
                authors = re.split(r'(\s+and\s+)', authors_str)

                # Add stars to the first N authors (every other element is an author, others are " and ")
                author_count = 0
                new_authors = []
                for i, part in enumerate(authors):
                    if i % 2 == 0:  # This is an author name
                        if author_count < n_cofirst:
                            # Add star after the last name (before the comma)
                            # Format is "LastName, FirstName" so insert star before first comma
                            comma_idx = part.find(',')
                            if comma_idx != -1:
                                part = part[:comma_idx] + r"$^*$" + part[comma_idx:]
                            else:
                                # No comma, just append star
                                part = part.rstrip() + r"$^*$"
                        author_count += 1
                    new_authors.append(part)

                new_authors_str = ''.join(new_authors)
                entry = entry[:author_match.start()] + prefix + new_authors_str + suffix + entry[author_match.end():]

        processed_entries.append(entry)

    return ''.join(processed_entries)

for file_name in files_to_convert:
    new_file = file_name.replace(".bib", "_underlined.bib")

    with open(file_name, "r") as f_read:
        content = f_read.read()

    # First, add stars for co-first authors
    content = process_bib_file(content)

    # Then, underline my name (handle both with and without star)
    content = content.replace(r"Feng$^*$, Jean", r"\underline{Jean Feng}$^*$")
    content = content.replace("Feng, Jean", r"\underline{Jean Feng}")
    content = content.replace(r"Feng$^*$, J", r"\underline{J Feng}$^*$")
    content = content.replace("Feng, J", r"\underline{J Feng}")

    with open(new_file, "w") as f_write:
        f_write.write(content)

