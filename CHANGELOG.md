# Changelog

All notable changes to NovelGame are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
