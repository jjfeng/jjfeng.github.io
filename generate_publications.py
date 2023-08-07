import bibtexparser

SOFTWARE_DICT = {
    "monitoring machine learning (ml)-based risk prediction algorithms in the presence of confounding medical interventions": "https://github.com/jjfeng/monitoring_ML_CMI",
    "ensembled sparse-input hierarchical networks for high-dimensional datasets": "https://pypi.org/project/EASIER-net/",
    "estimation of cell lineage trees by maximum-likelihood phylogenetics": "https://github.com/matsengrp/gapml",
    "sparse-input neural networks for high-dimensional nonparametric regression and classification": "https://github.com/jjfeng/spinn",
    "survival analysis of dna mutation motifs with penalized proportional hazards": "https://github.com/matsengrp/samm",
    "efficient nonparametric statistical inference on population feature importance using shapley values": "https://github.com/bdwilliamson/spvim_supplementary",
    "nonparametric variable importance using an augmented neural network with multi-task learning": "https://github.com/jjfeng/nnet_var_import",
    "gradient-based regularization parameter selection for problems with nonsmooth penalty functions": "https://github.com/jjfeng/nonsmooth-joint-opt",
    "deep generative models for t cell receptor protein sequences": "https://github.com/matsengrp/vampire/",
    "learning to safely approve updates to machine learning algorithms": "https://github.com/jjfeng/aACP_time_trends",
    "approval policies for modifications to machine learning-based software as a medical device: a study of bio-creep": "https://github.com/jjfeng/aACP",
    "bayesian logistic regression for online recalibration and revision of risk prediction models with performance guarantees": "https://github.com/jjfeng/bayesian_model_revision",
    "selective prediction-set models with coverage guarantees": "https://github.com/jjfeng/pc_SPS",
    "sequential algorithmic modification with test data reuse": "https://github.com/jjfeng/adaptive_SRGP",
    "is this model reliable for everyone? testing for strong calibration": "https://github.com/jjfeng/testing_strong_calibration",
}
POSTER_DICT = {
    "sequential algorithmic modification with test data reuse": "adaptive_SRGP.pdf",
    "is this model reliable for everyone? testing for strong calibration": "subgroup_poster.pdf",
}

def print_entries(entry_list):
    return "\n\n".join(entry_list)

def convert_journal(journal):
    if journal == "ICML" or journal == "International Conference on Machine Learning":
        return "International Conference on Machine Learning (ICML)"
    return journal

BIBFILES = ["publications_preprint.bib", "publications.bib"]
OUTFILE = "publications.md"

bib_entries = []
for BIBFILE in BIBFILES:
    with open(BIBFILE, 'r') as bibtex_file:
        bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)
    bib_entries += bib_database.entries

parsed_entries = {"preprints": []}
years = set()
# Parse entries
for entry in bib_entries:
    for key in entry.keys():
        entry[key] = entry[key].replace("\n", " ")
    print(entry)

    title = entry["title"].replace("{", "").replace("}", "")
    authors = entry["author"].split(" and ")
    last_names = []
    for author in authors:
        last_name = author.split(", ")[0]
        last_name = "*%s*" % last_name if author == "Feng, Jean" else last_name
        last_names.append(last_name)

    if len(last_names) > 1:
        author_str = ", ".join(last_names[:-1]) + " and " + last_names[-1]
    else:
        author_str = last_names[0]

    is_preprint = "journal" not in entry or entry["journal"] in ["arXiv", "bioRxiv"]
    url = entry["url"]

    if is_preprint:
        journal = "bioRxiv" if ("journal" in entry and entry["journal"] == "bioRxiv") else "arXiv"
        if title.lower() in SOFTWARE_DICT:
            print("FOUND")
            software = SOFTWARE_DICT[title.lower()]
            pub_str = "**%s**<br />\n%s<br />\n[\[%s\]](%s)[\[code\]](%s)" % (title, author_str, journal, url, software)
        else:
            print("NOT FOUND", title)
            pub_str = "**%s**<br />\n%s<br />\n[\[%s\]](%s)" % (title, author_str, journal, url)
        if title.lower() in POSTER_DICT:
            pub_str += "[\[poster\]](%s)" % POSTER_DICT[title.lower()]
        parsed_entries["preprints"].append(pub_str)
    else:
        journal = convert_journal(entry["journal"])
        year = None if ("note" in entry and entry["note"] == "In press") else int(entry["year"])
        print("year is none", year)
        if year is not None:
            years.add(year)
            if title.lower() in SOFTWARE_DICT:
                print("FOUND")
                software = SOFTWARE_DICT[title.lower()]
                pub_str = "**%s**<br />\n%s<br />\n*%s*, %d<br />\n[\[paper\]](%s)[\[code\]](%s)" % (title, author_str, journal, year, url, software)
            else:
                print("NOT FOUND", title)
                pub_str = "**%s**<br />\n%s<br />\n*%s*, %d<br />\n[\[paper\]](%s)" % (title, author_str, journal, year, url)
        else:
            if title.lower() in SOFTWARE_DICT:
                print("FOUND")
                software = SOFTWARE_DICT[title.lower()]
                pub_str = "**%s**<br />\n%s<br />\n*%s*, In press<br />\n[\[paper\]](%s)[\[code\]](%s)" % (title, author_str, journal, url, software)
            else:
                pub_str = "**%s**<br />\n%s<br />\n*%s*, In press<br />\n[\[paper\]](%s)" % (title, author_str, journal, url)
        if title.lower() in POSTER_DICT:
            pub_str += "[\[poster\]](%s)" % POSTER_DICT[title.lower()]
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
if None in parsed_entries:
    output_lines.append("\n\n## In press\n")
    output_lines.append(print_entries(parsed_entries[None]))
for year in sorted(years, reverse=True):
    output_lines.append("\n\n## %d\n" % year)
    output_lines.append(print_entries(parsed_entries[year]))

with open(OUTFILE, "w") as outfile:
    outfile.writelines(output_lines)

