[![English](https://img.shields.io/badge/lang-English-blue?style=flat-square)](./README.md)
[![Español](https://img.shields.io/badge/lang-Español-red?style=flat-square)](./README_ES.md)

> **Note:** This repository contains FMWarriors' Agent Skills for FileMaker Pro development. For information about the Agent Skills standard, see [agentskills.io](https://agentskills.io).

# FMWarriors Skills

Skills are folders of instructions, scripts, and references that AI agents load dynamically to improve performance on specialized tasks. FMWarriors Skills teach agents how to work effectively with **FileMaker Pro** — covering everything from SVG icon creation to XML schema building and validation.

For more information about Agent Skills, check out:
- [What are Agent Skills?](https://agentskills.io/home)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Quickstart guide](https://agentskills.io/skill-creation/quickstart)

## About This Repository

This repository contains skills for FileMaker Pro development workflows. Each skill is self-contained in its own folder with a `SKILL.md` file containing the instructions and metadata that agents use.

Browse these skills to get help with FileMaker-specific tasks, or use them as a reference for building your own FileMaker-related skills.

> **Disclaimer:** These skills are provided for FileMaker Pro development assistance. Always test outputs in your own FileMaker environment before deploying to production. FileMaker® is a registered trademark of Claris International Inc.

## Skill Sets

| Skill | Description | Compatibility |
|-------|-------------|---------------|
| [filemaker-svg-builder](./skills/filemaker-svg-builder) | Build, heal, and validate SVG icons for FileMaker Pro button icons and button bars according to the FileMaker Pro 14 SVG Grammar specification. | FileMaker Pro 14+ |
| [filemaker-saxml-builder](./skills/filemaker-saxml-builder) | Build, validate, heal, and fix FileMaker XML (SAXML/fmxmlsnippet) format files for scripts, fields, layouts, themes, and more. | FileMaker Pro 19+ / Claris FileMaker 21+ |
| [contribute-skill](./skills/contribute-skill) | Guides an FMWarriors org member through contributing a new skill to this repository — cloning, branching, scaffolding, validating, and opening a pull request via gh CLI. No git knowledge required. | Requires git + gh CLI |

## Installing Skills

There is no package format — a skill is just a folder. Download it and place it where your agent looks for skills.

### Download a skill

Each skill folder can be downloaded as a ZIP directly from GitHub:

| Skill | Download |
|-------|----------|
| filemaker-svg-builder | [Download ZIP](https://download-directory.github.io/?url=https://github.com/fmwarriors/skills/tree/main/skills/filemaker-svg-builder) |
| filemaker-saxml-builder | [Download ZIP](https://download-directory.github.io/?url=https://github.com/fmwarriors/skills/tree/main/skills/filemaker-saxml-builder) |
| contribute-skill | [Download ZIP](https://download-directory.github.io/?url=https://github.com/fmwarriors/skills/tree/main/skills/contribute-skill) |

Unzip the downloaded file — you get a folder named after the skill containing a `SKILL.md` file.

### Where to put it

| Agent | Path | Notes |
|-------|------|-------|
| **Claude Code** | `~/.claude/skills/<skill-name>/` | Personal — available in all your projects. No restart needed. |
| **Claude Code** (project) | `.claude/skills/<skill-name>/` | Project-only — commit to version control to share with your team. |
| **VS Code / Copilot** | `.agents/skills/<skill-name>/` | Inside your project root. Open Copilot Chat in Agent mode and type `/skills` to confirm. |
| **Cursor** | `.cursor/skills/<skill-name>/` | Inside your project root. |
| **Any other agent** | `~/.agents/skills/<skill-name>/` | Cross-client standard path supported by most spec-compatible agents. |

### Claude Code — one-command install

Claude Code also supports installing directly from this repository via its plugin system:

```
/plugin marketplace add fmwarriors/skills
```

```
/plugin install filemaker-skills@fmwarriors-skills
```

### Once installed

Just tell your agent what you need. Skills activate automatically from the description — no slash command required. For example:

> *"Build an SVG icon for a FileMaker button"* → activates `filemaker-svg-builder`
> *"Validate this fmxmlsnippet"* → activates `filemaker-saxml-builder`
> *"I want to contribute a skill to FMWarriors"* → activates `contribute-skill`

You can also invoke any skill directly by typing `/skill-name` (in agents that support slash commands).

See the [Client Showcase](https://agentskills.io/clients) for setup instructions for all compatible agents.

## Creating a New FileMaker Skill

Skills are simple to create — just a folder with a `SKILL.md` file containing YAML frontmatter and instructions. Use the **template** in this repository as a starting point:

```bash
cp -r template skills/my-new-filemaker-skill
```

Then edit `skills/my-new-filemaker-skill/SKILL.md`:

```markdown
---
name: my-new-filemaker-skill
description: A clear description of what this skill does and when to use it.
license: MIT
metadata:
  author: Your Name
  version: "1.0"
---

# My FileMaker Skill

[Instructions here]
```

The frontmatter requires only two fields:
- `name` — must match the folder name, lowercase with hyphens
- `description` — what the skill does and when to activate it (max 1024 chars)

See the [full specification](./spec/agent-skills-spec.md) or [agentskills.io/specification](https://agentskills.io/specification) for all available fields.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](.github/CONTRIBUTING.md) · [Español](.github/CONTRIBUTING_ES.md) for guidelines on adding new skills or improving existing ones.

## License

Skills in this repository are licensed under the [MIT License](./skills/filemaker-svg-builder/LICENSE.txt) unless otherwise noted in the individual skill's `LICENSE.txt` file.

---

**Author:** Francesc Sans &lt;fsans@ntwk.es&gt; — [FMWarriors](https://github.com/FMWarriors), Barcelona 2025
