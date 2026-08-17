# Story Settings Template

> Fill in the fields below, save, and start. One sentence per item is enough; the AI auto-loads and strictly follows them.
> Copy this file as your story settings (e.g. `my_story.md`) and replace the placeholders.

## Language

- Output language: en (English) / zh (Chinese) / ja (Japanese). Default: en

## Premise & Worldbuilding

- One-line premise:

## Protagonist

- Identity:
- Personality:
- Goal:

## Key Characters

- Character 1: name / personality / relationship to protagonist
- Character 2: name / personality / relationship to protagonist
- Character 3: name / personality / relationship to protagonist

## Core Rules

- Rule 1:
- Rule 2:
- Rule 3:

## Lorebook Entries (trigger keyword → setting content)

- Keyword 1: corresponding setting content
- Keyword 2: corresponding setting content

## Initial State

> **This section is the ONLY one the initial-state parser reads.** It must be headed `## Initial State` (English), `## 初始状态` (Chinese), or `## 初期状態` (Japanese). The parser does NOT scan other sections (e.g. `## Key Characters`) for stats/inventory/flags.
> Format: one entry per line, `Key: value`. Use `，`/`、` or `,` as separators. Empty values (`无` / `なし` / `none`) are skipped.

- Affinity: Character1=10, Character2=20
- Inventory: item one, item two
- Special flags: met_character=true, clue_found=true

Examples in each language:

```markdown
## Initial State
Affinity: Erin=10, Old Hawke=20
Inventory: old pocket watch, case files
Special flags: met_erin=true
```

```markdown
## 初始状态
好感度：林晚=20，老陈=30
背包：旧怀表、案件卷宗
特殊：已见过林晚=true
```

```markdown
## 初期状態
親密度：ミナ=15，ケン=25
所持品：古い懐中時計、事件ファイル
フラグ：会った=true
```
