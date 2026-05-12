---
name: filemaker-svg-builder
description: Build, heal, and validate SVG icons for FileMaker Pro button icons and button bars according to the FileMaker Pro 14 SVG Grammar specification. Use when users request creating, modifying, fixing, healing, or validating SVG icons specifically for FileMaker Pro, FileMaker button icons, FileMaker button bars, or mention FileMaker-compatible SVG files. Also trigger when users need to convert existing SVGs to FileMaker format, automatically fix compatibility issues, verify SVG compliance with FileMaker's restricted subset of the W3C SVG standard, want theme-compatible icons with fm_fill integration, or need help with FileMaker SVG validation, coordinate systems, transformations, or supported elements.
license: Complete terms in LICENSE.txt
compatibility: FileMaker Pro 14+
metadata:
  author: FMWarriors — Francesc Sans
  version: "1.0"
  org: FMWarriors
---

# FileMaker SVG Icon Builder

Build SVG icons that comply with the FileMaker Pro 14 SVG Grammar specification - a restricted subset of W3C SVG designed for FileMaker Pro button icons and button bars.

## Quick Start

### Create a New Icon

Start with a template based on your needs:

```bash
# Copy basic template
cp assets/basic_template.svg my_icon.svg

# Or start with theme-compatible button
cp assets/theme_button.svg my_button.svg
```

### Common Icon Requests

**Simple theme-compatible icon:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="100" height="100" viewBox="0 0 100 100">
  <!-- No fill attribute - will inherit from FileMaker fm_fill wrapper -->
  <circle cx="50" cy="50" r="40"/>
</svg>
```

**Icon with stroke:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="100" height="100" viewBox="0 0 100 100">
  <!-- No fill, but stroke is preserved -->
  <rect x="20" y="20" width="60" height="60" rx="5"
        stroke="#000000" stroke-width="2"/>
</svg>
```

**Icon with gradient (fixed colors):**
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="100" height="100" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4A90E2"/>
      <stop offset="100%" stop-color="#357ABD"/>
    </linearGradient>
  </defs>
  <!-- Gradient fills are not replaced by theme -->
  <circle cx="50" cy="50" r="40" fill="url(#grad)"/>
</svg>
```

## Healing Existing SVG Files

Got an existing SVG that isn't FileMaker-compatible? Use the healing script to automatically fix common issues:

```bash
# Heal an SVG file and save to new file
python3 scripts/heal_filemaker_svg.py input.svg output.svg

# Heal and overwrite the original file
python3 scripts/heal_filemaker_svg.py myicon.svg
```

### What the Healer Fixes

The healing script automatically corrects:

✓ **Missing XML declaration** - Adds `<?xml version="1.0" encoding="utf-8"?>`
✓ **Missing namespaces** - Adds required xmlns declarations
✓ **Missing width/height** - Extracts from viewBox or adds defaults
✓ **Unit symbols** - Removes px, pt, cm, etc. from all coordinates
✓ **Negative radius values** - Changes negative values to 0
✓ **Odd coordinate counts** - Fixes polyline/polygon points
✓ **Degrees to radians** - Converts rotation/skew transformations
✓ **Encoding issues** - Converts UTF-16 to UTF-8
✓ **Fill attribute on root SVG** - Removes (not needed)
✓ **Fill attributes on shapes** - Removes (except gradients/none) so they inherit from fm_fill

### Example Healing Session

```bash
$ python3 scripts/heal_filemaker_svg.py broken.svg fixed.svg

Healing: broken.svg
Output: fixed.svg
============================================================

✅ FIXES APPLIED:
  1. Added missing XML declaration
  2. Added width="200" (extracted from viewBox)
  3. Added height="200" (extracted from viewBox)
  4. Removed units from cx: "50px" → "50"
  5. Removed units from cy: "50px" → "50"
  6. Removed units from circle radius: 40px → 40
  7. Converted rotation from degrees to radians: 90° → 1.5708 rad
  8. Fixed negative rect rx: -5 → 0

✅ Healed SVG saved successfully!

💡 Tip: Run validation to confirm FileMaker compliance:
    python3 scripts/validate_filemaker_svg.py fixed.svg
