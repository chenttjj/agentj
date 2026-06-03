from pathlib import Path

ROOT = Path('studio_shell')
KEYWORDS = ['Piano Roll', 'piano roll', 'instrument', '樂器', 'guitar', 'bass', 'synth', 'piano']

for path in ROOT.rglob('*.py'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    hits = []
    for i, line in enumerate(text.splitlines(), start=1):
        if any(k in line for k in KEYWORDS):
            hits.append((i, line.strip()))
    if hits:
        print(f'FILE: {path}')
        for i, line in hits[:30]:
            print(f'  {i}: {line}')
        print()
