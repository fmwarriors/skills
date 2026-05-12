---
name: filemaker-saxml-builder
description: Build, validate, heal, and fix FileMaker XML (SAXML/fmxmlsnippet) format files for scripts, fields, tables, layouts, themes, custom functions, value lists, and custom menus. Use when creating new FileMaker XML snippets, validating existing SAXML against schemas, fixing broken fmxmlsnippet or FMObjectTransfer XML, or working with any FileMaker XML import/export format. Triggers on keywords: saxml, fmxmlsnippet, FMObjectTransfer, FileMaker XML, FileMaker field definition, FileMaker script XML, FileMaker snippet.
license: Complete terms in LICENSE.txt
compatibility: FileMaker Pro 19+ / Claris FileMaker 21+. Requires xmllint (libxml2) for schema validation.
metadata:
  author: FMWarriors — Francesc Sans
  version: "1.0"
  org: FMWarriors
  schema-version: "22.0.4"
---

# FileMaker SAXML Builder & Validator

Build, validate, heal, and fix FileMaker XML (SAXML) format files. Ensures all generated or modified XML conforms to the official FileMaker XSD schemas before delivery.

## Critical Rule: Always Validate

**ALWAYS** validate SAXML before delivering it to the user:

1. **Generating new SAXML** — validate against the schema BEFORE showing it
2. **Editing existing SAXML** — validate the modified XML after changes
3. **User-provided SAXML** — validate first to identify issues before working on it

Never deliver unvalidated FileMaker XML. If validation fails, fix and re-validate until it passes.

---

## Two XML Format Families

### Format 1: `fmxmlsnippet` (SAXML)

**Used for**: Scripts, Fields, Tables, Layouts, Themes, Custom Functions, Value Lists

**Encoding**: UTF-8

**Root element**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<fmxmlsnippet type="FMObjectList">
  <!-- objects here -->
</fmxmlsnippet>
```

**Schema**: `saxml-22.0.4.xsd`

### Format 2: `FMObjectTransfer`

**Used for**: Custom Menus, Custom Menu Sets ONLY

**Encoding**: UTF-16

**Root element**:
```xml
<?xml version="1.0" encoding="UTF-16"?>
<FMObjectTransfer version="1" membercount="N" Source="21.0.2" File="DbName" UUID="..." locale="en_US" timestamp="...">
  <!-- catalog structure here -->
</FMObjectTransfer>
```

**Schema**: `fmobjecttransfer-22.0.4.xsd`

---

## Validation

```bash
# Detect format type
head -n 5 file.xml | grep -E "(fmxmlsnippet|FMObjectTransfer)"

# Validate fmxmlsnippet
xmllint --noout --schema saxml-22.0.4.xsd file.xml

# Validate FMObjectTransfer
xmllint --noout --schema fmobjecttransfer-22.0.4.xsd file.xml
```

---

## Common Errors and Fixes

### 1. Wrong root element
Custom menus MUST use `FMObjectTransfer`. Everything else uses `fmxmlsnippet`.

### 2. Missing required attribute on `<fmxmlsnippet>`
```xml
<!-- WRONG -->  <fmxmlsnippet>
<!-- CORRECT --> <fmxmlsnippet type="FMObjectList">
```

### 3. Incomplete Field definition
Every `<Field>` MUST have `<AutoEnter>`, `<Validation>`, and `<Storage>` children:
```xml
<Field id="1" dataType="Text" fieldType="Normal" name="CustomerName">
  <AutoEnter allowEditing="True" constant="False" furigana="False" lookup="False" calculation="False">
    <ConstantData></ConstantData>
  </AutoEnter>
  <Validation message="False" maxLength="False" valuelist="False" calculation="False" alwaysValidateCalculation="False" type="OnlyDuringDataEntry">
  </Validation>
  <Storage autoIndex="True" index="None" indexLanguage="English" global="False" maxRepetition="1">
  </Storage>
</Field>
```

### 4. Wrong boolean capitalization
```xml
<!-- WRONG -->   allowEditing="true"
<!-- CORRECT --> allowEditing="True"
```

### 5. Calculations without CDATA
```xml
<!-- WRONG -->   <Calculation>field1 & " " & field2</Calculation>
<!-- CORRECT --> <Calculation><![CDATA[field1 & " " & field2]]></Calculation>
```

### 6. Wrong encoding
- `fmxmlsnippet` → `encoding="UTF-8"`
- `FMObjectTransfer` → `encoding="UTF-16"`

---

## Valid Attribute Values

**dataType**: `Text` | `Number` | `Date` | `Time` | `Timestamp` | `Binary`

**fieldType**: `Normal` | `Calculated` | `Summary`

**index**: `None` | `All` | `Some` | `Minimal`

---

## Workflow

### Building new XML
1. Ask: what object type? (Script, Field, Table, Layout, Custom Function, Value List, Custom Menu)
2. Use the appropriate template from [references/REFERENCE.md](./references/REFERENCE.md)
3. Generate complete XML with all required child elements
4. Validate against schema — fix any errors, repeat until clean
5. Deliver with "✓ Validated against FileMaker SAXML schema"

### Fixing user-provided XML
1. Identify format type from root element
2. Run `xmllint` validation
3. Parse errors, explain them in plain language
4. Apply fixes — validate again until clean

---

## Reference Files

Load these on demand as needed:

- [references/REFERENCE.md](./references/REFERENCE.md) — Full object-type templates, workflow detail, schema paths
- [references/QUICK_REFERENCE.md](./references/QUICK_REFERENCE.md) — Decision tree, checklists, error table
- [examples/](./examples/) — Real broken/fixed XML pairs for each error type

---

## Success Criteria

- XML validates against the appropriate XSD schema without errors
- All required elements and attributes are present
- Attribute values match allowed enums
- Correct encoding (UTF-8 or UTF-16)
- Structure matches FileMaker's expected format exactly
