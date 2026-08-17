# NovelGame

> **Never re-describe your story setup again.** A self-contained interactive fiction engine for AI agents — package your worldbuilding, characters, and rules once, and the AI auto-loads them every session, with progress that survives context loss.

**Read this in:** [English](README.md) · [中文](README.zh-CN.md) · [日本語](README.ja.md)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Agent Plugins](https://img.shields.io/badge/Agent%20Plugins-1.0.0-blue.svg)](https://agent-plugins.org)
[![Output Languages](https://img.shields.io/badge/Output-EN%20%7C%20%E4%B8%AD%E6%96%87%20%7C%20%E6%97%A5%E6%9C%AC%E8%AA%9E-blue.svg)](README.md)
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-Yes-brightgreen.svg)](skills/novel-game/scripts/state.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)

Built as an [Agent Plugins](https://agent-plugins.org) 1.0.0 plugin (Working Draft).

## Why NovelGame?

| Pain point | Typical AI chat | With NovelGame |
|------------|-----------------|----------------|
| **Re-describing setup** | You re-explain your world, characters, and rules every session ("half an hour of setup, every time") | Settings are files — written once, auto-loaded forever |
| **Lost progress** | Story state evaporates when context gets compressed or you open a new chat | State lives in JSON saves on disk; chapter snapshots + dynamic context injection recover it — recovery is never a restart |
| **AI-flavored writing** | Generic, clichéd prose that all sounds the same | Anti-trope engine: cliché blacklist, sensory-first rules, non-typical plot idea bank, and self-scored narrative quality |

## Features

- **Settings are files** — write your world once, every session auto-loads it.
- **State is scripts** — all progress, affinity, inventory, flags, and branch history persist to JSON saves via `state.py`; game state survives context loss and new sessions.
- **Tiered memory** — short-term (recent events), mid-term (chapter summaries), and long-term (player-preference reflections) keep long stories coherent.
- **Chapter snapshots + dynamic context injection** — recover seamlessly after context compression or a new session; recovery is never a restart.
- **ToT branch planning** — internally evaluates 3–5 story directions and keeps only the strongest 2–4 choices.
- **Narrative quality scoring** — self-evaluates each output on OOC, settings consistency, coherence, anti-trope strength, and choice quality.
- **Anti-trope engine** — a cliché blacklist, sensory-first writing rules, and a non-typical plot idea bank to avoid AI-flavored prose.
- **English-first, multilingual output** — engine rules and commands are in English for precision; narrative output can switch between **English, Chinese, and Japanese**.

## Language Support

| Language | Code | Narrative output |
|----------|------|------------------|
| English (default) | `en` | Yes |
| Chinese | `zh` | Yes |
| Japanese | `ja` | Yes |

- Engine rules, commands, and internal script output are always in English for unambiguous instruction-following.
- Set the default narrative language in your settings file (`## Language: en|zh|ja`), or switch at any time by saying "switch to Chinese", "用中文", "日本語に切り替えて", etc.
- Settings files may be authored in English, Chinese, or Japanese; the initial-state parser accepts all three.

## Quick Start

```bash
# 1. Copy the settings template and fill it in
cp skills/novel-game/references/SETTINGS.md my_story.md

# 2. Initialize a save from your settings
python3 skills/novel-game/scripts/new_story.py --settings my_story.md --title "My Story" --dir ./saves

# 3. Start playing — the engine reads the state each turn
python3 skills/novel-game/scripts/state.py summary --dir ./saves
```

Or start instantly from the bundled example:

```bash
python3 skills/novel-game/scripts/new_story.py \
  --settings skills/novel-game/references/EXAMPLE.md \
  --title "The Fogbound Detective" --dir ./saves
```

## Game Templates

Ready-to-play settings live in `skills/novel-game/references/templates/`. Copy one, tweak it, and start — no setup needed:

| Template | Genre | Language | Premise |
|----------|-------|----------|---------|
| [STARFALL.md](skills/novel-game/references/templates/STARFALL.md) | Space opera | English | A lost colony ship answers a signal from an alien megastructure |
| [DRAGON_ACADEMY.md](skills/novel-game/references/templates/DRAGON_ACADEMY.md) | Fantasy school | English | Students vanish as a sealed vault leaks black mist |
| [JIANGHU.md](skills/novel-game/references/templates/JIANGHU.md) | Wuxia | Chinese | A wandering swordsman hunts the truth behind a massacre |
| [NEON_NOIR.md](skills/novel-game/references/templates/NEON_NOIR.md) | Cyberpunk noir | English | A detective holds a memory-rewriting chip worth killing for |

```bash
# Start from a template in one command
python3 skills/novel-game/scripts/new_story.py \
  --settings skills/novel-game/references/templates/STARFALL.md \
  --title "Starfall" --dir ./saves
```

## Writing Settings: the Initial State Section

The initial-state parser reads **only** the `## Initial State` section (English), `## 初始状态` (Chinese), or `## 初期状態` (Japanese) of your settings file. Stats, inventory, and flags written anywhere else are ignored. One entry per line, `Key: value`:

```markdown
## Initial State
Affinity: Erin=10, Old Hawke=20
Inventory: old pocket watch, case files
Special flags: met_erin=true
```

See [SETTINGS.md](skills/novel-game/references/SETTINGS.md) for the full template and examples in all three languages.

## Demo

A turn from the bundled example, *The Fogbound Detective* (English output):

> **You** (to Erin, the forensic pathologist): "I need to see the case files from the harbor warehouse fire."
>
> **NovelGame** — *Erin's eyes narrow. She slides a manila folder across the table, her fingers lingering on the edge. "The fire was no accident. Someone wanted those records gone."* (affinity +5)
>
> 1. Ask her what she found in the ashes.
> 2. Take the folder and leave without a word.
> 3. Tell her you trust her judgment — and mean it.

The engine tracked your affinity with Erin, updated the inventory, and logged the event — all persisted to the JSON save, ready for the next session.

## Repository Layout

```
novel-game/
├── LICENSE                     # Apache License 2.0
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
├── plugin.json                 # Agent Plugins manifest
└── skills/
    └── novel-game/
        ├── SKILL.md            # Engine instructions (English)
        ├── scripts/
        │   ├── state.py        # State management CLI (JSON saves)
        │   └── new_story.py    # Initialize a save from a settings file
        └── references/
            ├── SETTINGS.md     # Story settings template
            ├── RULES.md        # Mandatory engine rules
            ├── ANTI_TROPE.md   # Anti-cliché checklist & idea bank
            ├── EXAMPLE.md      # Ready-to-play example story
            └── templates/      # Ready-to-play game templates
                ├── STARFALL.md        # Space opera (English)
                ├── DRAGON_ACADEMY.md  # Fantasy school (English)
                ├── JIANGHU.md         # Wuxia (Chinese)
                └── NEON_NOIR.md       # Cyberpunk noir (English)
```

## State Command Reference

```
python3 scripts/state.py init --title <title> [--settings <file>] [--dir <dir>]   # create a save
python3 scripts/state.py get [--story <id>] [--dir <dir>]                        # read full state
python3 scripts/state.py summary [--story <id>] [--dir <dir>]                    # compact state summary
python3 scripts/state.py set --key <flag> --value <value> [--dir <dir>]          # set a flag
python3 scripts/state.py add-stat --key <stat> --delta <delta> [--dir <dir>]     # adjust a stat
python3 scripts/state.py add-item --item <item> [--dir <dir>]                    # add to inventory
python3 scripts/state.py remove-item --item <item> [--dir <dir>]                 # remove from inventory
python3 scripts/state.py set-node --node <node> [--dir <dir>]                    # set current node
python3 scripts/state.py log --event <event> [--dir <dir>]                       # record an event
python3 scripts/state.py remember --tier <short|mid|long> --content <content> [--dir <dir>]
python3 scripts/state.py recall --tier <short|mid|long> [--keyword <word>] [--limit N] [--dir <dir>]
python3 scripts/state.py reflect --content <reflection> [--dir <dir>]            # write player-preference reflection
python3 scripts/state.py snapshot --scene <scene> --characters <chars> --goal <goal> --threads <threads> [--dir <dir>]
python3 scripts/state.py restore [--dir <dir>]                                    # recover from latest snapshot
python3 scripts/state.py context [--dir <dir>]                                    # full context block for recovery
python3 scripts/state.py list [--dir <dir>]                                      # list saves
```

Save directory priority: `--dir` argument > `$NOVEL_DATA_DIR` > `./saves`.

## Requirements

- Python 3.10+ (standard library only, no third-party dependencies)

## Support the Project

If NovelGame saves you from re-describing your setup one more time, consider:

- **Star this repository** — it's the single best way to help others discover it.
- **Share it** with friends who play or write interactive fiction with AI.
- **Report issues** or request features in the Issues tab.
- **Contribute** — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

## License

[Apache License 2.0](LICENSE)