```

### When to Use Healing

Use the healing script when you:
- Have SVG icons from design tools (Illustrator, Figma, etc.)
- Downloaded SVG files from icon libraries
- Converted other graphics formats to SVG
- Received SVG files that fail FileMaker validation
- Want to quickly fix multiple compatibility issues

## Core Workflow

### 1. Understand Requirements

Gather information about the icon:
- Size (width/height)
- Visual design (shapes, colors, gradients)
- Theme integration needs (should it respond to FileMaker themes?)
- Complexity (simple shapes vs. complex paths)

### 2. Choose Starting Point

Select the appropriate template from `assets/`:
- `basic_template.svg` - Minimal structure for any icon
- `theme_button.svg` - Theme-compatible button with rounded corners
- `gradient_icon.svg` - Example with linear and radial gradients
- `reusable_symbol.svg` - Pattern for repeated elements using `<symbol>` and `<use>`
- `common_shapes.svg` - Reference showing all basic shape elements

### 3. Build the Icon

Follow these critical requirements:

**File Structure:**
1. Start with XML declaration: `<?xml version="1.0" encoding="utf-8"?>`
2. Root `<svg>` with required attributes:
   - `xmlns="http://www.w3.org/2000/svg"`
   - `xmlns:xlink="http://www.w3.org/1999/xlink"`
   - `width` and `height` (REQUIRED)
3. Place `<defs>` as first child if used

**Coordinate System:**
- Origin at top-left corner
- Positive x-axis points right, positive y-axis points down
- Use only user coordinate units (NO px, pt, cm, etc.)

**Supported Elements:**
- Basic shapes: `<line>`, `<rect>`, `<circle>`, `<ellipse>`
- Complex shapes: `<polyline>`, `<polygon>`, `<path>`
- Grouping: `<g>`, `<svg>`, `<symbol>`, `<use>`
- Definitions: `<defs>`
- Gradients: `<linearGradient>`, `<radialGradient>`, `<stop>`

**Transformations** (in radians, not degrees):
- `translate(tx ty)` - Move along axes
- `scale(sx sy)` - Scale (sy optional)
- `rotate(angle cx cy)` - Rotate in RADIANS around point
- `skewX(angle)`, `skewY(angle)` - Skew in RADIANS
- `matrix(a,b,c,d,e,f)` - Full transformation matrix

**Critical: Rotation uses RADIANS, not degrees!**

### 4. Validate the Icon

Always validate before use:

```bash
python3 scripts/validate_filemaker_svg.py my_icon.svg
```

The validator checks:
- ✓ UTF-8 encoding
- ✓ XML declaration present
- ✓ Required namespace declarations
- ✓ Width and height specified
- ✓ No unit symbols in coordinates
- ✓ Valid radius values (≥ 0)
- ✓ Even number of coordinates in points attributes
- ✓ Proper `<defs>` placement

### 5. Refine Based on Validation

Fix any errors reported by the validator. Common issues:
- Missing width/height on root `<svg>`
- Unit symbols in coordinates (remove "px", "pt", etc.)
- Negative radius values
- Missing namespace declarations
- Wrong encoding (must be UTF-8)

## Theme Integration (fm_fill)

FileMaker Pro automatically wraps SVG content in `<g class="fm_fill">` to enable dynamic theming.

### Critical Principles (From Official FileMaker Documentation)

**For Theme-Compatible Icons:**

1. **DO NOT add fill attributes** to shape elements
2. **FileMaker automatically adds** `<g class="fm_fill">` wrapper when saving
3. **Elements inherit** fill color from the fm_fill parent group
4. **Strokes are preserved** - you can specify stroke properties

```xml
<!-- CORRECT: Your SVG (before FileMaker saves it) -->
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <!-- No fill attribute - will inherit from fm_fill -->
  <rect x="50" y="25" width="100" height="125"/>
</svg>

<!-- After FileMaker Pro processes it: -->
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <g class="fm_fill">
    <rect x="50" y="25" width="100" height="125"/>
    <!-- Inherits fill color from fm_fill parent -->
  </g>
