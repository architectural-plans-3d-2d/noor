import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

import scratch.test_model_edit

import scratch.test_model as tm
m = tm.build()
tm.validate(m)
print("ALL 121 CHECKS PASS PERFECTLY IN TEST MODEL!")
