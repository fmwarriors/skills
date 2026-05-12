# Agent Skills Specification

The specification is maintained at [agentskills.io/specification](https://agentskills.io/specification).

Fetch the complete documentation index at: https://agentskills.io/llms.txt

## Quick Reference

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: supplementary documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files
```

### SKILL.md Frontmatter Fields

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Max 64 chars. Lowercase letters, numbers, hyphens only. Must match directory name. |
| `description` | Yes | Max 1024 chars. Describes what the skill does and when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars. Environment requirements. |
| `metadata` | No | Arbitrary key-value pairs for additional metadata. |
| `allowed-tools` | No | Space-separated string of pre-approved tools (experimental). |

### Minimal Example

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---

# Skill instructions go here
```
