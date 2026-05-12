[![English](https://img.shields.io/badge/lang-English-blue?style=flat-square)](./CONTRIBUTING.md)
[![Español](https://img.shields.io/badge/lang-Español-red?style=flat-square)](./CONTRIBUTING_ES.md)

# Contribuir a FMWarriors Skills

¡Gracias por tu interés en contribuir skills de FileMaker Pro!
Esta guía describe el proceso completo — desde hacer un fork del repositorio hasta que tu PR sea aceptado.

---

## El flujo de trabajo de un vistazo

```
Fork → Clonar → Rama → Añadir skill → Probar → Push → Pull Request → Revisión → Merge
```

---

## Paso a paso: Añadir un nuevo skill

### 1. Haz un fork del repositorio

Haz clic en **Fork** en https://github.com/fmwarriors/skills — esto crea tu propia copia bajo tu cuenta de GitHub.

### 2. Clona tu fork

```bash
git clone https://github.com/TU_USUARIO/skills.git
cd skills
```

### 3. Crea una rama

Trabaja siempre en una rama, nunca directamente en `main`:

```bash
git checkout -b add/mi-nuevo-skill
```

Usa un nombre descriptivo como `add/filemaker-theme-builder` o `fix/svg-builder-typos`.

### 4. Copia la plantilla

```bash
cp -r template skills/nombre-de-tu-skill
```

> El nombre de la carpeta debe ser **solo minúsculas con guiones** y coincidir exactamente con el campo `name`
> en `SKILL.md`. Ejemplo: carpeta `filemaker-theme-builder` → `name: filemaker-theme-builder`

### 5. Escribe tu SKILL.md

Edita `skills/nombre-de-tu-skill/SKILL.md`:

```markdown
---
name: nombre-de-tu-skill
description: Qué hace este skill y exactamente cuándo debe activarlo un agente.
             Incluye palabras clave específicas de FileMaker. Máx. 1024 caracteres.
license: MIT
compatibility: FileMaker Pro 19+ / Claris FileMaker 21+
metadata:
  author: Tu Nombre o usuario de GitHub
  version: "1.0"
---

# Título de tu Skill

## Descripción general
Resumen breve de lo que hace el skill.

## Instrucciones
Instrucciones paso a paso que el agente debe seguir...
```

**Campos obligatorios del frontmatter:**
- `name` — debe coincidir exactamente con el nombre de la carpeta, solo `[a-z0-9-]`, máx. 64 caracteres
- `description` — el agente usa este campo para decidir si activar el skill; incluye palabras clave relevantes de FileMaker

**Opcionales pero recomendados:**
- `license` — `MIT` o `Complete terms in LICENSE.txt`
- `compatibility` — requisitos de versión de FileMaker
- `metadata.author`, `metadata.version`

### 6. Añade archivos complementarios (opcional pero recomendado)

```
skills/nombre-de-tu-skill/
├── SKILL.md          ← Obligatorio
├── LICENSE.txt       ← Recomendado (copia de un skill existente y actualiza la línea de copyright)
├── references/       ← Documentación detallada que el agente carga bajo demanda
│   └── REFERENCE.md
├── scripts/          ← Scripts ejecutables en Python/Bash
├── assets/           ← Plantillas, SVGs, archivos de datos
└── examples/         ← Ejemplos de entradas/salidas que muestran el skill en acción
```

### 7. Añade un LICENSE.txt por skill

Copia un `LICENSE.txt` existente y actualiza la línea de copyright:

```bash
cp skills/filemaker-svg-builder/LICENSE.txt skills/nombre-de-tu-skill/LICENSE.txt
# Edita la línea de copyright con tu nombre y año
```

### 8. Registra el skill en el manifiesto del marketplace

Abre `.claude-plugin/marketplace.json` y añade la ruta de tu skill al array `skills`
dentro del plugin `filemaker-skills`:

```json
"skills": [
  "./skills/filemaker-svg-builder",
  "./skills/filemaker-saxml-builder",
  "./skills/nombre-de-tu-skill"   ← añade esta línea
]
```

### 9. Actualiza el README raíz

Añade una fila a la tabla de skills en `README.md` (y en `README_ES.md` si quieres):

```markdown
| [nombre-de-tu-skill](./skills/nombre-de-tu-skill) | Descripción en una línea | FileMaker Pro XX+ |
```

### 10. Prueba tu skill

Antes de enviar, prueba con al menos un agente compatible:

- Carga el skill en Claude Code, VS Code Copilot, Cursor u otro agente compatible
- Confirma que se activa con los prompts correctos (revisa las palabras clave de `description`)
- Confirma que el agente sigue las instrucciones correctamente

### 11. Commit y push

```bash
git add .
git commit -m "Add filemaker-nombre-de-tu-skill skill"
git push origin add/nombre-de-tu-skill
```

### 12. Abre un Pull Request

Ve a https://github.com/fmwarriors/skills y haz clic en **"Compare & pull request"**.

En la descripción del PR incluye:
- Qué hace el skill
- Cómo lo has probado (qué agente, qué prompts usaste)
- Requisitos de versión de FileMaker

Mantén cada PR enfocado en **un solo skill** — facilita mucho la revisión.

---

## Mejorar un skill existente

El mismo flujo: fork → rama → editar → push → PR.

- Corregir errores tipográficos o aclarar instrucciones — siempre bienvenido
- Añadir casos especiales, ejemplos o archivos de referencia que falten
- Incrementa `metadata.version` en el frontmatter cuando hagas cambios significativos
- Describe qué has cambiado y por qué en la descripción del PR

---

## Lista de verificación de calidad

Antes de enviar, comprueba:

- [ ] El nombre de la carpeta coincide con `name` en el frontmatter de `SKILL.md` (solo minúsculas y guiones)
- [ ] `description` tiene ≤ 1024 caracteres e incluye palabras clave de activación relevantes
- [ ] Todos los elementos secundarios obligatorios están presentes en los ejemplos XML
- [ ] `LICENSE.txt` está presente con la línea de copyright correcta
- [ ] Añadido a `.claude-plugin/marketplace.json`
- [ ] Añadido a la tabla de skills en `README.md`
- [ ] Probado con al menos un agente

---

## ¿Preguntas?

Abre una [GitHub Discussion](https://github.com/fmwarriors/skills/discussions) o crea un [Issue](https://github.com/fmwarriors/skills/issues).
