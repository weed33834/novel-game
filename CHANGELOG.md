---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 98adaa6f98486df4666888a6691e7607_87c0ee529a4011f19467525400287e28
    ReservedCode1: wj+zjRadru9/Zla+EgjRfrxqUhcKfuS9LbVfSVRaaGOdvSkUf0utGduLHsVz2iwPjyVFvCBGkvRVvlworepMwuuVuZvN7MVptUQJuNXhfWiaIoBaCn24Vpcdds8nZ/5/aXewPbNa/GuU5o+36pG9TF8r4UVTyDPBvmDXz2HJUr3opc+vADzxmKfryP8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 98adaa6f98486df4666888a6691e7607_87c0ee529a4011f19467525400287e28
    ReservedCode2: wj+zjRadru9/Zla+EgjRfrxqUhcKfuS9LbVfSVRaaGOdvSkUf0utGduLHsVz2iwPjyVFvCBGkvRVvlworepMwuuVuZvN7MVptUQJuNXhfWiaIoBaCn24Vpcdds8nZ/5/aXewPbNa/GuU5o+36pG9TF8r4UVTyDPBvmDXz2HJUr3opc+vADzxmKfryP8=
---

# Changelog

All notable changes to NovelGame are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.7.0] - 2026-08-18

### Added
- **Gameplay systems** in `scripts/state.py` — this is an interactive game, not a novel. New commands make outcomes deterministic, goals trackable, and choices consequential:
  - `roll --dice <N> [--mod <N>] [--dc <N>]`: dice/check resolution (d20 default) with optional modifier and difficulty class, replacing free-form judgment for actions with a meaningful chance of failure.
  - `quest --action <add|update|complete|fail> --id <id> [--title] [--desc] [--progress]` and `quest-list`: persistent quest tracking with active/completed/failed status.
  - `combat --action <start|attack|end> [--enemy] [--hp] [--atk] [--damage] [--result]` and `combat-status`: save-tracked combat with enemy HP/ATK, win/lose/flee results.
  - `ending --id <id> --title <title>` and `ending-list`: ending recording and accumulation across playthroughs.
  - `encounter --pool '<json>' [--avoid <N>]`: weighted random encounter scheduling from the blueprint's Encounter Pool, avoiding recently used events.
- **`SKILL.md` "Gameplay Systems" section**: engine guidance on when to use each system (dice for checks, quests for goals, combat for fights, endings for terminal outcomes, encounters for event scheduling), with the rule that raw rolls/numbers are never shown to the player.

### Changed
- `SKILL.md`: State Command Reference extended with the 8 new gameplay commands.
- `plugin.json`: version 0.7.0; description now advertises the gameplay systems (dice/checks, quests, combat, endings, encounters).

## [0.6.0] - 2026-08-17

### Added
- **Engine Blueprint** (`references/BLUEPRINT.md`): a mandatory engine-internal backstage brief written before every story starts, stored next to the save (e.g. `<save-dir>/blueprint.md`). It covers four sections — **Genre System Brief** (what this genre/setting is: core premise, typical rules, typical elements), **Current Situation** (world state, main conflict, timeline/countdown at story start), **Encounter Pool** (events, factions, key characters, threats, side quests the protagonist is likely to run into), and **Direction & Tone** (core direction, possible endings, tone, player freedom).
- **Blueprint purpose**: the engine draws every scene, encounter, and branch from the blueprint, so the story has direction instead of drifting; re-read it at session start.
- **Worked intake example** in `INTAKE.md`: "I want to experience urban supernatural powers" (都市异能, Type A) showing a full blueprint (hidden supernatural layer, power vacuum, mentor/rogue/agency/syndicate/artifact encounter pool, survive-and-choose-a-side direction).

### Changed
- `SKILL.md`: "Starting a New Story" now has a mandatory **Step 2 — Write the Engine Blueprint** (engine-internal, never shown to the player) between building settings and initializing the save; the blueprint is listed under Player-invisible in Information Layering.
- `RULES.md`: new mandatory "Engine Blueprint" rule — write the blueprint before starting, re-read it at session start, and never output or hint at it to the player.
- `INTAKE.md`: Build Sequence now includes writing the Engine Blueprint as step 2; the survival and 十日终焉/异兽迷城 examples updated to include blueprint steps.
- `plugin.json`: version 0.6.0; description now advertises the engine blueprint (genre brief, current situation, encounter pool, direction) as the backstage guide that keeps stories coherent and directed.

