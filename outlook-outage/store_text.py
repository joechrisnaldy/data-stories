"""Write a plain-text copy of each stored page, with the title its reference entry uses as the first line.

The gate's source check reads these .txt copies (docs/sources.json pins each one's sha256). The stored .html pages
under sources/ are the captures; this script only removes markup. Run once after capturing: python3 store_text.py
"""
import hashlib
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
# folder under sources/ -> the title its reference entry gives (the first line of the text copy)
TITLES = {
    "penn-ms-incidents": "Microsoft's incident report for PennO365",
    "datareportal-2027-global-overview": "Digital 2027 global overview report",
    "datareportal-2027-indonesia": "Digital 2027: Indonesia",
    "datareportal-2027-internet-use": "Digital 2027: Internet use around the world",
    "reuters-faxes-phones": "Faxes, phones and Bluetooth: Microsoft outage forces businesses to find fixes",
    "reuters-outage-eases": "Microsoft restores service to Outlook and Teams after global outage",
    "aljazeera-2026-11-13-explainer": "Microsoft hit by global outages: What happened and why?",
    "sg-courts-advisory": "Advisory on disruption to SG Courts' email services",
    "wa-planning-notice": "Service notice: Microsoft outage",
    "vic-supreme-court-update": "Microsoft outage update",
    "workhorse-release-finviz": "Workhorse Group postpones third quarter earnings release and conference call",
    "fieldeffect-outage-theme": "Microsoft 365 outage theme drives credential phishing and support scams",
    "mimecast-held-messages": "Attackers exploit the Microsoft 365 outage with fake held messages lures",
    "microsoft-security-blog-lures": "High volume phishing campaign uses Microsoft 365 outage lures to target multiple industry sectors",
    "krdo-cnn-office-workers": "Massive Microsoft outage disrupts businesses, schools and governments around the world",
    "businessinsurance-financial-toll": "Microsoft outage's financial toll may fall short of disruption",
}


def main():
    for folder, title in TITLES.items():
        base = os.path.join(HERE, "sources", folder)
        page = next(f for f in sorted(os.listdir(base)) if f.endswith(".html"))
        with open(os.path.join(base, page), encoding="utf-8", errors="replace") as f:
            raw = f.read()
        raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
        text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw.replace("<br>", "\n"))).split())
        out = os.path.join(base, folder + ".txt")
        with open(out, "w", encoding="utf-8") as f:
            f.write(title + "\n\n" + text + "\n")
        digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
        print(f"{digest[:12]}  {len(text):>8} chars  sources/{folder}/{folder}.txt")


if __name__ == "__main__":
    main()
