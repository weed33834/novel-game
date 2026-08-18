#!/usr/bin/env python3
"""NovelGame state management CLI.

All story state (current node, affinity, inventory, flags, branch history) is
read/written through this script as JSON saves, guaranteeing deterministic
state that does not depend on AI conversation memory.

Save directory priority: --dir argument > $NOVEL_DATA_DIR > ./saves
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path


def default_dir() -> Path:
    return Path(os.environ.get("NOVEL_DATA_DIR", "saves"))


def resolve_dir(d: str | None) -> Path:
    return Path(d) if d else default_dir()


def story_path(data_dir: Path, story_id: str) -> Path:
    return data_dir / f"{story_id}.json"


def load(data_dir: Path, story_id: str) -> dict:
    p = story_path(data_dir, story_id)
    if not p.exists():
        sys.exit(f"Save not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def save(data_dir: Path, state: dict) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    p = story_path(data_dir, state["story_id"])
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {p}")


def latest(data_dir: Path) -> str:
    if not data_dir.exists():
        sys.exit("Save directory does not exist")
    files = sorted(data_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        sys.exit("No saves found")
    return files[0].stem


def cmd_init(args: argparse.Namespace) -> None:
    data_dir = resolve_dir(args.dir)
    story_id = args.story or uuid.uuid4().hex[:8]
    state = {
        "story_id": story_id,
        "title": args.title or "Untitled Story",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "current_node": "start",
        "flags": {},
        "stats": {},
        "inventory": [],
        "history": [],
        "branch_log": [],
        "memory": {
            "short": [],  # short-term memory: recent events/dialogue, capped at 20 entries
            "mid": [],    # mid-term memory: chapter summaries
            "long": [],   # long-term memory: core settings/key events/player-preference reflections
        },
        "snapshots": [],  # chapter snapshots: recovery points after context loss
    }
    if args.settings:
        sp = Path(args.settings)
        if not sp.exists():
            sys.exit(f"Settings file not found: {sp}")
        state["settings"] = sp.read_text(encoding="utf-8")
    save(data_dir, state)
    print(f"Story created: {story_id} ({state['title']})")


def cmd_get(args: argparse.Namespace) -> None:
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    print(json.dumps(state, ensure_ascii=False, indent=2))


def cmd_summary(args: argparse.Namespace) -> None:
    """Output a compact state block to inject into context before each turn, preventing state loss."""
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    parts = [f"node:{state['current_node']}"]
    if state["stats"]:
        parts.append("affinity:" + ", ".join(f"{k}={v}" for k, v in state["stats"].items()))
    if state["inventory"]:
        parts.append("inventory:" + ", ".join(state["inventory"]))
    if state["flags"]:
        parts.append("flags:" + ", ".join(f"{k}={v}" for k, v in state["flags"].items()))
    if state["history"]:
        parts.append("last_event:" + state["history"][-1]["event"])
    mem = state.get("memory", {})
    if mem.get("short"):
        parts.append("short_mem:" + " | ".join(mem["short"][-3:]))
    if mem.get("mid"):
        parts.append("chapter_summary:" + " | ".join(mem["mid"][-2:]))
    if mem.get("long"):
        parts.append("long_mem:" + " | ".join(mem["long"][-2:]))
    print("[STATE] " + " | ".join(parts))


def mutate(args: argparse.Namespace, fn) -> None:
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    fn(state, args)
    save(data_dir, state)


def cmd_set(args: argparse.Namespace) -> None:
    def fn(state: dict, args: argparse.Namespace) -> None:
        state["flags"][args.key] = args.value
    mutate(args, fn)


def cmd_add_stat(args: argparse.Namespace) -> None:
    def fn(state: dict, args: argparse.Namespace) -> None:
        state["stats"][args.key] = state["stats"].get(args.key, 0) + args.delta
    mutate(args, fn)


def cmd_add_item(args: argparse.Namespace) -> None:
    def fn(state: dict, args: argparse.Namespace) -> None:
        if args.item not in state["inventory"]:
            state["inventory"].append(args.item)
    mutate(args, fn)


def cmd_remove_item(args: argparse.Namespace) -> None:
    def fn(state: dict, args: argparse.Namespace) -> None:
        if args.item in state["inventory"]:
            state["inventory"].remove(args.item)
    mutate(args, fn)


def cmd_set_node(args: argparse.Namespace) -> None:
    def fn(state: dict, args: argparse.Namespace) -> None:
        state["current_node"] = args.node
    mutate(args, fn)


def cmd_log(args: argparse.Namespace) -> None:
    def fn(state: dict, args: argparse.Namespace) -> None:
        state["history"].append({
            "node": state["current_node"],
            "event": args.event,
            "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })
        # Mirror the event into short-term memory, capped at 20 entries
        mem = state.setdefault("memory", {"short": [], "mid": [], "long": []})
        mem["short"].append(args.event)
        del mem["short"][:-20]
    mutate(args, fn)


def cmd_remember(args: argparse.Namespace) -> None:
    """Write to a specific memory tier: short / mid (chapter summary) / long."""
    def fn(state: dict, args: argparse.Namespace) -> None:
        mem = state.setdefault("memory", {"short": [], "mid": [], "long": []})
        tier = mem.setdefault(args.tier, [])
        tier.append(args.content)
        if args.tier == "short":
            del tier[:-20]
    mutate(args, fn)


def cmd_recall(args: argparse.Namespace) -> None:
    """Read a memory tier, with optional --keyword lightweight filtering (instead of vector search)."""
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    mem = state.get("memory", {})
    tier = mem.get(args.tier, [])
    if args.keyword:
        kw = args.keyword.lower()
        tier = [m for m in tier if kw in m.lower()]
    if args.limit:
        tier = tier[-args.limit:]
    if not tier:
        print(f"[{args.tier}] no memory")
        return
    for m in tier:
        print(f"- {m}")


def cmd_reflect(args: argparse.Namespace) -> None:
    """Write long-term memory (reflection: player preferences / recurring patterns)."""
    def fn(state: dict, args: argparse.Namespace) -> None:
        mem = state.setdefault("memory", {"short": [], "mid": [], "long": []})
        mem["long"].append(args.content)
    mutate(args, fn)


def cmd_snapshot(args: argparse.Namespace) -> None:
    """Write a chapter snapshot: recovery point after context loss. Call once at the end of each chapter."""
    def fn(state: dict, args: argparse.Namespace) -> None:
        snapshots = state.setdefault("snapshots", [])
        snapshots.append({
            "chapter": len(snapshots) + 1,
            "scene": args.scene,
            "characters": args.characters,
            "open_threads": args.threads,
            "goal": args.goal,
            "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })
    mutate(args, fn)


def cmd_restore(args: argparse.Namespace) -> None:
    """Read the latest chapter snapshot and output recovery guidance (for new sessions / context loss)."""
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    snapshots = state.get("snapshots", [])
    if not snapshots:
        print("[RESTORE] No chapter snapshot. Read the current state with `summary` and continue.")
        return
    s = snapshots[-1]
    print(f"[RESTORE] Chapter {s['chapter']} snapshot")
    print(f"Scene: {s['scene']}")
    print(f"Characters present: {s['characters']}")
    print(f"Open threads: {s['open_threads']}")
    print(f"Current goal: {s['goal']}")
    print("Resume the story from this snapshot + the `summary` state, and continue with 2-4 choices.")


def cmd_context(args: argparse.Namespace) -> None:
    """Dynamic context injection: assemble a full context block from current state, for recovery after context changes.

    More complete than `summary`: includes current node, key state, recent events,
    chapter snapshot, and player preferences.
    """
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    lines = [f"node:{state['current_node']}"]
    if state["stats"]:
        lines.append("affinity:" + ", ".join(f"{k}={v}" for k, v in state["stats"].items()))
    if state["inventory"]:
        lines.append("inventory:" + ", ".join(state["inventory"]))
    if state["flags"]:
        lines.append("flags:" + ", ".join(f"{k}={v}" for k, v in state["flags"].items()))
    mem = state.get("memory", {})
    if mem.get("short"):
        lines.append("recent_events:" + " | ".join(mem["short"][-3:]))
    if mem.get("long"):
        lines.append("player_prefs:" + " | ".join(mem["long"][-1:]))
    snapshots = state.get("snapshots", [])
    if snapshots:
        s = snapshots[-1]
        lines.append(f"current_scene:{s['scene']}")
        lines.append(f"characters_present:{s['characters']}")
        lines.append(f"open_threads:{s['open_threads']}")
        lines.append(f"current_goal:{s['goal']}")
    print("[CONTEXT] " + " | ".join(lines))


def cmd_list(args: argparse.Namespace) -> None:
    data_dir = resolve_dir(args.dir)
    if not data_dir.exists():
        print("Save directory does not exist")
        return
    for p in sorted(data_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        s = json.loads(p.read_text(encoding="utf-8"))
        print(f"{s['story_id']}  {s['title']}  node:{s['current_node']}  updated:{s['updated_at']}")


# ---------------------------------------------------------------------------
# Gameplay systems: dice, quests, combat, endings, encounters
# ---------------------------------------------------------------------------

def cmd_roll(args: argparse.Namespace) -> None:
    """Roll a die (d20/d100/etc.) with an optional modifier and DC.

    The engine uses this to decide action outcomes instead of free-form
    judgment, so success/failure is deterministic and fair.
    """
    import random
    total = random.randint(1, args.dice) + args.mod
    out = f"[ROLL] d{args.dice}{'+' if args.mod >= 0 else ''}{args.mod} = {total}"
    if args.dc is not None:
        out += f" (DC {args.dc}) -> {'SUCCESS' if total >= args.dc else 'FAILURE'}"
    print(out)


def cmd_quest(args: argparse.Namespace) -> None:
    """Mutate a quest: add / update / complete / fail."""
    def fn(state: dict, args: argparse.Namespace) -> None:
        quests = state.setdefault("quests", {})
        if args.action == "add":
            quests[args.id] = {
                "title": args.title,
                "desc": args.desc or "",
                "status": "active",
                "progress": "",
                "added_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            return
        q = quests.get(args.id)
        if not q:
            sys.exit(f"Quest not found: {args.id}")
        if args.action == "update":
            q["progress"] = args.progress
        elif args.action == "complete":
            q["status"] = "completed"
        elif args.action == "fail":
            q["status"] = "failed"
    mutate(args, fn)


def cmd_quest_list(args: argparse.Namespace) -> None:
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    quests = state.get("quests", {})
    if not quests:
        print("[QUESTS] none")
        return
    for qid, q in quests.items():
        print(f"- [{q['status']}] {qid}: {q['title']} {q['progress']}")


def cmd_combat(args: argparse.Namespace) -> None:
    """Mutate combat: start / attack / end."""
    def fn(state: dict, args: argparse.Namespace) -> None:
        if args.action == "start":
            state["combat"] = {
                "enemy": args.enemy,
                "hp": args.hp,
                "max_hp": args.hp,
                "atk": args.atk,
                "active": True,
            }
            return
        c = state.get("combat")
        if not c:
            sys.exit("No combat in progress")
        if args.action == "attack":
            c["hp"] = max(0, c["hp"] - args.damage)
            if c["hp"] == 0:
                c["active"] = False
                c["result"] = "win"
        elif args.action == "end":
            c["active"] = False
            c["result"] = args.result
    mutate(args, fn)


def cmd_combat_status(args: argparse.Namespace) -> None:
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    c = state.get("combat")
    if not c or not c.get("active"):
        print("[COMBAT] none")
        return
    print(f"[COMBAT] {c['enemy']} HP {c['hp']}/{c['max_hp']} ATK {c['atk']}")


def cmd_ending(args: argparse.Namespace) -> None:
    """Record a reached ending (endings are judged by the engine from settings + state)."""
    def fn(state: dict, args: argparse.Namespace) -> None:
        endings = state.setdefault("endings", [])
        if not any(e["id"] == args.id for e in endings):
            endings.append({
                "id": args.id,
                "title": args.title,
                "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            })
    mutate(args, fn)


def cmd_ending_list(args: argparse.Namespace) -> None:
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    endings = state.get("endings", [])
    if not endings:
        print("[ENDINGS] none reached yet")
        return
    for e in endings:
        print(f"- {e['id']}: {e['title']} ({e['at']})")


def cmd_encounter(args: argparse.Namespace) -> None:
    """Pick an encounter from a pool (JSON list of {id, weight}), avoiding recently used ones.

    The engine passes the blueprint's Encounter Pool here to schedule events
    with direction instead of drifting or repeating.
    """
    import random
    data_dir = resolve_dir(args.dir)
    story_id = args.story or latest(data_dir)
    state = load(data_dir, story_id)
    pool = json.loads(args.pool)
    hist = state.setdefault("encounter_history", [])
    recent = set(hist[-max(1, args.avoid):])
    candidates = [e for e in pool if e["id"] not in recent] or pool
    weights = [e.get("weight", 1) for e in candidates]
    pick = random.choices(candidates, weights=weights, k=1)[0]
    hist.append(pick["id"])
    del hist[:-20]
    save(data_dir, state)
    print(f"[ENCOUNTER] {pick['id']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="NovelGame state management")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create a new save")
    p.add_argument("--title", default="")
    p.add_argument("--story", default="")
    p.add_argument("--settings", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("get", help="read full state")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("summary", help="compact state summary (for context injection)")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_summary)

    p = sub.add_parser("set", help="set a flag")
    p.add_argument("--key", required=True)
    p.add_argument("--value", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("add-stat", help="adjust a numeric stat (affinity, etc.)")
    p.add_argument("--key", required=True)
    p.add_argument("--delta", type=int, required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_add_stat)

    p = sub.add_parser("add-item", help="add an item to inventory")
    p.add_argument("--item", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_add_item)

    p = sub.add_parser("remove-item", help="remove an item from inventory")
    p.add_argument("--item", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_remove_item)

    p = sub.add_parser("set-node", help="set the current node")
    p.add_argument("--node", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_set_node)

    p = sub.add_parser("log", help="record an event")
    p.add_argument("--event", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("remember", help="write tiered memory (short/mid/long)")
    p.add_argument("--tier", required=True, choices=["short", "mid", "long"])
    p.add_argument("--content", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_remember)

    p = sub.add_parser("recall", help="read tiered memory (with keyword filter)")
    p.add_argument("--tier", required=True, choices=["short", "mid", "long"])
    p.add_argument("--keyword", default="")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_recall)

    p = sub.add_parser("reflect", help="write long-term memory (reflection)")
    p.add_argument("--content", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_reflect)

    p = sub.add_parser("snapshot", help="write a chapter snapshot (recovery point after context loss)")
    p.add_argument("--scene", required=True)
    p.add_argument("--characters", default="")
    p.add_argument("--threads", default="")
    p.add_argument("--goal", default="")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_snapshot)

    p = sub.add_parser("restore", help="read the latest chapter snapshot (recover after new session / context loss)")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_restore)

    p = sub.add_parser("context", help="dynamic context injection (full context block, for recovery after context changes)")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_context)

    p = sub.add_parser("list", help="list saves")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("roll", help="roll a die with optional modifier and DC")
    p.add_argument("--dice", type=int, default=20)
    p.add_argument("--mod", type=int, default=0)
    p.add_argument("--dc", type=int, default=None)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_roll)

    p = sub.add_parser("quest", help="mutate a quest: add / update / complete / fail")
    p.add_argument("--action", required=True, choices=["add", "update", "complete", "fail"])
    p.add_argument("--id", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--desc", default="")
    p.add_argument("--progress", default="")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_quest)

    p = sub.add_parser("quest-list", help="list active/completed/failed quests")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_quest_list)

    p = sub.add_parser("combat", help="mutate combat: start / attack / end")
    p.add_argument("--action", required=True, choices=["start", "attack", "end"])
    p.add_argument("--enemy", default="")
    p.add_argument("--hp", type=int, default=0)
    p.add_argument("--atk", type=int, default=0)
    p.add_argument("--damage", type=int, default=0)
    p.add_argument("--result", default="")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_combat)

    p = sub.add_parser("combat-status", help="show current combat state")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_combat_status)

    p = sub.add_parser("ending", help="record a reached ending")
    p.add_argument("--id", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_ending)

    p = sub.add_parser("ending-list", help="list reached endings")
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_ending_list)

    p = sub.add_parser("encounter", help="pick a weighted encounter from a JSON pool, avoiding recent repeats")
    p.add_argument("--pool", required=True)
    p.add_argument("--avoid", type=int, default=3)
    p.add_argument("--story", default="")
    p.add_argument("--dir", default="")
    p.set_defaults(func=cmd_encounter)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
