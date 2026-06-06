# AGENTS.md — BigHomework_Python

Student homework repo for **Python Programming Design** course at Wuhan College (2025–2026 Sem 2).

## Repo state

- **No source code yet** — only two `.docx` files (course requirements + grading rubric) and `README.md`.
- **Branches:** `main` (default) and `Escape` — identical trees.
- Remote: `https://github.com/orange-sunshine/BigHomework_Python.git`
- `.docx` files are untracked (no `.gitignore`).

## Course requirements (from `9a8008c6575cb8721b9c38915d8730b5.docx`)

Pick **one** project type:
1. Data analysis & visualization
2. Utility tool
3. Interactive / text-based game
4. Web application or API client

**Deliverables:**
- Source code
- Project documentation (requirements, dependency list, user guide)
- Course design report (UML use-case diagrams, system design, module breakdown, screenshots)
- Execution demo video

**Grading:** Process 40% + Final 60%.
- Project implementation (60 pts): core features (20), extended features (10), modular design (10), comments (5), error handling (5), user-friendly prompts (5), algorithm difficulty (5)
- Course design report (30 pts): requirements analysis (5), use-case diagram (5), system/module design (10), screenshots (5), formatting (5)
- Presentation & Q&A (10 pts)

## Useful commands

```bash
# extract text from assessment docx
pip install python-docx
python -c "import docx; print(docx.Document('9a8008c6575cb8721b9c38915d8730b5.docx').tables)"
```

## Style notes

As this is a course project, follow standard Python conventions (PEP 8). Use modular design with functions/classes. Include docstrings and inline comments at key logic points.

## Game Project: 2D Roguelite Survivors

Build a 2D top-down "bullet heaven" game with Pygame.  
Core loop: player moves with WASD, auto-attacks nearest enemies, kills grant XP, level-up picks from 3 random upgrades (stats, new weapons, passives). Waves of enemies grow stronger.

### Technical constraints
- Python 3.11+, Pygame 2.x
- Only one `requirements.txt` with `pygame`
- At least 4 modules: `main.py`, `entities.py`, `systems.py`, `ui.py`
- Save/load high scores to JSON
- All user-facing texts in English
- PEP 8, docstrings on every function, inline comments on non‑trivial logic
- Must demonstrate an algorithm beyond basic loops: e.g. nearest‑enemy targeting (Euclidean distance), wave scaling formula, random upgrade generation with rarity weights

### Deliverables (matching course)
- Source code (all `.py`)
- `README.md` (how to install, run, controls, scoring)
- `DESIGN.md` (UML use‑case text diagram, system design, module breakdown, algorithm explanation, screenshot placeholder)
- Demo video instructions (just note in README how to record)