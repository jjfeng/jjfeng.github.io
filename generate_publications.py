import bibtexparser

def print_entries(entry_list):
    return "\n\n".join(entry_list)

OUTFILE = "publications.md"

with open('publications.bib', 'r') as bibtex_file:
    bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

parsed_entries = {"preprints": []}
years = set()
# Parse entries
for entry in bib_database.entries:
    for key in entry.keys():
        entry[key] = entry[key].replace("\n", " ")
    print(entry)

    title = entry["title"].replace("{", "").replace("}", "")
    authors = entry["author"].split(" and ")
    last_names = []
    for author in authors:
        last_name = author.split(", ")[0]
        last_names.append(last_name)

    if len(last_names) > 1:
        author_str = ", ".join(last_names[:-1]) + " and " + last_names[-1]
    else:
        author_str = last_names[0]

    is_preprint = "journal" not in entry or entry["journal"] in ["arXiv", "bioRxiv"]
    url = entry["url"]

    if is_preprint:
        journal = "bioRxiv" if ("journal" in entry and entry["journal"] == "bioRxiv") else "arXiv"
        pub_str = "**%s**<br />\n%s<br />\n[\[%s\]](%s)" % (title, author_str, journal, url)
        parsed_entries["preprints"].append(pub_str)
    else:
        journal = entry["journal"]
        year = int(entry["year"])
        years.add(year)
        pub_str = "**%s**<br />\n%s<br />\n%s, %d<br />\n[\[paper\]](%s)" % (title, author_str, journal, year, url)
        if year not in parsed_entries:
            parsed_entries[year] = []
        parsed_entries[year].append(pub_str)

output_lines = [
"""---
layout: default
title: Publications
---

"""]
output_lines.append("## Preprints\n")
output_lines.append(print_entries(parsed_entries["preprints"]))
for year in sorted(years, reverse=True):
    output_lines.append("\n\n## %d\n" % year)
    output_lines.append(print_entries(parsed_entries[year]))

with open(OUTFILE, "w") as outfile:
    outfile.writelines(output_lines)

