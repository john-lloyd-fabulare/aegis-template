"""List every open task for one owner in the wiki, newest page first.

A task is an unticked line under a page's `## Tasks` heading that starts with
"<Owner>:" (bold or plain), for example `- [ ] Alex: send the deck`. The owner
match ignores case. Pages are dated by the (YYYY-MM-DD) in the filename, else
the frontmatter `date:`, else `created:`.

Tasks stay on the page that owns them. This script only reads them, so there
is never a second copy to go stale.

Usage:
    python .claude/scripts/owner_tasks.py --owner Alex            # all open tasks
    python .claude/scripts/owner_tasks.py --owner Alex --days 14  # pages from the last 14 days
    python .claude/scripts/owner_tasks.py --owner Alex --json     # rows with page, date, age_days, task
"""
import argparse, datetime as dt, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2] / "wiki"
FNAME_DATE = re.compile(r"\((\d{4}-\d{2}-\d{2})")
FM_DATE = re.compile(r"^(?:date|created):\s*(\d{4}-\d{2}-\d{2})", re.M)


def task_re(owner):
    return re.compile(r"^\s*- \[ \] \**" + re.escape(owner) + r"\**\s*:\**\s*(.+)$", re.I)


def page_date(path, text):
    m = FNAME_DATE.search(path.name) or FM_DATE.search(text[:600])
    return dt.date.fromisoformat(m.group(1)) if m else None


def collect(owner):
    task = task_re(owner)
    rows = []
    for p in ROOT.rglob("*.md"):
        if p.name in ("index.md", "log.md"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "- [ ]" not in text:
            continue
        in_tasks = False
        for line in text.splitlines():
            if line.startswith("## "):
                in_tasks = line.strip().lower().startswith("## tasks")
                continue
            if in_tasks:
                m = task.match(line)
                if m:
                    rows.append({"page": p.stem, "date": page_date(p, text), "task": m.group(1).strip()})
    rows.sort(key=lambda r: (r["date"] or dt.date.min, r["page"]), reverse=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True, help="name before the colon on the task line")
    ap.add_argument("--days", type=int)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rows = collect(a.owner)
    today = dt.date.today()
    if a.days is not None:
        cut = today - dt.timedelta(days=a.days)
        rows = [r for r in rows if r["date"] and r["date"] >= cut]
    for r in rows:
        r["age_days"] = (today - r["date"]).days if r["date"] else None
    if a.json:
        print(json.dumps(rows, default=str, ensure_ascii=False, indent=1))
        return
    print(f"{len(rows)} open {a.owner} tasks")
    page = None
    for r in rows:
        if r["page"] != page:
            page = r["page"]
            age = f"{r['age_days']}d" if r["age_days"] is not None else "undated"
            print(f"\n[[{page}]] ({age})")
        print(f"- [ ] {r['task']}")


if __name__ == "__main__":
    main()
