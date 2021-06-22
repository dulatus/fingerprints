import os
import io
import csv
import json
from pprint import pprint  # noqa
from normality import stringify
from urllib.request import urlopen
CSV_URL = "https://docs.google.com/spreadsheets/d/120Cd_8bev-MMxWJ7fBZOg0RJr2XQnjKgxbdYLKPeGNM/pub?gid=0&single=true&output=csv"  # noqa


def fetch():
    file_path = os.path.dirname(__file__)
    out_types_path = os.path.join(file_path, "..", "fingerprints", "types.json")
    out_intl_path = os.path.join(file_path, "..", "fingerprints", "types_intl.json")
    types = {}
    intl_types = {}
    fh = urlopen(CSV_URL)
    fh = io.TextIOWrapper(fh, encoding="utf-8")
    for row in csv.DictReader(fh):
        name = stringify(row.get("Name"))
        abbr = stringify(row.get("Abbreviation"))
        intl_abbr = stringify(row.get("Intl Equivalent"))
        if name is None or abbr is None:
            continue
        if name in types and types[name] != abbr:
            print(name, types[name], abbr)
        types[name] = abbr
        if intl_abbr:
            intl_types[abbr] = intl_abbr
        # print abbr, name

    elf_path = os.path.join(file_path, "elf-code-list.csv")
    with open(elf_path, "r") as fh:
        for row in csv.DictReader(fh):
            pprint(dict(row))

    with open(out_types_path, "w") as fh:
        json.dump({"types": types}, fh)

    with open(out_intl_path, "w") as fh:
        json.dump({"intl_types": types}, fh)


if __name__ == "__main__":
    fetch()
