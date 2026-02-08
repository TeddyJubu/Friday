# Friday Workspace (`/home/ubuntu/clawd`)

Personal OpenClaw workspace for **Friday** (AI assistant) used by **Teddy**.

This repository stores assistant identity, operating rules, memory files, custom skills, scripts, and support assets so behavior can persist across sessions and be versioned in GitHub.

---

## What this repo is

This is **not** a typical app codebase. It is an **assistant operating workspace** that contains:

- Core behavior and safety documents (`AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`)
- Short-term and long-term memory artifacts (`memory/`, `MEMORY.md`)
- Custom and imported skills (`skills/`)
- Utility scripts (`scripts/`)
- Supporting assets (`avatars/`, `canvas/`, `agents/`)
- Planning artifacts (`task_plan.md`, `findings.md`, `progress.md`)

The primary goal is continuity + reliability for day-to-day assistant operation.

---

## Repository structure

```text
.
├── AGENTS.md              # Workspace operating rules and policies
├── SOUL.md                # Assistant personality/tone definition
├── USER.md                # Owner-specific preferences/context
├── MEMORY.md              # Curated long-term memory
├── HEARTBEAT.md           # Optional heartbeat task checklist
├── TOOLS.md               # Local environment/tool notes
├── IDENTITY.md            # Name/persona metadata
│
├── memory/                # Daily logs and lightweight state
├── skills/                # Assistant skills (guides/scripts/references)
├── scripts/               # Utility scripts for local operations
├── agents/                # Additional agent persona/config folders
├── avatars/               # Persona image assets
├── canvas/                # Canvas-related artifacts
├── backups/               # Local backup archives (large/sensitive: review before sharing)
├── dist/                  # Generated/build artifacts
├── keys/                  # Key material/config (never expose publicly)
│
├── package.json
├── package-lock.json
├── task_plan.md
├── findings.md
├── progress.md
└── README.md
```

---

## Core operating docs (read order)

For main-session operation, the expected context-loading order is:

1. `SOUL.md` — identity + vibe
2. `USER.md` — who to help and how
3. `memory/YYYY-MM-DD.md` (today + yesterday) — recent context
4. `MEMORY.md` (main session only) — curated long-term memory

`AGENTS.md` defines behavioral norms, safety expectations, and operational habits.

---

## Skills system

The `skills/` directory contains modular instructions and tooling for repeatable tasks.

A typical skill may include:

- `SKILL.md` (entry instructions)
- `scripts/` (automation helpers)
- `references/` (support docs/checklists)

Examples in this repo include strategy, research, content, automation, platform integrations, and workflow utilities.

> Note: `skills/last30days` is currently tracked as an embedded Git repository (submodule-style entry). If you want a fully in-repo copy instead, convert it from submodule to regular directory tracking.

---

## Local setup

### Requirements

- Linux/macOS shell
- Git
- Node.js + npm (repo has `package.json`)
- OpenClaw runtime/environment (for full assistant operation)

### Install JS dependencies

```bash
npm install
```

Current package manifest is minimal and mainly supports workspace utilities.

---

## Daily workflow (human/operator)

### Check repo state

```bash
git status
```

### Commit and push

```bash
git add -A
git commit -m "chore: update workspace"
git push origin master
```

> Remote currently: `https://github.com/TeddyJubu/Friday.git`

---

## Safety and privacy guidance

This repository may contain highly sensitive assistant context.

### Treat as sensitive by default

- `MEMORY.md` can include personal preferences/context
- `memory/` can include day-by-day operational notes
- `keys/` may contain secrets or secret-adjacent data
- `backups/` may include snapshots with private files

### Recommended hygiene

- Keep `.gitignore` strict and current
- Never commit tokens/passwords/private keys
- Audit diffs before pushing
- Avoid publishing raw memory/keys/backups in public contexts

---

## Backups and large files

`backups/` includes tar archives and may grow quickly.

Recommendations:

- Keep backups out of normal feature commits where possible
- Use retention rules (e.g., keep latest N)
- Consider Git LFS or external backup storage for large binaries

---

## Troubleshooting

### `gh` (GitHub CLI) issues

Check auth:

```bash
gh auth status
```

Re-auth if needed:

```bash
gh auth login
```

### Embedded repository warning

If you see warnings like “adding embedded git repository”, you staged a nested repo. Decide whether it should be:

- a real submodule (`git submodule add ...`), or
- flattened to regular files (remove nested `.git`, then re-add files)

---

## Maintenance checklist

- [ ] Review and prune stale memory entries
- [ ] Rotate/archive old daily notes if needed
- [ ] Audit `keys/` and secrets handling
- [ ] Keep skill docs and scripts synchronized
- [ ] Validate `.gitignore` against new file types
- [ ] Remove accidental binary/noise commits

---

## Intent

This workspace is the persistent brain + playbook for Friday.

If you change core behavior files (`AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, major skills), commit and push so those improvements persist across sessions and environments.
