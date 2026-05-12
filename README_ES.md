[![English](https://img.shields.io/badge/lang-English-blue?style=flat-square)](./README.md)
[![Español](https://img.shields.io/badge/lang-Español-red?style=flat-square)](./README_ES.md)

> **Nota:** Este repositorio contiene los Agent Skills de FMWarriors para el desarrollo con FileMaker Pro. Para información sobre el estándar Agent Skills, visita [agentskills.io](https://agentskills.io).

# FMWarriors Skills

Los skills son carpetas de instrucciones, scripts y referencias que los agentes de IA cargan dinámicamente para mejorar su rendimiento en tareas especializadas. Los FMWarriors Skills enseñan a los agentes a trabajar eficazmente con **FileMaker Pro** — desde la creación de iconos SVG hasta la construcción y validación de esquemas XML.

Para más información sobre Agent Skills:
- [¿Qué son los Agent Skills?](https://agentskills.io/home)
- [Especificación de Agent Skills](https://agentskills.io/specification)
- [Guía de inicio rápido](https://agentskills.io/skill-creation/quickstart)

## Sobre este repositorio

Este repositorio contiene skills para flujos de trabajo de desarrollo con FileMaker Pro. Cada skill es una carpeta autocontenida con un archivo `SKILL.md` que incluye las instrucciones y metadatos que utilizan los agentes.

Explora estos skills para obtener ayuda con tareas específicas de FileMaker, o úsalos como referencia para construir tus propios skills relacionados con FileMaker.

> **Aviso:** Estos skills se proporcionan como ayuda para el desarrollo con FileMaker Pro. Prueba siempre los resultados en tu propio entorno FileMaker antes de desplegar en producción. FileMaker® es una marca registrada de Claris International Inc.

## Skills disponibles

| Skill | Descripción | Compatibilidad |
|-------|-------------|----------------|
| [filemaker-svg-builder](./skills/filemaker-svg-builder) | Construye, repara y valida iconos SVG para botones y barras de botones de FileMaker Pro según la especificación SVG Grammar de FileMaker Pro 14. | FileMaker Pro 14+ |
| [filemaker-saxml-builder](./skills/filemaker-saxml-builder) | Construye, valida, repara y corrige archivos XML de FileMaker (SAXML/fmxmlsnippet) para scripts, campos, layouts, temas y mucho más. | FileMaker Pro 19+ / Claris FileMaker 21+ |
| [contribute-skill](./skills/contribute-skill) | Guía a un miembro de la org FMWarriors para contribuir un nuevo skill a este repositorio — clonación, ramas, estructura, validación y apertura de pull request vía gh CLI. No se necesitan conocimientos de git. | Requiere git + gh CLI |

## Úsalo en tu agente

### Claude Code

Registra este repositorio como marketplace de plugins de Claude Code ejecutando:

```
/plugin marketplace add fmwarriors/skills
```

Luego instala el plugin de skills de FileMaker:

```
/plugin install filemaker-skills@fmwarriors-skills
```

También puedes clonar el repositorio y apuntar Claude Code al directorio `skills/` en la configuración de tu proyecto.

### VS Code (GitHub Copilot)

VS Code busca skills en `.agents/skills/` por defecto. Copia cualquier carpeta de skill a `.agents/skills/` en tu proyecto:

```bash
cp -r skills/filemaker-svg-builder /tu-proyecto/.agents/skills/
```

Abre el panel de Copilot Chat en modo **Agent** y escribe `/skills` para confirmar que aparece.

### Cursor

En Cursor, ve a Settings → Features → Agent Skills y añade la ruta al directorio `skills/` de este repositorio, o copia carpetas de skills individuales al directorio `.cursor/skills/` de tu proyecto.

### Otros agentes

Cualquier agente compatible con la [especificación Agent Skills](https://agentskills.io/specification) puede utilizar estos skills. Coloca la carpeta del skill donde tu agente busca skills, o configura el directorio de skills del agente para apuntar a `skills/` de este repositorio.

Consulta el [Client Showcase](https://agentskills.io/clients) para ver la lista completa de agentes compatibles y sus instrucciones de configuración.

## Crear un nuevo skill de FileMaker

Crear un skill es sencillo: basta con una carpeta con un archivo `SKILL.md` que contenga frontmatter YAML e instrucciones. Usa la **plantilla** de este repositorio como punto de partida:

```bash
cp -r template skills/mi-nuevo-skill-filemaker
```

Edita `skills/mi-nuevo-skill-filemaker/SKILL.md`:

```markdown
---
name: mi-nuevo-skill-filemaker
description: Una descripción clara de qué hace este skill y cuándo usarlo.
license: MIT
metadata:
  author: Tu Nombre
  version: "1.0"
---

# Mi Skill de FileMaker

[Instrucciones aquí]
```

El frontmatter solo requiere dos campos:
- `name` — debe coincidir exactamente con el nombre de la carpeta, en minúsculas con guiones
- `description` — qué hace el skill y cuándo activarlo (máx. 1024 caracteres)

Consulta la [especificación completa](./spec/agent-skills-spec.md) o [agentskills.io/specification](https://agentskills.io/specification) para todos los campos disponibles.

## Contribuir

¡Las contribuciones son bienvenidas! Consulta [CONTRIBUTING_ES.md](.github/CONTRIBUTING_ES.md) para ver las pautas sobre cómo añadir nuevos skills o mejorar los existentes.

## Licencia

Los skills de este repositorio están bajo la [Licencia MIT](./skills/filemaker-svg-builder/LICENSE.txt) salvo que se indique lo contrario en el archivo `LICENSE.txt` del skill correspondiente.

---

**Autor:** Francesc Sans &lt;fsans@ntwk.es&gt; — [FMWarriors](https://github.com/fmwarriors), Barcelona 2025
