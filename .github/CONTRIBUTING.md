# Contributing to FMWarriors Skills

Thank you for your interest in contributing FileMaker Pro skills!
This guide walks you through the full process — from forking the repo to getting your PR merged.

---

## The Full Workflow at a Glance

```
Fork → Clone → Branch → Add skill → Test → Push → Pull Request → Review → Merge
```

---

## Step-by-step: Adding a New Skill

### 1. Fork the repository

Click **Fork** on https://github.com/fmwarriors/skills — this creates your own copy under your GitHub account.

### 2. Clone your fork

```bash
git clone https://github.com/YOUR_USERNAME/skills.git
cd skills
```

### 3. Create a feature branch

Always work on a branch, never directly on `main`:

```bash
git checkout -b add/my-new-skill
```

Use a descriptive name like `add/filemaker-theme-builder` or `fix/svg-builder-typos`.

### 4. Copy the template

```bash
cp -r template skills/your-skill-name
```

> The folder name must be **lowercase with hyphens only** and must match the `name` field
> in `SKILL.md` exactly. Example: folder `filemaker-theme-builder` → `name: filemaker-theme-builder`

### 5. Write your SKILL.md

Edit `skills/your-skill-name/SKILL.md`:

```markdown
---
name: your-skill-name
description: What this skill does and exactly when an agent should activate it.
             Include specific FileMaker keywords that trigger the skill. Max 1024 characters.
license: MIT
compatibility: FileMaker Pro 19+ / Claris FileMaker 21+
metadata:
  author: Your Name or GitHub handle
  version: "1.0"
---

# Your Skill Title

## Overview
Brief summary of what the skill does.

## Instructions
Step-by-step instructions for the agent to follow...
```

**Required frontmatter fields:**
- `name` — must match the folder name exactly, `[a-z0-9-]` only, max 64 chars
- `description` — the agent uses this to decide whether to activate the skill; include relevant FileMaker keywords

**Optional but recommended:**
- `license` — `MIT` or `Complete terms in LICENSE.txt`
- `compatibility` — FileMaker version requirements
- `metadata.author`, `metadata.version`

### 6. Add supplementary files (optional but encouraged)

```
skills/your-skill-name/
├── SKILL.md          ← Required
├── LICENSE.txt       ← Recommended (copy from an existing skill and update the copyright line)
├── references/       ← Detailed docs the agent loads on demand (keeps SKILL.md lean)
│   └── REFERENCE.md
├── scripts/          ← Executable Python/Bash scripts
├── assets/           ← Templates, SVGs, data files
└── examples/         ← Sample inputs/outputs showing the skill in action
```

### 7. Add a per-skill LICENSE.txt

Copy an existing `LICENSE.txt` and update the copyright line:

```bash
cp skills/filemaker-svg-builder/LICENSE.txt skills/your-skill-name/LICENSE.txt
# Then edit the copyright line with your name and year
```

### 8. Register in the marketplace manifest

Open `.claude-plugin/marketplace.json` and add your skill path to the `skills` array
inside the `filemaker-skills` plugin:

```json
"skills": [
  "./skills/filemaker-svg-builder",
  "./skills/filemaker-saxml-builder",
  "./skills/your-skill-name"   ← add this line
]
```

### 9. Update the root README

Add a row to the skills table in `README.md`:

```markdown
| [your-skill-name](./skills/your-skill-name) | One-line description | FileMaker Pro XX+ |
```

### 10. Test your skill

Before submitting, test with at least one compatible agent:

- Load the skill in Claude Code, VS Code Copilot, Cursor, or another supported agent
- Confirm it activates on the right prompts (check your `description` keywords)
- Confirm the agent follows the instructions correctly

### 11. Commit and push

```bash
git add .
git commit -m "Add filemaker-your-skill-name skill"
git push origin add/your-skill-name
```

### 12. Open a Pull Request

Go to https://github.com/fmwarriors/skills and click **"Compare & pull request"**.

In your PR description include:
- What the skill does
- How you tested it (which agent, what prompts)
- Any FileMaker version requirements

Keep each PR focused on **one skill** — it makes review much faster.

---

## Improving an Existing Skill

Same flow: fork → branch → edit → push → PR.

- Fix typos or clarify instructions — always welcome
- Add missing edge cases, examples, or reference files
- Bump `metadata.version` in the frontmatter when you make meaningful changes
- Describe what changed and why in the PR

---

## Skill Quality Checklist

Before submitting, verify:

- [ ] Folder name matches `name` in `SKILL.md` frontmatter (lowercase, hyphens only)
- [ ] `description` is ≤ 1024 characters and includes relevant trigger keywords
- [ ] All required child elements present in any XML examples
- [ ] `LICENSE.txt` is present with correct copyright line
- [ ] Added to `.claude-plugin/marketplace.json`
- [ ] Added to the skills table in `README.md`
- [ ] Tested with at least one agent

---

## Questions?

Open a [GitHub Discussion](https://github.com/fmwarriors/skills/discussions) or file an [Issue](https://github.com/fmwarriors/skills/issues).