</svg>
```

### Key Rules

**What FileMaker Does:**
- Automatically wraps your shapes in `<g class="fm_fill">`
- The fm_fill group provides the theme/conditional format color
- Child elements **inherit** this color automatically

**What You Should Do:**
- ✅ **Omit** fill attributes on shapes (for theme colors)
- ✅ **Keep** stroke attributes (FileMaker preserves these)
- ✅ **Use** `fill="none"` for transparent shapes
- ✅ **Add** explicit fill only for fixed colors (not theme-responsive)

### Stroke Attributes

FileMaker preserves stroke properties:

```xml
<path d="..."
      stroke="#000000"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"/>
<!-- No fill - inherits from fm_fill wrapper -->
```

### Fixed Colors (Non-Theme)

For icons that should **NOT** change with themes, add explicit fill:

```xml
<!-- Error icon - always red, never theme color -->
<circle cx="50" cy="50" r="10" fill="#FF0000" stroke="#CC0000" stroke-width="2"/>
```

Use explicit fill for:
- Icons with specific brand colors that shouldn't change
- Status indicators (error=red, success=green, warning=yellow)
- Multi-color logos or designs
- Gradient fills: `fill="url(#gradientId)"`

## Common Patterns

### Pattern 1: Simple Icon
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="100" height="100" viewBox="0 0 100 100">
  <path d="M 20 80 L 50 20 L 80 80 Z"/>
</svg>
```

### Pattern 2: Grouped Elements with Shared Style
```xml
<svg width="200" height="200" ...>
  <g style="stroke:#333;stroke-width:2;fill:none">
    <circle cx="60" cy="60" r="30"/>
    <circle cx="140" cy="60" r="30"/>
    <path d="M 40 120 Q 100 160 160 120"/>
  </g>
</svg>
```

### Pattern 3: Reusable Components
```xml
<svg width="300" height="100" ...>
  <defs>
    <symbol id="star" viewBox="0 0 20 20">
      <path d="M 10 2 L 12 8 L 18 8 L 13 12 L 15 18 L 10 14 L 5 18 L 7 12 L 2 8 L 8 8 Z"/>
    </symbol>
  </defs>
  <use x="10" y="10" width="30" height="30" xlink:href="#star"/>
  <use x="60" y="10" width="30" height="30" xlink:href="#star"/>
  <use x="110" y="10" width="30" height="30" xlink:href="#star"/>
</svg>
```

### Pattern 4: Icon with Gradient Background
```xml
<svg width="100" height="100" ...>
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#667EEA"/>
      <stop offset="100%" stop-color="#764BA2"/>
    </linearGradient>
  </defs>
  <rect width="100" height="100" fill="url(#bg)"/>
  <circle cx="50" cy="50" r="25" fill="white"/>
</svg>
```

## Detailed Documentation

For comprehensive specification details:
- **Grammar reference**: See `references/svg_grammar.md`
- **Official documentation links**: See `references/documentation_links.md`

Key topics in grammar reference:
- Complete list of supported elements with attributes
- Display properties (stroke, fill, colors)
- Path commands syntax
- Transformation details
- Validation rules
- Best practices

## Python Scripts

Two powerful Python scripts are included for SVG processing:

### Healing Script

Automatically fixes SVG files to make them FileMaker-compatible.

**Usage:**
```bash
# Save to new file
python3 scripts/heal_filemaker_svg.py input.svg output.svg

# Overwrite original
python3 scripts/heal_filemaker_svg.py myicon.svg
```

**What it fixes:**
- Missing XML declaration
- Missing namespace declarations
- Missing width/height attributes
- Unit symbols in coordinates (px, pt, cm, etc.)
- Negative radius values
- Odd number of coordinates in points
- Degrees to radians conversion
- UTF-16 to UTF-8 encoding

### Validation Script

Checks SVG files for FileMaker SVG Grammar compliance.

**Usage:**
```bash
python3 scripts/validate_filemaker_svg.py <path-to-svg-file>
```

**Exit codes:**
- 0 = Valid
- 1 = Validation errors found

