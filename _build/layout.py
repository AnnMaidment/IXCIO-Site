import os, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_build" / "pages"

NAV = [
    ("services", "Services"),
    ("whx-johannesburg", "WHX Johannesburg"),
    ("about", "About"),
    ("contact", "Contact"),
]

def head(title, desc, slug):
    canonical = "https://ixciodigihealth.com/" + ("" if slug == "index" else slug)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
</head>
<body>
"""

def header(slug):
    links = ""
    for s, label in NAV:
        cls = ' class="active"' if s == slug else ""
        links += f'<a href="/{s}"{cls}>{label}</a>\n      '
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="wordmark" href="/">IXCIO</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav" onclick="var n=document.getElementById('nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">Menu</button>
    <nav class="nav" id="nav">
      {links}
      <a class="btn btn-primary btn-sm" href="/contact">Request a meeting</a>
    </nav>
  </div>
</header>
"""

FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="wordmark" href="/">IXCIO</a>
        <p style="margin-top:.6rem;max-width:32ch">South African regulatory representation and market entry for medical devices, SaMD and AI-enabled devices.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="/services#represent">Licence holding &amp; representation</a></li>
          <li><a href="/services#register">SAHPRA registration</a></li>
          <li><a href="/services#advise">Regulatory advisory</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/about">About</a></li>
          <li><a href="/whx-johannesburg">WHX Johannesburg 2026</a></li>
          <li><a href="https://aletia-index.com" rel="noopener">Aletia Index</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></li>
          <li>Johannesburg, South Africa</li>
          <li><a href="/contact">Request a meeting</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>&copy; 2026 {{LEGAL_NAME}}. All rights reserved.</span>
      <span>Information on this site is general in nature and is not regulatory or legal advice for any specific product.</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

PLACEHOLDERS = {
    "EMAIL": os.environ.get("IXCIO_EMAIL", "info@ixciodigihealth.com"),
    "LEGAL_NAME": os.environ.get("IXCIO_LEGAL_NAME", "IXCIO (Pty) Ltd"),
    "BOOKING_URL": os.environ.get("IXCIO_BOOKING_URL", "/contact"),
    "FORM_ENDPOINT": os.environ.get("IXCIO_FORM_ENDPOINT", "https://formspree.io/f/REPLACE_ME"),
}

def build():
    for page in SRC.glob("*.html"):
        slug = page.stem
        raw = page.read_text()
        # first two lines: title / description
        lines = raw.split("\n", 2)
        title = lines[0].removeprefix("TITLE:").strip()
        desc = lines[1].removeprefix("DESC:").strip()
        body = lines[2]
        html = head(title, desc, slug) + header(slug) + body + FOOTER
        for k, v in PLACEHOLDERS.items():
            html = html.replace("{{" + k + "}}", v)
        (ROOT / f"{slug}.html").write_text(html)
        print("built", slug)

if __name__ == "__main__":
    build()
