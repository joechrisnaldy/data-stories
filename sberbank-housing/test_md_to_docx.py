"""md_to_docx carries each Markdown image's alt text into the picture's wp:docPr descr.

Run from the repo root: python3 -m unittest discover -s sberbank-housing -p "test_md_to_docx.py"
"""
import struct
import tempfile
import unittest
import zipfile
import zlib
import xml.etree.ElementTree as ET
from pathlib import Path

from md_to_docx import convert

WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"


def tiny_png():
    """A valid 1x1 grayscale PNG, built from the stdlib so the test needs no image files."""
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(b"\x00\x00")) + chunk(b"IEND", b""))


class AltTextTest(unittest.TestCase):
    def test_each_picture_gets_its_markdown_alt_as_descr(self):
        alts = ["Growth of one yearly saving", "Rates after inflation, S&P 500 vs JHT"]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "a.png").write_bytes(tiny_png())
            (tmp / "b.png").write_bytes(tiny_png())
            md = tmp / "post.md"
            md.write_text(f"# Title\n\n![{alts[0]}](a.png)\n\nText.\n\n![{alts[1]}](b.png)\n")
            out = tmp / "post.docx"
            convert(md, out)
            with zipfile.ZipFile(out) as z:
                root = ET.fromstring(z.read("word/document.xml"))
        descrs = [el.get("descr") for el in root.iter(f"{WP}docPr")]
        self.assertEqual(descrs, alts)


if __name__ == "__main__":
    unittest.main()