## [0.5.0] - 2026-08-17

### Added
- **Agent Identity & Responsibility** section in `SKILL.md`: the engine driver now knows what it is (an interactive fiction engine) and what it owns (identify → research/clarify → build → initialize → play) before acting.
- **Requirement Intake protocol** in `references/INTAKE.md`: classifies every request into three types — A. Direct theme, B. Reference work, C. Fully custom — with a mandatory online research protocol for Type B (extract power system → stats, items → inventory, countdown → flags, relationships → affinity, world rules → RULES.md, confirm with the player, then build).
- **Clarification question rules**: at most 2–3 one-line questions (power/rule system, tone, player freedom), only for what is genuinely missing; never interrogate the player.
- **Worked intake examples** in `INTAKE.md`: "post-apocalyptic survival sim" (Type A) and "like 十日终焉 / 异兽迷城" (Type B).

### Changed
- `SKILL.md`: new "Starting a New Story" flow with mandatory Step 0 (Requirement Intake) before building settings; setup prompts now reference the intake protocol.
- `RULES.md`: new mandatory "Requirement Intake" rule — Type B requests must be researched online, never guessed from memory.
- `plugin.json`: version 0.5.0; description now advertises request-type identification and online research of referenced works.

## [0.4.0] - 2026-08-17

### Added
- **Game templates**: 4 ready-to-play settings in `references/templates/` — STARFALL (space opera, EN), DRAGON_ACADEMY (fantasy school, EN), JIANGHU (wuxia, ZH), NEON_NOIR (cyberpunk noir, EN). Copy one and start with a single command.
- **README "Game Templates" section** with a template table and one-command quick start.
- **README "Writing Settings: the Initial State Section"** documenting that the parser reads only the `## Initial State` / `## 初始状态` / `## 初期状態` section.

### Changed
- `SETTINGS.md` template: expanded the Initial State section with a clear "only section the parser reads" note, format rules, and worked examples in English, Chinese, and Japanese.
- `SKILL.md`: starting-a-new-story flow now points to the ready-to-play templates.

## [0.3.1] - 2026-08-17

### Added
- **Multilingual READMEs**: `README.zh-CN.md` (Chinese) and `README.ja.md` (Japanese), with a language switcher at the top of each README.
- **Shields.io badges** in README: License, Python version, Agent Plugins spec, output languages, zero dependencies, PRs welcome.
- **"Why NovelGame?"** pain-point comparison table and a **Demo** turn from the bundled example to make the value proposition instantly clear.
- **"Support the Project"** section with a star/share/contribute call to action.

## [0.3.0] - 2026-08-17

### Changed
- Renamed plugin from `interactive-novel-engine` to **NovelGame** (`novel-game`).
- Relicensed from MIT to **Apache License 2.0**; added `LICENSE`, `README.md`, `CONTRIBUTING.md`, `.gitignore`, and `CHANGELOG.md` for open-source release.
- **English-first rewrite**: `SKILL.md`, `RULES.md`, `ANTI_TROPE.md`, `SETTINGS.md`, `EXAMPLE.md`, and both scripts are now in English with domain-optimized terminology (affinity, inventory, flags, lorebook, tiered memory, chapter snapshot, dynamic context injection, ToT branch planning, anti-trope).
- Added **multilingual narrative output**: English (default), Chinese, and Japanese, switchable via the settings file or in-session command.
- `new_story.py` initial-state parser now accepts English, Chinese, and Japanese section keywords.

## [0.2.0] - (previous)

### Added
- Tiered memory (short/mid/long), ToT branch planning, narrative quality scoring, chapter snapshots, and dynamic context recovery.

## [0.1.0] - (initial)

### Added
- Initial interactive fiction engine: settings-as-files, state-as-scripts, branching saves.
*（内容由AI生成，仅供参考）*