**What it checks:**
- File encoding (UTF-8 required)
- XML declaration
- Namespace declarations on root `<svg>`
- Required width/height attributes
- Coordinate values (no unit symbols)
- Radius values (must be ≥ 0)
- Points attributes (even number of coordinates)
- Element-specific requirements

### Recommended Workflow

For existing SVG files:
```bash
# 1. Heal the file
python3 scripts/heal_filemaker_svg.py original.svg healed.svg

# 2. Validate the result
python3 scripts/validate_filemaker_svg.py healed.svg
```

## Asset Templates

Pre-built templates to accelerate icon creation:

- **basic_template.svg** - Minimal valid FileMaker SVG structure
- **theme_button.svg** - Rounded button with theme integration
- **gradient_icon.svg** - Examples of linear and radial gradients
- **reusable_symbol.svg** - Using `<symbol>` and `<use>` for efficiency
- **common_shapes.svg** - Reference showing all basic shape elements

## Key Differences from Standard SVG

FileMaker SVG is a **restricted subset** of W3C SVG:

**Not Supported:**
- UTF-16 encoding (UTF-8 only)
- Unit symbols (px, pt, cm, mm, in, em, etc.)
- Most text elements
- Animation elements
- External resources/file uploads
- preserveAspectRatio (except xMinYMin)
- Fill rules (except nonzero)

**Critical Requirements:**
1. Width and height MUST be specified on root `<svg>`
2. User coordinate units only (no unit symbols)
3. Required namespace declarations
4. UTF-8 encoding only
5. Transformations use radians, not degrees

## Tips for Success

1. **Heal first, validate second** - For existing SVGs, run healing script then validate
2. **Start with templates** - Faster than starting from scratch for new icons
3. **Theme integration first** - Omit fills unless specific colors required
4. **Use `<defs>` for reusability** - Place as first child of root `<svg>`
5. **Group related elements** - Use `<g>` for shared styling and transforms
6. **Remember: radians, not degrees** - For rotate, skewX, skewY (healing script auto-converts)
7. **No unit symbols** - Just numbers for all coordinates (healing script auto-removes)
8. **Always validate before deploying** - Catch issues early
9. **Test in FileMaker** - Final validation is visual inspection in FileMaker Pro

## Example Workflow

User request: "Create a settings icon (gear) for a FileMaker button"

1. **Understand**: 32x32 icon, theme-compatible (no explicit fill)
2. **Start**: Copy `assets/basic_template.svg`
3. **Build**: Create gear shape using path or circles
4. **Validate**: Run `python3 scripts/validate_filemaker_svg.py settings_icon.svg`
5. **Fix**: Address any validation errors
6. **Deliver**: Provide the validated SVG file

## Troubleshooting

### Quick Fix: Use the Healing Script

For most compatibility issues, the healing script can automatically fix them:
```bash
python3 scripts/heal_filemaker_svg.py problematic.svg fixed.svg
```

### Common Issues and Manual Fixes

**"Missing width or height"**
- **Auto-fix**: Healing script extracts from viewBox or adds defaults
- **Manual**: Add `width="200" height="200"` to root `<svg>` element

**"Unit symbols not allowed"**
- **Auto-fix**: Healing script removes all unit symbols (px, pt, etc.)
- **Manual**: Change `width="100px"` to `width="100"`

**"Invalid encoding"**
- **Auto-fix**: Healing script converts UTF-16 to UTF-8
- **Manual**: Ensure file is saved as UTF-8, not UTF-16

**"Namespace missing"**
- **Auto-fix**: Healing script adds required xmlns declarations
- **Manual**: Add `xmlns="http://www.w3.org/2000/svg"` to root `<svg>`

**"Rotation not working correctly"**
- **Auto-fix**: Healing script converts common degree values (45, 90, 180, etc.) to radians
- **Manual**: Convert manually - radians = degrees × π/180

**"Points must have even number"**
- **Auto-fix**: Healing script removes last coordinate to make it even
- **Manual**: Check polyline/polygon points attribute for complete coordinate pairs

**"Icon doesn't match theme colors"**
- **Not auto-fixed**: This is a design choice
- **Manual**: Remove explicit fill attributes to inherit from fm_fill
