files_to_convert = ["publications.bib"]

for file_name in files_to_convert:
    new_file = file_name.replace(".bib", "_underlined.bib")
    with open(new_file, "w") as f_write:
        with open(file_name, "r") as f_read:
            for line in f_read:
                new_line = line.replace("Feng, Jean", r"\underline{Jean Feng}")
                f_write.write(new_line)

