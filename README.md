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

## Try in Your Agent

### Claude Code

You can register this repository as a Claude Code Plugin marketplace by running:

```
/plugin marketplace add fmwarriors/skills
```

Then install the FileMaker skills plugin:

```
/plugin install filemaker-skills@fmwarriors-skills
```

Alternatively, clone this repository and point Claude Code to the `skills/` directory in your project settings.

### VS Code (GitHub Copilot)

VS Code looks for skills in `.agents/skills/` by default. Copy any skill folder into `.agents/skills/` in your project:

```bash
cp -r skills/filemaker-svg-builder /your-project/.agents/skills/
```

Then open Copilot Chat in **Agent** mode and type `/skills` to confirm it appears.

### Cursor

In Cursor, open Settings → Features → Agent Skills and add the path to the `skills/` directory from this repo, or copy individual skill folders into your project's `.cursor/skills/` directory.

### Other Agents

Any agent that supports the [Agent Skills specification](https://agentskills.io/specification) can use these skills. Place the skill folder where your agent looks for skills, or configure the agent's skills directory to point to `skills/` from this repo.

See the [Client Showcase](https://agentskills.io/clients) for the full list of compatible agents and their configuration instructions.

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
