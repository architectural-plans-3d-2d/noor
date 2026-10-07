import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

text = Path("scripts/daata_hamlet/model.py").read_text(encoding="utf-8")
print(f"Read {len(text)} chars from model.py")
