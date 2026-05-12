# Contribute Skill — Full Workflow Reference

Detailed instructions for both contribution paths. Load this file when the SKILL.md overview
is not enough detail for the current step.

---

## Copy path

The user already has a skill folder on their disk. Jump straight to scaffolding.

### Locate the source

Ask the user:
> "What is the full path to your skill folder? For example: `/Users/yourname/Desktop/my-skill`"

If they only have a single `SKILL.md` file (no folder), create the folder:

```bash
mkdir -p skills/<skill-name>
cp /path/to/their/SKILL.md skills/<skill-name>/SKILL.md
```

If they have a full folder:

```bash
cp -rX /path/to/their/skill-folder skills/<skill-name>
```

> Use `-rX` on macOS to avoid copying extended attributes. On Linux use `-r`.

### Infer the skill name

Read the `name:` field from their `SKILL.md`. That value must become the folder name.

```bash
# Extract name from frontmatter
grep '^name:' skills/<skill-name>/SKILL.md
```

If the folder name doesn't match, rename it:

```bash
mv skills/<wrong-name> skills/<correct-name>
```

---

## Build path

The user wants to create a skill from scratch. Interview them first, then write the files.

### Interview questions

Ask these one at a time, not all at once:

1. **"What does the skill do?"** — one sentence, plain language
2. **"When should an agent activate it?"** — what will the user say or ask? (these become trigger keywords)
3. **"What FileMaker version does it require?"** — e.g. FileMaker Pro 19+, Claris 21+
4. **"What should the skill be called?"** — suggest a lowercase-hyphens name if they're unsure (e.g. `filemaker-pdf-export`)
5. **"Do you have any instructions, notes, or reference material I should base it on?"** — paste text, point to a file, or say no

### Draft the SKILL.md

Using the answers, write `skills/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: <what it does>. Use when <trigger conditions>. Triggers on: <keyword1>, <keyword2>, <keyword3>.
license: Complete terms in LICENSE.txt
compatibility: <FileMaker version requirement>
metadata:
  author: <their name or GitHub handle>
  version: "1.0"
  org: FMWarriors
---

# <Skill Title>

## Overview
<one paragraph summary>

## Instructions

<step-by-step instructions>

## Examples

<at least one example of what the user says and what the agent does>

## Reference files

Load [references/REFERENCE.md](./references/REFERENCE.md) for detailed technical content.
```

Show it to the user and ask:
> "Does this look right? Say yes to continue, or tell me what to change."

Iterate until they approve.

### Add a REFERENCE.md if the skill has complex content

If the skill needs detailed technical documentation (more than ~100 lines of instructions),
move the detail to `references/REFERENCE.md` and keep `SKILL.md` to the overview and key steps.

```bash
mkdir -p skills/<skill-name>/references
# write references/REFERENCE.md with the detailed content
```

---

## Both paths: Required scaffolding

After the skill folder exists, always run these steps regardless of which path was used.

### Add LICENSE.txt

```bash
cp skills/filemaker-svg-builder/LICENSE.txt skills/<skill-name>/LICENSE.txt
```

Then edit the copyright line:

```
Copyright (c) 2025 FMWarriors — <Their Name> <their@email.com>
```

Ask the user for their name and email if not known.

### Validate SKILL.md frontmatter

Run these checks manually by reading the file:

```bash
cat skills/<skill-name>/SKILL.md | head -20
```

Checklist:
- [ ] `name:` value matches the folder name exactly
- [ ] `name:` is all lowercase, hyphens only, no spaces, no underscores
- [ ] `name:` is ≤ 64 characters
- [ ] `description:` is present and non-empty
- [ ] `description:` is ≤ 1024 characters — count if unsure:
  ```bash
  python3 -c "
  import re, sys
  txt = open('skills/<skill-name>/SKILL.md').read()
  desc = re.search(r'^description:\s*(.+)', txt, re.MULTILINE)
  print(len(desc.group(1)) if desc else 'NOT FOUND')
  "
  ```
- [ ] `description:` contains FileMaker-specific trigger keywords
- [ ] `license:` field is present
- [ ] `metadata.author` is present

Fix any failures before continuing.

---

## Register

### 1. Add to marketplace manifest

Open `.claude-plugin/marketplace.json`. Find the `skills` array inside the `filemaker-skills` plugin and append the new path:

```json
"skills": [
  "./skills/filemaker-svg-builder",
  "./skills/filemaker-saxml-builder",
  "./skills/<skill-name>"
]
```

### 2. Add to README.md skill table

Open `README.md`. Find the skills table and add a new row:

```markdown
| [<skill-name>](./skills/<skill-name>) | <one-line description> | <FileMaker version> |
```

### 3. Add to README_ES.md skill table

Same row in Spanish in `README_ES.md`:

```markdown
| [<skill-name>](./skills/<skill-name>) | <descripción en una línea> | <versión FileMaker> |
```

If the user doesn't provide a Spanish description, translate the English one directly.

---

## PR body template

Use this as the `--body` content for `gh pr create`.
Fill in the three sections from what the user told you during the interview or copy path:

```markdown
## What this skill does
<one paragraph — what it does, what FileMaker objects/workflows it covers>

## How I tested it
<which agent (Claude Code / Cursor / VS Code Copilot / etc.), what prompts triggered it,
what the agent produced, whether it matched expectations>

## FileMaker version requirements
<e.g. FileMaker Pro 19+ / Claris FileMaker 21+. Or "No specific version required.">

## Checklist
- [x] Folder name matches `name` in SKILL.md
- [x] description ≤ 1024 characters
- [x] LICENSE.txt present
- [x] Added to .claude-plugin/marketplace.json
- [x] Added to README.md skill table
- [x] Added to README_ES.md skill table
- [x] Tested with at least one agent
```

---

## Troubleshooting

### `gh auth status` says "not logged in"
```bash
gh auth login
# Choose: GitHub.com → HTTPS → Login with a web browser
```

### `git push` says "permission denied"
The user may not be added to the `fmwarriors` org yet. Ask them to contact @fsans on GitHub or email fsans@ntwk.es to be added.

### `git push` says "remote: Repository not found"
The clone URL may have been typed wrong. Verify:
```bash
git remote -v
# Should show: origin  https://github.com/fmwarriors/skills.git
```
If wrong:
```bash
git remote set-url origin https://github.com/fmwarriors/skills.git
```

### Branch already exists
```bash
git checkout main
git pull origin main
git branch -d add/<skill-name>   # delete old branch
git checkout -b add/<skill-name>  # recreate fresh
```

### `name` in SKILL.md has uppercase or spaces
The spec rejects these. Convert the name:
- spaces → hyphens
- uppercase → lowercase
- underscores → hyphens
- Example: `FileMaker Theme Builder` → `filemaker-theme-builder`
