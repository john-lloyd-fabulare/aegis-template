---
name: linkedin-lookup
description: Find people's public LinkedIn profiles from a name and company, pull the full profile (experience, volunteering, organizations, about), and list every board, chair, committee and advisory role they hold. Use when asked to "look up these people on LinkedIn", "find their board seats", "what other boards / associations is X on", or to enrich a roster (board, speakers, attendees, prospects) with LinkedIn data.
---

# LinkedIn lookup

Reads **public** LinkedIn profiles through two Apify actors published by HarvestAPI. No LinkedIn login is used.

| Step | Actor | Cost |
|---|---|---|
| Find the person | `harvestapi/linkedin-profile-search-by-name` (name), then `harvestapi/linkedin-profile-search` (name + company) when the name is common | about $0.004 to $0.10 per person |
| Full profile | `harvestapi/linkedin-profile-scraper`, mode "Profile details no email" | $0.004 per profile |

A 70-person board costs about $3 to $5 in total.

## Setup (once)

1. Make an account at https://apify.com and copy your API token (Settings → API & Integrations).
2. Put the token in `~/.apify.env` (in your home folder, outside the vault) as one line, `APIFY_TOKEN=...`. The principal does this step themselves.

## Use

Input is a JSON list of people; `company` and `title` improve matching a lot.

```bash
python .claude/skills/linkedin-lookup/scripts/lookup.py people.json out/          # [{"name": "...", "company": "...", "title": "..."}]
```

Writes to `out/`:
- `matches.json`: the LinkedIn URL chosen for each person, the match score, and runner-up candidates
- `profiles.json`: full raw profiles
- `roles.md`: per person, every board / chair / committee / council / association / advisory role found in experience, volunteering, organizations and the About section, with dates

## Rules

- **Check every match.** Common names match the wrong person (one "Mark Ferguson" on a test board came back as a J.P. Morgan analyst). A match with score 0 is a guess; the script leaves it out and lists it under "unmatched" in `matches.json` for you to resolve by hand.
- A role on LinkedIn is self-reported. For anything going into a report, mark it "LinkedIn (self-reported)" or confirm it on the organization's own site.
- Distinguish **current** (end date "Present") from past roles.
- Public data only. Don't use this to build lists of private individuals for outreach without a reason they'd expect; don't store profiles longer than the project needs.
- Pair with ProPublica Nonprofit Explorer for an association's revenue: `https://projects.propublica.org/nonprofits/api/v2/search.json?q=<name>` then `/organizations/<ein>.json` (`filings_with_data[].totrevenue`). Free, no key.

## Vault rules

- **The token never enters the vault.** It lives only in `~/.apify.env`, outside the repo. Never paste it into a page, a log or chat output.
- **Write output to the session scratchpad, not the vault.** `profiles.json` holds full personal profiles. Only the findings go into the vault (a lead list or overlap sheet), each role labelled "LinkedIn (self-reported)". Delete the raw output files after.
- **Looking people up is not outreach.** If a client or partner must approve contact, nothing found here is used to contact anyone until they do.
- **Run it only when the principal asks.** Each run spends money on the principal's Apify account. State the head count and the expected cost before running.
