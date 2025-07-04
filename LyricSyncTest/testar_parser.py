import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.lrc_parser import parse_lrc

lrc_path = "assets/lrc/teste.lrc"
estrofes = parse_lrc(lrc_path)

for tempo, texto in estrofes:
    print(f"[{tempo:.2f}s] {texto}")
