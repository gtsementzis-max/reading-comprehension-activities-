# Reading Comprehension Activities — project guide (for Claude Code)

Two kids' reading sites in **one** static-HTML repo, hosted on GitHub Pages.
No build step, no framework — plain HTML/CSS/JS. Everything runs offline.

- **Amara** — grade 5. Hub: `index.html`. Storage key: `amaraReading`.
- **Dani** — grade 2. Hub: `dani.html`. Storage key: `daniReading`.
- **Landing page**: `who.html` — "Who's reading?" chooser linking to both hubs.

Live site: https://gtsementzis-max.github.io/reading-comprehension-activities-/
Repo: `gtsementzis-max/reading-comprehension-activities-` (branch `main`, Pages serves `/` root).
Local folder: `C:\Users\gtsem\OneDrive\Desktop\reading comprehension` (inside OneDrive —
if git throws permission errors, pause OneDrive sync and retry).

---

## File map

| File(s) | What it is | Maintained how |
|---|---|---|
| `index.html` | Amara's hub (dashboard of all her modules) | **hand-edited** |
| `dani.html` | Dani's hub | **hand-edited** |
| `who.html` | Landing/chooser page | hand-edited |
| `build_modules.py` | Generator for all the per-module activity pages | edit + run |
| `amara-<key>-reading.html` (18) | Amara activity pages | **generated** by build_modules.py |
| `dani-<key>-reading.html` (13) | Dani activity pages | **generated** by build_modules.py |
| `amara-marine-life-reading.html`, `amara-bees-reading.html` | 2 original Amara modules | hand-made, **NOT** in the generator |
| `amara-write-a-summary.html` | Writing lesson (not score-counted) | hand-made |
| `amara-typing-quest.html` | Touch-typing game (in-memory only) | hand-made |

> The generator only owns the 31 `*-reading.html` activity pages it lists in `MODULES`.
> The hubs, the two originals, the writing lesson, the typing game, and `who.html`
> are separate hand-maintained files. Re-running the generator does **not** touch them.

---

## How to run the generator

```bash
python build_modules.py
```
It writes every module in its `MODULES` list into **its own folder** (the repo folder).
Override the output dir with the `OUT_DIR` env var if needed. Re-running overwrites
the generated module files only.

---

## How to ADD a new reading module

1. Open `build_modules.py`, copy an existing entry in the `MODULES` list, and edit it.
2. **Pick the child** with these per-module fields:
   - Amara (default): omit `name`/`hubKey`/`hubFile` — they default to `Amara` / `amaraReading` / `index.html`.
   - Dani: set `"name":"Dani"`, `"hubKey":"daniReading"`, `"hubFile":"dani.html"`, and a gentle `"useLead"`.
3. **Match the grade format** (counts matter — the hub bars read these):
   - **Amara (grade 5):** `questions` ×6, `match` ×6, `bank`/`fills` ×8, with **exactly one** fill flagged `"challenge":True` (the ★ transfer item). Per-sub totals **6 / 6 / 8**.
   - **Dani (grade 2):** `questions` ×5, `match` ×5, `bank`/`fills` ×6, **no** challenge item. Per-sub totals **5 / 5 / 6**.
4. Give the module a unique `activityId` and `projectKey`, and a **new distinct palette** hex
   (see the "Amara Reading Modules Catalogue" / "Dani Reading Modules Catalogue" entities in
   Genesis for colors already used — don't repeat one).
5. Run `python build_modules.py`. Output file is `amara-<activityId>-reading.html` (or
   `dani-<activityId>-reading.html` when `name=="Dani"`).
6. **Wire it into the hub** (`index.html` for Amara, `dani.html` for Dani):
   - Add one `.proj` card: a `.proj-head` (`.dot` color + `<h2>` + Open `<a>` to the file) and
     three `.act-row`s, each with `<div class="bar" data-k="<projectKey>:comprehend|match|use" data-total="6|6|8">`
     (use `5|5|6` for Dani) and a `<span class="act-score" data-s="...">`.
   - Add a CSS rule `.dot.<projectKey>{background:<primaryHex>}`.
   - Bump the JS `var totalActivities` to (number of projects × 3) **and** the static `0 / N` summary text.
7. Validate: every `fills` answer must exist in that module's `bank`; no leftover `%%TOKENS%%`;
   counts match the grade format above.

> ⚠️ Python gotcha: `challenge:True` must be **capitalized** (Python bool), not `true`.

---

## SCORING CONTRACT (do not break this)

A module saves to `localStorage` under its hub key (`amaraReading` or `daniReading`) as:
```
data["<projectKey>:comprehend" | ":match" | ":use"] = { best:int, attempts:int }
```
- "best score wins" — a retry never lowers a previous best.
- After saving, the module dispatches `window` event `amara-scores-updated`
  (same event name for both kids — the hubs listen for it) and defensively calls
  `window.amaraCloud.save/set/sync` if that global exists.
- The hub bar's `data-total` MUST equal the number of items in that step, or the bar
  shows "not yet". (Amara 6/6/8, Dani 5/5/6.)

If you change item counts, update **both** the module and its hub tile's `data-total`.

---

## Publish workflow

```powershell
cd "C:\Users\gtsem\OneDrive\Desktop\reading comprehension"
git add .
git commit -m "your message"
git push
```
Wait ~1 min, then hard-refresh (Ctrl+F5). First push may need a GitHub Personal Access
Token as the password.

---

## Content cautions (carried from earlier review)

- Boa "suffocate" is the traditional textbook simplification; modern science says constriction
  kills mainly via blood-flow / cardiac arrest. *(Amara boa module.)*
- "Wheel used for pottery before transport" — plausible but the chronology is debated. *(Amara wheel module.)*
- Roblox passage is an **original factual description** of the platform only — no copyrighted
  characters, logos, or game text. Keep it that way if edited.

## Status flags to verify (not assumed true)

- Cross-device Firebase/Firestore sync is **UNVERIFIED** for generator-built modules; only
  on-device localStorage scoring is confirmed.
- Whether `amara-typing-quest.html` and `who.html` are already pushed live is **unconfirmed** —
  check the live URLs.

Full project history lives in Genesis (knowledge graph) under: **Amara Reading Project**,
**Amara Reading Module Recipe**, **Amara Reading Modules Catalogue**, **Dani**,
**Dani Reading Modules Catalogue**.
