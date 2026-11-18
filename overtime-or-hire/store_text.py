"""Write a plain-text copy of each stored source document, for the gate's source check and the provenance audit.

docs/sources.json pins each copy's sha256. A web page (.html) loses its markup and gets the title its reference
entry uses as the first line. A PDF is converted by pdftotext -layout, which keeps table rows on one line and
separates pages with form feeds, so a quote's page is one plus the number of form feeds before it. The law in
uu27-2026 is a scan whose text layer garbles its first page, so its copy opens with the title as printed there
(UU_TITLE). Run once after capturing: python3 store_text.py
"""
import hashlib
import html
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
UU_TITLE = "UNDANG-UNDANG REPUBLIK INDONESIA NOMOR 27 TAHUN 2026 TENTANG PELINDUNGAN KETENAGAKERJAAN"

# folder under sources/ -> (stored file, encoding of a page, first line written before the text or None)
PAGES = {
    "ecec-2026-06": ("index.html", "cp1252", "Employer costs for employee compensation: June 2026"),
    "dol-fs23": ("index.html", "utf-8", "Fact sheet #23: Overtime pay requirements of the FLSA"),
    "dol-fs17a": ("index.html", "utf-8", "Fact sheet #17A: Exemption for executive, administrative, professional, "
                                         "computer & outside sales employees under the Fair Labor Standards Act "
                                         "(FLSA)"),
    "ecfr-29-541": ("index.html", "utf-8", "29 CFR Part 541"),
    "cap-2012-turnover": ("index.html", "utf-8", "There are significant business costs to replacing employees"),
}
PDFS = {
    "atus": ("lexiconnoex0324.pdf", None),
    "atus-codebook": ("atusintcodebk0324.pdf", None),
    "atus-2024-release": ("atus_06262025.pdf", None),
    "pencavel-iza-8129": ("dp8129.pdf", None),
    "rieti-21e040": ("21e040.pdf", None),
    "rand-rr1791": ("RAND_RR1791.pdf", None),
    "uu27-2026": ("uu27-2026.pdf", UU_TITLE),
    "pp35-2021": ("pp35-2021.pdf", None),
}
FOLDER = {"atus-codebook": "atus"}     # the lexicon and the codebook share the folder the survey files came in


def page_text(path: str, encoding: str) -> str:
    with open(path, encoding=encoding, errors="replace") as f:
        raw = f.read()
    raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())


def pdf_text(path: str) -> str:
    done = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, check=True)
    return done.stdout.decode("utf-8", "replace")


def write(out: str, first_line: str | None, text: str) -> None:
    with open(out, "w", encoding="utf-8") as f:
        f.write((first_line + "\n\n" if first_line else "") + text + ("" if text.endswith("\n") else "\n"))
    with open(out, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"{digest[:12]}  {len(text):>8} chars  {os.path.relpath(out, HERE)}")


def main() -> None:
    for folder, (name, encoding, title) in PAGES.items():
        base = os.path.join(HERE, "sources", folder)
        write(os.path.join(base, folder + ".txt"), title, page_text(os.path.join(base, name), encoding))
    for key, (name, title) in PDFS.items():
        base = os.path.join(HERE, "sources", FOLDER.get(key, key))
        write(os.path.join(base, os.path.splitext(name)[0] + ".txt"), title, pdf_text(os.path.join(base, name)))


if __name__ == "__main__":
    main()
