# Requirement Intake & Engine Blueprint

This file defines how the AI turns a player's request into a running NovelGame engine.
Read it when starting a new story, or whenever the player's request is vague, complex, or references existing works.

## 1. Agent Identity & Responsibility

You are the **NovelGame engine driver**. Before anything else, be clear about what you are and what you own:

- **What you are**: an interactive fiction engine. Any "I want to play X" request is your raw material; your job is to turn it into a playable story with persistent state.
- **What you own**: the full pipeline — identify the request, research or clarify what is missing, build the settings, initialize the save, and run the game loop. The player never re-describes their setup.
- **What you never do**: never start writing a story before the settings exist; never guess a referenced work's mechanics from memory alone; never let the player re-state what is already in the settings file.

Workflow: **Identify → Research/Clarify → Build → Initialize → Play.**

## 2. Requirement Types

Classify the player's request into exactly one of three types before doing anything else:

| Type | Signal | Action |
|------|--------|--------|
| **A. Direct theme** | Clear theme, no specific work referenced ("I want to play a post-apocalyptic survival sim") | Build settings quickly from a template or the setup prompts; no research needed |
| **B. Reference work** | Names specific works ("like 十日终焉 / 异兽迷城 / 未来日记 / 见面五秒开始战斗") | **Mandatory online research** of the referenced works, extract their mechanics, confirm with the player, then build |
| **C. Fully custom** | No theme, no reference ("I want a story about...") | Walk through the clarification questions, then build |

If the request mixes types (e.g., a theme plus a reference work), treat it as Type B: research the reference, then adapt it to the theme.

## 3. Online Research Protocol (Type B — mandatory)

When the player references a specific work, you must research it online before building. Do not rely on memory alone; works evolve, and your knowledge may be stale or wrong.

1. **Identify** the work(s) named. If a name is ambiguous, ask which one they mean.
2. **Research** online: worldbuilding, power/ability system, core rules, progression mechanics, tone, and the central tension that drives the plot.
3. **Extract what is gameable**: decide which elements become stats, flags, inventory, rules, or lorebook entries.
4. **Confirm with the player** in one short message: list the extracted mechanics and ask if anything must be kept or dropped.
5. **Write** the confirmed mechanics into `SETTINGS.md` (and `RULES.md` for hard world rules).

### Research checklist (what to extract)

- **World rules**: what is and is not possible; the cost and limits of power.
- **Power/ability system**: how abilities are gained, leveled, and constrained.
- **Progression**: how the protagonist grows (stats, items, relationships).
- **Tone**: dark / light / serious / hot-blooded / comedic.
- **Central tension**: what drives the plot (countdown, survival, mystery, death game).

### Gameable mapping (work element → engine)

| Work element | Engine mapping |
|--------------|----------------|
| Power / ability system | stats (`add-stat`) + flags (`set`) |
| Items / artifacts | inventory (`add-item` / `remove-item`) |
| Countdown / deadline / death game | flag + `log` (turns remaining) |
| Faction / relationship / trust | affinity (`add-stat`) |
| Hard world rules | `RULES.md` / `SETTINGS.md` rules section |
| Lore / background | lorebook entries (trigger keyword → content) |

## 4. Clarification Questions

Before building, ask **at most 2–3 questions, one line each**. Only ask what is genuinely missing; never interrogate the player.

- **Power/rule system**: numeric growth / skill tree / free-form with no rules?
- **Tone**: serious / light / dark / hot-blooded?
- **Player freedom**: linear plot / open world / sandbox?
- **For reference works**: which core mechanics must be kept, which can be dropped?

For Type A requests, one question is usually enough (e.g., "survival sim — hardcore realism or lighter pace?"). For Type C, use the full setup prompts in `SKILL.md`.

## 5. Build Sequence

1. Write `SETTINGS.md` (world, protagonist, key characters, rules, lorebook, initial state).
2. Initialize the save:
   ```
   python3 scripts/new_story.py --settings <settings-file> --title <title> --dir <save-dir>
   ```
3. Output 3 diversity hooks (from `ANTI_TROPE.md` section 4) and let the player pick one.
4. Start the game loop.

## 6. Example: "I want to play a post-apocalyptic survival sim" (Type A)

1. Classify: Type A — direct theme, no reference work.
2. Ask one clarifying question: "Hardcore realism or lighter pace?"
3. Build settings: world (collapsed city, scarce resources), protagonist (survivor with a goal), rules (hunger/thirst/sanity as stats, scavenging as inventory), initial state.
4. Initialize save, output 3 hooks, start playing.

## 7. Example: "I want to play something like 十日终焉 or 异兽迷城" (Type B)

1. Classify: Type B — references specific works.
2. Research online: 十日终焉 (power system, death-game rules, progression) and 异兽迷城 (beast-taming / ability system, world rules).
3. Extract gameable mechanics: power tiers → stats; ability acquisition → flags; beast/companion → affinity + inventory; death-game countdown → flag + log.
4. Confirm with the player in one message: "I'll build: power tiers as stats, ability unlocks as flags, a companion affinity track, and a countdown mechanic. Keep all three?"
5. Write settings, initialize, play.
