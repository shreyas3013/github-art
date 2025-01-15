from datetime import date, timedelta

FONT = {
    'A': [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
    'B': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,1,0]],
    'C': [[0,1,1],[1,0,0],[1,0,0],[1,0,0],[0,1,1]],
    'D': [[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,1,0]],
    'E': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,1,1]],
    'H': [[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
    'I': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
    'L': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
    'O': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'P': [[1,1,0],[1,0,1],[1,1,0],[1,0,0],[1,0,0]],
    'R': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
    'S': [[0,1,1],[1,0,0],[0,1,0],[0,0,1],[1,1,0]],
    'V': [[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0]],
    'Y': [[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0]],
    ' ': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
}

def get_dates(text, year=2025, start_week=2, per_pixel=10):
    text = text.upper()
    jan1 = date(year, 1, 1)
    first_monday = jan1 - timedelta(days=jan1.weekday())
    dates = []
    week = start_week
    for ch in text:
        if ch not in FONT: continue
        pat = FONT[ch]
        for c in range(3):
            for r in range(5):
                if pat[r][c] == 1:
                    d = first_monday + timedelta(weeks=week+c, days=r+1)
                    if d.year == year:
                        for i in range(per_pixel):
                            dates.append((d, i))
        week += 4
    return sorted(dates)

commits = get_dates("SHREYAS", per_pixel=10)

with open("run.sh", "w") as f:
    f.write("#!/bin/bash\nset -e\ntouch art.txt\n")
    for i, (d, idx) in enumerate(commits):
        h = 10 + (idx % 8)
        m = (idx * 7) % 60
        t = f"{d}T{h:02d}:{m:02d}:00"
        f.write(f'echo "s{i}" >> art.txt\n')
        f.write(f'GIT_AUTHOR_DATE="{t}" GIT_COMMITTER_DATE="{t}" git add -A\n')
        f.write(f'GIT_AUTHOR_DATE="{t}" GIT_COMMITTER_DATE="{t}" git commit -m "SHREYAS {i+1}"\n')
    f.write('echo "Done!"\n')

print(f"Generated run.sh with {len(commits)} commits")
