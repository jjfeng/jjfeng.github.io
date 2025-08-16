import bibtexparser

SOFTWARE_DICT = {
    "a hierarchical decomposition for explaining ml performance discrepancies": "https://github.com/jjfeng/HDPD",
    "bayesian concept bottleneck models with llm priors": "https://github.com/jjfeng/bc-llm",
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
    "designing monitoring strategies for deployed machine learning algorithms: navigating performativity through a causal lens": "https://github.com/jjfeng/monitoring_causally",
    "who experiences large model decay and why? a hierarchical framework for diagnosing heterogeneous performance drift": "https://github.com/jjfeng/shift",
    "when the domain expert has no time and the llm developer has no clinical expertise: real-world lessons from llm co-design in a safety-net hospital": "https://github.com/jjfenglab/social-wayfinder",
}
TALK_DICT = {
    "towards a post-market monitoring framework for machine learning-based medical devices: a case study": "postmarket_monitoring_talk_short.pdf",
}
POSTER_DICT = {
    "sequential algorithmic modification with test data reuse": "adaptive_SRGP.pdf",
    "is this model reliable for everyone? testing for strong calibration": "subgroup_poster.pdf",
    "towards a post-market monitoring framework for machine learning-based medical devices: a case study": "poster_neurips_regml_workshop.pdf",
    "designing monitoring strategies for deployed machine learning algorithms: navigating performativity through a causal lens": "clear_poster.pdf",
    "``who experiences large model decay and why?'' a hierarchical framework for diagnosing heterogeneous performance drift": "2025_07_16_icml_SHIFT_poster.pdf",
}

def print_entries(entry_list):
    return "\n\n".join(entry_list)

def convert_journal(journal):
    if journal == "ICML" or journal == "International Conference on Machine Learning":
        return "International Conference on Machine Learning (ICML)"
    return journal

BIBFILES = ["publications_preprint.bib", "publications.bib"] #, "publications_workshop.bib"]
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
        if title.lower() in TALK_DICT:
            pub_str += "[\[slides\]](%s)" % TALK_DICT[title.lower()]
        if "award" in entry:
            pub_str += f" ***{entry['award']}***"
        if year not in parsed_entries:
            parsed_entries[year] = []
        parsed_entries[year].append(pub_str)

output_lines = [
"""---
layout: default
title: Publications
---
"""]
#<link rel="stylesheet" type="text/css" href="publications.css">
#<script src="publications_filter.js"></script>
#
#
#<button class="filter-btn" data-filter="all">All</button>
#<button class="filter-btn" data-filter="methods">Methods</button>
#<button class="filter-btn" data-filter="applied">Applied</button>

if None in parsed_entries:
    output_lines.append("\n## In press\n")
    output_lines.append(print_entries(parsed_entries[None]))
output_lines.append("\n\n## Preprints\n")
output_lines.append(print_entries(parsed_entries["preprints"]))
for year in sorted(years, reverse=True):
    output_lines.append("\n\n## %d\n" % year)
    output_lines.append(print_entries(parsed_entries[year]))
with open(OUTFILE, "w") as outfile:
    outfile.writelines(output_lines)

