---
name: contribute-skill
description: Guide an FMWarriors org member through contributing a new Agent Skill to the fmwarriors/skills GitHub repository — including cloning the repo, creating a branch, scaffolding or copying the skill folder, validating SKILL.md, registering it in the marketplace manifest, updating the README, committing, and opening a pull request via the gh CLI. Use when a user says they want to add a skill, contribute a skill, submit a skill, publish a skill to FMWarriors, or share a FileMaker skill with the team.
license: Complete terms in LICENSE.txt
compatibility: Requires git and gh CLI installed and authenticated. User must be a member of the fmwarriors GitHub org.
metadata:
  author: FMWarriors — Francesc Sans
  version: "1.0"
  org: FMWarriors
---

# Contribute a Skill to FMWarriors

Guide the user through contributing a new Agent Skill to [fmwarriors/skills](https://github.com/fmwarriors/skills). This covers everything from zero — the user does not need to know git.

---

## Step 0: Understand what the user has

Ask exactly one question before doing anything else:

> "Do you already have a skill folder (with a SKILL.md file), or do you want help building one from scratch?"

- **Has files** → go to [WORKFLOW.md § Copy path](./references/WORKFLOW.md#copy-path)
- **Needs to build** → go to [WORKFLOW.md § Build path](./references/WORKFLOW.md#build-path)

---

## Step 1: Check prerequisites

Run these checks silently and only report problems:

```bash
# git installed?
git --version

# gh installed?
gh --version

# gh authenticated?
gh auth status
```

If `gh auth status` fails, tell the user:
> "You need to authenticate with GitHub first. Run `gh auth login` and follow the prompts — choose HTTPS and authenticate via browser."

If `git` or `gh` is missing, point them to:
- git: https://git-scm.com/downloads
- gh: https://cli.github.com

Do not continue until both tools are installed and `gh` is authenticated.

---

## Step 2: Clone the repository

```bash
git clone https://github.com/fmwarriors/skills.git
cd skills
```

If the folder already exists locally, update it instead:

```bash
cd skills
git checkout main
git pull origin main
```

---

## Step 3: Create a branch

Branch name must follow the pattern `add/<skill-name>`:

```bash
git checkout -b add/<skill-name>
```

Use the exact skill folder name (e.g. `add/filemaker-theme-builder`).

---

## Step 4: Add the skill

See the full instructions for both paths in [references/WORKFLOW.md](./references/WORKFLOW.md).

**Quick summary:**
- Copy or build the skill folder into `skills/<skill-name>/`
- Ensure `SKILL.md` frontmatter is valid (see validation rules below)
- Add `LICENSE.txt` (copy from an existing skill, update the copyright line)

---

## Step 5: Validate SKILL.md

Check these rules before committing — fix any that fail:

| Rule | Check |
|------|-------|
| `name` matches folder name | `name: filemaker-foo` → folder must be `filemaker-foo` |
| `name` is lowercase, hyphens only | no uppercase, no spaces, no underscores |
| `name` ≤ 64 characters | count it |
| `description` is present and non-empty | required |
| `description` ≤ 1024 characters | count it |
| `description` contains FileMaker trigger keywords | helps agents activate the skill correctly |

---

## Step 6: Register and update docs

```bash
# 1. Add skill path to .claude-plugin/marketplace.json skills array
# 2. Add a row to the skills table in README.md
# 3. Add the same row to README_ES.md (Spanish README)
```

See [references/WORKFLOW.md § Register](./references/WORKFLOW.md#register) for exact edit instructions.

---

## Step 7: Commit and push

```bash
git add .
git commit -m "Add <skill-name> skill"
git push origin add/<skill-name>
```

---

## Step 8: Open the pull request

```bash
gh pr create \
  --repo fmwarriors/skills \
  --base main \
  --title "Add <skill-name> skill" \
  --body "$(cat <<'EOF'
## What this skill does
<one paragraph description>

## How I tested it
<which agent, what prompts, what results>

## FileMaker version requirements
<e.g. FileMaker Pro 19+ / Claris FileMaker 21+>
EOF
)"
```

After running, `gh` will print the PR URL. Share it with the user:
> "Your PR is open at: https://github.com/fmwarriors/skills/pull/..."

---

## Done

Tell the user:
> "Your skill has been submitted for review. A maintainer will check it and merge it or leave feedback. You'll get a GitHub notification when there's an update."
