# SKILL: FileMaker SVG Icon Builder

## Purpose
Build valid SVG icons for FileMaker Pro button icons and button bars according to the FileMaker Pro 14 SVG Grammar specification.

## Core Requirements

### File Structure
- Start with XML declaration: `<?xml version="1.0" encoding="utf-8"?>`
- Use UTF-8 encoding (UTF-16 not supported)
- Root element must be `<svg>` with required namespace declarations:
  - `xmlns="http://www.w3.org/2000/svg"`
  - `xmlns:xlink="http://www.w3.org/1999/xlink"` (for internal links)
- MUST specify `width` and `height` attributes on root `<svg>` element

### Coordinate System
- Origin at top-left corner
- Positive x-axis points right
- Positive y-axis points down
- All coordinates in user coordinate units (no unit symbols)

## Supported Elements

### Basic Shapes
- **`<line>`**: Stroked only
  - Attributes: `x1`, `y1`, `x2`, `y2`, `transform`
- **`<rect>`**: Stroked and filled
  - Attributes: `x`, `y`, `width`, `height`, `rx`, `ry` (for rounded corners), `transform`
  - Defaults: `x=0`, `y=0` if not specified
- **`<circle>`**: Stroked and filled
  - Attributes: `cx`, `cy`, `r`, `transform`
  - Defaults: `cx=0`, `cy=0` if not specified
- **`<ellipse>`**: Stroked and filled
  - Attributes: `cx`, `cy`, `rx`, `ry`, `transform`
  - Defaults: `cx=0`, `cy=0` if not specified

### Complex Shapes
- **`<polyline>`**: Connected line segments, stroked only
  - Attributes: `points` (even number of coordinates), `transform`
- **`<polygon>`**: Closed polyline, stroked and filled
  - Attributes: `points` (even number of coordinates), `transform`
  - Start and end points auto-connected
- **`<path>`**: Most versatile element for complex shapes
  - Attributes: `d` (path commands), `transform`
  - Uppercase commands = absolute coordinates
  - Lowercase commands = relative coordinates

### Grouping Elements
- **`<g>`**: Groups child elements, inherits styles
  - Attributes: `transform`
- **`<svg>`**: Can be nested for viewports
  - Attributes: `version`, `x` (only 0 supported), `y` (only 0 supported), `width`, `height`, `viewBox`
- **`<symbol>`**: Template elements referenced by `<use>`
  - Attributes: `id`, `viewBox`, `preserveAspectRatio` (only xMinyMin supported)
- **`<use>`**: Duplicates referenced elements
  - Attributes: `x`, `y`, `width`, `height`, `xlink:href`

### Definitions
- **`<defs>`**: Container for referenced elements
  - Should be first child of `<svg>`
  - Elements only render when referenced

### Gradients
- **`<linearGradient>`**: Smooth color transition along vector
  - Attributes: `x1`, `y1`, `x2`, `y2`, `gradientUnits`
  - Defaults: `x1=0%`, `y1=0%`, `x2=0%`, `y2=0%`
- **`<radialGradient>`**: Circular color transition
  - Attributes: `cx`, `cy`, `r`, `gradientUnits`
  - Defaults: `cx=50%`, `cy=50%`, `r=0%`
- **`<stop>`**: Defines gradient colors
  - Attributes: `offset` (0-1 or 0%-100%), `stop-color`, `stop-opacity`

## Display Properties

### Stroke Properties
- `stroke`: Color of outline
- `stroke-width`: Width in user coordinates
- `stroke-opacity`: 0.0 (transparent) to 1.0 (opaque)
- `stroke-dasharray`: Pattern of dashes and gaps
- Default line cap: butt
- Default line join: miter (limit of 10)

### Fill Properties
- `fill`: Interior color
- `fill-opacity`: 0.0 (transparent) to 1.0 (opaque)
- Default fill rule: nonzero

### Color Specification
- `none`: No fill or stroke
- Color keywords: `aliceblue`, `antiquewhite`, `cyan`, `lightgray`, etc.
- Hex format: `#rrggbb` or `#rgb`
- RGB function: `rgb(r, g, b)` where r, g, b are 0-255 or 0%-100%

### Style Syntax Options
1. Attribute style: `fill="red" stroke="blue" stroke-width="3"`
2. CSS2 style: `style="fill:red;stroke:blue;stroke-width:3"`

## Transformations
Apply via `transform` attribute (processed before other coordinates):
- `matrix(a,b,c,d,e,f)`: 3x3 transformation matrix
- `translate(tx ty)`: Move along axes
- `scale(sx sy)`: Scale (if sy omitted, equals sx)
- `rotate(angle cx cy)`: Rotate in radians around point (defaults to origin)
- `skewX(angle)`: Skew along x-axis in radians
- `skewY(angle)`: Skew along y-axis in radians

## Theme Integration (FileMaker Specific)

### Dynamic Fill Colors
- FileMaker wraps SVG in `<g class="fm_fill">` element
- Do NOT explicitly set fill colors if you want theme-controlled colors
- Child elements inherit `fm_fill` color from parent group
- Enables dynamic theme updates and conditional formatting
- Elements can override inherited fill with explicit colors

### Example Pattern
```xml
<!-- User creates (no explicit fill) -->
<rect x="50" y="25" width="100" height="125" />

<!-- FileMaker wraps with fm_fill -->
<g class="fm_fill">
  <rect x="50" y="25" width="100" height="125" />
</g>
```

## Validation Rules
1. Width and height MUST be specified on root `<svg>`
2. All coordinates without unit symbols
3. Width/height must be ≥ 0 (0 means no render)
4. Radius values must be ≥ 0
5. Even number of coordinates in `points` attributes
6. Valid namespace declarations required
7. UTF-8 encoding required

## Best Practices
1. Place `<defs>` as first child of `<svg>`
2. Use `<path>` for complex shapes (most versatile)
3. Use CSS2 style syntax for compact code
4. Omit fill colors for theme-compatible icons
5. Group related elements with `<g>` for shared styling
6. Use `<symbol>` and `<use>` for repeated patterns
7. Apply transforms at group level when possible
8. Use meaningful IDs for referenced elements

## Limitations
- Only user coordinate units supported
- No file uploads or external resources
- UTF-16 not supported
- preserveAspectRatio: only xMinyMin supported
- svg x, y: only 0 values supported
- Fill rule: only nonzero supported

## Example Template
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="200"
     height="200"
     viewBox="0 0 200 200">
  <defs>
    <!-- Gradients, symbols, etc. -->
  </defs>
  <g>
    <!-- Shape elements here -->
  </g>
</svg>
```

## Common Patterns

### Rounded Rectangle Button
```xml
<rect x="10" y="10" rx="5" ry="5" width="180" height="180"
      style="stroke:blue;stroke-width:2"/>
```

### Icon with Gradient
```xml
<defs>
  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#F60"/>
    <stop offset="100%" stop-color="#FF6"/>
  </linearGradient>
</defs>
<circle cx="100" cy="100" r="80" fill="url(#grad1)"/>
```

### Reusable Symbol
```xml
<defs>
  <symbol id="icon" viewBox="0 0 20 20">
    <rect x="2" y="2" width="16" height="16"/>
  </symbol>
</defs>
<use x="50" y="50" width="50" height="50" xlink:href="#icon"/>
```

---

**Reference**: FileMaker Pro 14 SVG Grammar for Button Icons  
**Specification**: Subset of W3C SVG standard optimized for FileMaker Pro