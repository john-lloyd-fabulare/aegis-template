#!/usr/bin/env python3
"""LinkedIn lookup: people.json -> matches.json, profiles.json, roles.md. Needs APIFY_TOKEN."""
import json, os, re, sys, urllib.request, concurrent.futures as cf

def token():
    t = os.environ.get("APIFY_TOKEN")
    p = os.path.expanduser("~/.apify.env")
    if not t and os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            if l.startswith("APIFY_TOKEN="): t = l.split("=", 1)[1].strip()
    if not t: sys.exit("Set APIFY_TOKEN (see SKILL.md).")
    return t

TOK = token()

def run(actor, inp, timeout=240):
    r = urllib.request.Request(
        f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?token={TOK}&timeout={timeout}",
        data=json.dumps(inp).encode(), headers={"content-type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=timeout + 30))

STOP = {"inc", "llc", "ltd", "corp", "the", "and", "company", "group", "corporation", "limited", "international"}
def words(s): return [w for w in re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).split() if len(w) > 2 and w not in STOP]

def score(p, text):
    t = words(text)
    return sum(3 for w in words(p.get("company")) if w in t) + sum(1 for w in words(p.get("title")) if w in t)

def find(p):
    parts = p["name"].split()
    cands = []
    try:
        for h in run("harvestapi~linkedin-profile-search-by-name",
                     {"profileScraperMode": "Short", "firstName": parts[0], "lastName": " ".join(parts[1:]), "maxPages": 1}, 120):
            if h.get("linkedinUrl"):
                cands.append({"url": h["linkedinUrl"], "headline": h.get("position"), "score": score(p, (h.get("position") or "") + json.dumps(h.get("currentPositions") or ""))})
    except Exception as e:
        cands.append({"error": str(e)})
    cands = sorted([c for c in cands if "url" in c], key=lambda c: -c["score"])
    if (not cands or cands[0]["score"] < 3) and p.get("company"):
        # Common name: search name + company, LinkedIn's own ranking.
        last = parts[-1].lower()
        for attempt in range(2):
            try:
                hits = run("harvestapi~linkedin-profile-search", {"searchQuery": f"{p['name']} {p['company']}", "profileScraperMode": "Short", "maxItems": 3})
                hits = [h for h in hits if last in (h.get("firstName", "") + " " + h.get("lastName", "")).lower()]
                if hits: cands.insert(0, {"url": hits[0]["linkedinUrl"], "headline": hits[0].get("headline"), "score": 3, "via": "name+company search"})
                break
            except Exception:
                continue
    return p["name"], cands[:4]

KW = re.compile(r"\b(board|trustee|chair\w*|co-chair|vice[- ]chair|president|treasurer|secretary|advisory|steering|committee|council|association|consortium|alliance|coalition|institute|society|federation|foundation|chamber)\b", re.I)

def roles(prof):
    out = []
    for e in prof.get("experience") or []:
        t = f"{e.get('position')} @ {e.get('companyName')}"
        if KW.search(t): out.append(f"{t} ({(e.get('startDate') or {}).get('text','')} to {(e.get('endDate') or {}).get('text','')})")
    for v in prof.get("volunteering") or []:
        out.append(f"{v.get('role')} @ {v.get('organizationName')} ({(v.get('startDate') or {}).get('text','')} to {(v.get('endDate') or {}).get('text','')}) [volunteering]")
    for o in prof.get("organizations") or []:
        out.append(f"{o.get('positionHeld') or 'Member'} @ {o.get('name')} ({(o.get('startDate') or {}).get('text','')} to {(o.get('endDate') or {}).get('text','')}) [organizations]")
    for m in re.finditer(r"[^.]*\b(board|chair|advisory|committee|association|council)\b[^.]*\.", prof.get("about") or "", re.I):
        out.append("About: " + m.group(0).strip())
    return out

def main():
    if len(sys.argv) < 3: sys.exit("usage: lookup.py people.json outdir/")
    people = json.load(open(sys.argv[1], encoding="utf-8")); outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    with cf.ThreadPoolExecutor(4) as ex: found = dict(ex.map(find, people))
    pick = {n: c[0]["url"] for n, c in found.items() if c and c[0]["score"] >= 3}
    json.dump({"picked": pick, "candidates": found, "unmatched": [p["name"] for p in people if p["name"] not in pick]},
              open(f"{outdir}/matches.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    urls = list(pick.values()); profs = []
    for i in range(0, len(urls), 20):
        profs += run("harvestapi~linkedin-profile-scraper", {"profileScraperMode": "Profile details no email ($4 per 1k)", "queries": urls[i:i + 20]}, 600)
    json.dump(profs, open(f"{outdir}/profiles.json", "w", encoding="utf-8"), ensure_ascii=False)
    with open(f"{outdir}/roles.md", "w", encoding="utf-8") as f:
        for pr in profs:
            f.write(f"## {pr.get('firstName','')} {pr.get('lastName','')}\n{pr.get('linkedinUrl')}\n_{pr.get('headline')}_\n\n")
            f.writelines(f"- {r}\n" for r in roles(pr)); f.write("\n")
    print(f"matched {len(pick)}/{len(people)}; profiles {len(profs)}; see {outdir}/roles.md")

if __name__ == "__main__": main()
