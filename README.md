# IXCIO website

Static site for ixciodigihealth.com, deployed on Vercel. No build step: the HTML files at the root are what gets served.

## Editing

Page sources live in `_build/pages/*.html` (first line = title, second = meta description, rest = body). Shared header/footer are in `_build/layout.py`. Regenerate the root HTML with:

    python3 _build/layout.py

Or edit the root `.html` files directly for quick changes — just keep header/footer consistent.

## Placeholders to replace before launch

Set these as environment variables when running the build, or find-and-replace in the generated HTML:

| Placeholder | Where | Current value |
|---|---|---|
| `IXCIO_EMAIL` | footer, contact page | info@ixciodigihealth.com |
| `IXCIO_LEGAL_NAME` | footer copyright | IXCIO (Pty) Ltd |
| `IXCIO_FORM_ENDPOINT` | contact + WHX forms | formspree.io/f/REPLACE_ME — create a free Formspree form, paste its endpoint |

Also confirm: bio wording and photo on `/about`; the licence-status paragraph on `/services`.

## Deploy

Push to `main` → Vercel deploys. Preview deployments come from any other branch.

## Going live on ixciodigihealth.com

In Vercel: Project → Settings → Domains → add `ixciodigihealth.com` and `www.ixciodigihealth.com`. In Wix's DNS panel: set the root A record and the `www` CNAME to the values Vercel shows. Do NOT change nameservers; leave MX/SPF/DKIM/TXT records untouched.
