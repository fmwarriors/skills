# Contributing to FMWarriors Skills

Thank you for your interest in contributing FileMaker Pro skills! This guide explains how to add a new skill or improve an existing one.

## What Makes a Good FileMaker Skill

A skill should be:
- **Focused** — one clear task or domain (e.g. "build SVG icons", not "do everything FileMaker")
- **Repeatable** — agents should be able to follow the instructions consistently
- **Tested** — try the skill with at least two different agents before submitting

## Adding a New Skill

### 1. Copy the template

```bash
cp -r template skills/your-skill-name
```

The folder name must match the `name` field in `SKILL.md` exactly (lowercase, hyphens only).

### 2. Write your SKILL.md

```markdown
---
name: your-skill-name
description: What this skill does and exactly when an agent should activate it. Include trigger keywords. Max 1024 characters.
license: MIT
metadata:
  author: Your Name
  version: "1.0"
---

# Your Skill Name

## Overview
...

## Instructions
...
```

**Required frontmatter fields:**
- `name` — matches folder name, `[a-z0-9-]`, max 64 chars
- `description` — triggers the skill; include relevant FileMaker keywords

**Optional frontmatter fields:**
- `license` — `MIT` or `Complete terms in LICENSE.txt`
- `metadata.author`, `metadata.version`
- `compatibility` — e.g. `FileMaker Pro 19+ / Claris FileMaker 21+`

### 3. Add supplementary files (optional)

- `references/` — detailed technical docs loaded on-demand
- `scripts/` — executable scripts (Python, Bash, etc.)
- `assets/` — templates, examples, data files
- `LICENSE.txt` — if your skill has a specific license

### 4. Register in the marketplace manifest

Add your skill to `.claude-plugin/marketplace.json` under the appropriate plugin `skills` array:

```json
"./skills/your-skill-name"
```

### 5. Update the README

Add a row to the skills table in `README.md`.

### 6. Submit a pull request

- Keep the PR focused on one skill
- Include a brief description of what the skill does and how you tested it
- Ensure `SKILL.md` passes the [spec validation](https://agentskills.io/specification)

## Improving an Existing Skill

- Fix typos, clarify instructions, or add missing edge cases — all welcome
- Bump `metadata.version` in the frontmatter
- Note the change in the PR description

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Open a GitHub Discussion or file an issue.
