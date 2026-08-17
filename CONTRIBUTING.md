# Contributing to NovelGame

Thanks for your interest in contributing. This project is released under the [Apache License 2.0](LICENSE); by submitting a contribution you agree to the terms of the license.

## How to Contribute

1. **Open an issue first** for non-trivial changes, so we can align on scope before you write code.
2. **Fork** the repository and create a feature branch: `git checkout -b feat/your-feature`.
3. Make your changes, following the guidelines below.
4. **Test** your changes (see "Testing").
5. Submit a pull request with a clear description of what and why.

## Guidelines

- **English-first**: engine rules, commands, comments, and docs are in English. Narrative output may be multilingual, but the engine itself stays English.
- **No third-party dependencies**: the scripts use only the Python standard library. Keep it that way.
- **State determinism**: any new state must be persisted through `state.py` as JSON; never rely on conversation memory.
- **Backward compatibility**: don't break existing save files or command signatures without a major version bump and a migration note in `CHANGELOG.md`.
- **Code style**: Python 3.10+, type hints, no dead code, no unnecessary defensive programming.

## Testing

Run the smoke test to verify the full state lifecycle:

```bash
python3 -m py_compile skills/novel-game/scripts/state.py skills/novel-game/scripts/new_story.py
python3 skills/novel-game/scripts/new_story.py --settings skills/novel-game/references/EXAMPLE.md --title "Test" --dir /tmp/novelgame-test
python3 skills/novel-game/scripts/state.py summary --dir /tmp/novelgame-test
python3 skills/novel-game/scripts/state.py add-stat --key Erin --delta 5 --dir /tmp/novelgame-test
python3 skills/novel-game/scripts/state.py snapshot --scene "test" --characters "Erin" --goal "test" --threads "none" --dir /tmp/novelgame-test
python3 skills/novel-game/scripts/state.py restore --dir /tmp/novelgame-test
```

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(engine): add ...`
- `fix(state): correct ...`
- `docs(readme): update ...`
- `refactor(scripts): ...`

## Reporting Bugs

Include: the command you ran, the expected output, the actual output, and your Python version.
