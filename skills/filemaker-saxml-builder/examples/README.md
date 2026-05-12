# FileMaker SAXML Builder - Example Fixes

**Author**: Francesc Sans <fsans@ntwk.es> | Barcelona, 2025 | Version 0.0.27

---

This directory contains before/after examples of common SAXML errors and their fixes.

## Example 1: Missing Required Attributes and Elements

**Files**: `01-broken-field.xml` → `01-fixed-field.xml`

**Problems**:
- Missing `type="FMObjectList"` attribute on root element
- Missing `id`, `dataType`, `fieldType` attributes on Field element
- Missing required child elements: `<Validation>`, `<Storage>`
- Incomplete `<AutoEnter>` element
- Wrong boolean capitalization ("true" vs "True")

**Fixes Applied**:
- Added `type="FMObjectList"` to `<fmxmlsnippet>`
- Added all required Field attributes: `id="1"`, `dataType="Text"`, `fieldType="Normal"`
- Added complete `<AutoEnter>` with all attributes and `<ConstantData>` child
- Added complete `<Validation>` with all attributes
- Added complete `<Storage>` with all attributes
- Changed boolean values to proper capitalization

**Validation**:
```bash
# Before (fails)
xmllint --noout --schema ../saxml-22.0.4.xsd 01-broken-field.xml

# After (succeeds)
xmllint --noout --schema ../saxml-22.0.4.xsd 01-fixed-field.xml
```

---

## Example 2: Calculation Field Issues

**Files**: `02-broken-calculation.xml` → `02-fixed-calculation.xml`

**Problems**:
- Missing CDATA wrapper around calculation formula
- Lowercase boolean values ("false" instead of "False")
- Special characters in calculation could cause XML parsing issues

**Fixes Applied**:
- Wrapped calculation formula in `<![CDATA[...]]>`
- Changed all boolean values to proper capitalization: "False" and "True"
- This ensures special characters like `&`, `<`, `>` in formulas don't break XML parsing

**Why CDATA Matters**:
FileMaker calculations often contain:
- Ampersands (`&`) for string concatenation
- Comparison operators (`<`, `>`, `<=`, `>=`)
- Logical operators (`and`, `or`, `not`)
- Complex nested functions

Without CDATA, these would need to be XML-escaped (e.g., `&amp;`, `&lt;`, `&gt;`), which is error-prone and harder to read.

**Validation**:
```bash
# Before (fails)
xmllint --noout --schema ../saxml-22.0.4.xsd 02-broken-calculation.xml

# After (succeeds)
xmllint --noout --schema ../saxml-22.0.4.xsd 02-fixed-calculation.xml
```

---

## Example 3: Wrong XML Format for Custom Menus

**Files**: `03-broken-menu-wrong-format.xml` → `03-fixed-menu-correct-format.xml`

**Problems**:
- Using `<fmxmlsnippet>` format for custom menus (WRONG!)
- Custom menus require `<FMObjectTransfer>` format
- Missing catalog structure
- Missing UUID tracking
- Missing PasteIndexList
- Wrong encoding (UTF-8 vs UTF-16)

**Fixes Applied**:
- Changed root element from `<fmxmlsnippet>` to `<FMObjectTransfer>`
- Added all required FMObjectTransfer attributes: `version`, `membercount`, `Source`, `File`, `UUID`, `locale`, `timestamp`
- Wrapped menu in `<CustomMenuSetCatalog>` structure
- Added `<UUID>` element with modification tracking
- Added `<TagList>` (can be empty)
- Added `<CustomMenuSetReference>` for catalog
- Wrapped actual menu in `<ObjectList>`
- Added `<PasteIndexList>` for clipboard operations
- Changed encoding from UTF-8 to UTF-16

**Why Two Formats?**:
FileMaker uses two distinct XML formats:
1. **fmxmlsnippet** (simple) - For most objects: scripts, fields, tables, layouts, themes, functions, value lists
2. **FMObjectTransfer** (complex) - For custom menus/menu sets with modification tracking and catalog structure

**Validation**:
```bash
# Before (fails - wrong schema)
xmllint --noout --schema ../saxml-22.0.4.xsd 03-broken-menu-wrong-format.xml

# After (succeeds - correct schema)
xmllint --noout --schema ../fmobjecttransfer-22.0.4.xsd 03-fixed-menu-correct-format.xml
```

---

## How to Use These Examples

1. **Study the broken files** to understand common mistakes
2. **Compare with fixed files** to see the corrections
3. **Run validation commands** to verify the fixes
4. **Use as templates** for your own SAXML generation

## Quick Validation Commands

```bash
# Validate fmxmlsnippet format
xmllint --noout --schema ../saxml-22.0.4.xsd your-file.xml

# Validate FMObjectTransfer format
xmllint --noout --schema ../fmobjecttransfer-22.0.4.xsd your-file.xml

# Check which format a file uses
head -n 5 your-file.xml | grep -E "(fmxmlsnippet|FMObjectTransfer)"
```

## Common Error Patterns

### "Element X is not expected"
→ Missing or extra child elements, or wrong parent element

### "Attribute Y is required"
→ Missing required attribute on element

### "Invalid attribute value"
→ Wrong data type, enum value, or format

### "This element is not expected. Expected is X"
→ Wrong element used, or elements in wrong order

### "Character content is not allowed"
→ Text directly in element that should only have child elements

## More Examples

See the main samples directory for more real-world examples:
- `/Volumes/DATA00/HOME/Desktop/saxml/samples/` - Standard format examples
- `/Volumes/DATA00/HOME/Desktop/saxml/rare/` - FMObjectTransfer examples
