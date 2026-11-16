# Sitemap board tools

Used to build the Whiteboard sitemap of the guide (every page and every link).

1. `python3 graph.py ../../releases/GM_Early_Years_App_iPhone_vX.XX.html` writes `graph.json` (pages in Next order, with their Next, Back, answer, menu and in-text links).
2. `python3 board.py` turns `graph.json` into `batch0.json`… (Whiteboard element writes, 50 per batch).

Board for v2.52: https://claude.ai/artifact/V7jvUseLZMcJQB78yRi3YY
