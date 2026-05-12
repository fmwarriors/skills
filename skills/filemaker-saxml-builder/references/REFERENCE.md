# FileMaker SAXML Builder & Validator — Full Reference

> Detailed reference for the `filemaker-saxml-builder` skill. Load this file when you need complete
> object-type templates, full workflow detail, or schema path information.

**Author**: Francesc Sans <fsans@ntwk.es> | Barcelona, 2025 | Version 1.0

> **Note on schema paths**: The XSD schema files (`saxml-22.0.4.xsd`, `fmobjecttransfer-22.0.4.xsd`)
> are not bundled in this repository. Place them in a known directory and adjust paths in validation
> commands accordingly. They can be exported from FileMaker Pro or obtained from Claris documentation.

---

This reference provides complete instructions for building, validating, healing, and fixing FileMaker XML (SAXML) format files, ensuring XML snippets conform to the proper schemas and format specifications.

## ⚠️ CRITICAL: Automatic Quality Assurance

**ALWAYS** validate SAXML before delivering it to the user:

1. **When generating new SAXML** - After writing FileMaker XML, automatically validate it against the schema BEFORE showing it to the user
2. **When editing existing SAXML** - After making changes, automatically validate the modified XML
3. **When user provides SAXML** - When user asks you to work with FileMaker XML, validate it first to identify issues

This is NOT optional - SAXML validation MUST happen automatically for every FileMaker XML operation. If validation fails, fix the errors and validate again until it passes.

**Never deliver unvalidated FileMaker XML to the user.**

## Your Responsibilities

1. **Identify the correct XML format** (fmxmlsnippet vs FMObjectTransfer)
2. **Validate XML** against the appropriate XSD schema
3. **Detect and fix common errors** in FileMaker XML
4. **Guide proper SAXML generation** from scratch
5. **Heal malformed XML** to match FileMaker's requirements

## Two XML Format Families

### Format 1: `fmxmlsnippet` (SAXML)
**Schema**: `saxml-22.0.4.xsd`

**Used by**: Scripts, Fields, Tables, Layouts, Themes, Custom Functions, Value Lists

**Root element**: `<fmxmlsnippet type="FMObjectList">`

**Example structure**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<fmxmlsnippet type="FMObjectList">
  <Field id="1" dataType="Text" fieldType="Normal" name="CustomerName">
    <AutoEnter allowEditing="True" constant="False" furigana="False" lookup="False" calculation="False">
      <ConstantData></ConstantData>
    </AutoEnter>
    <Validation message="False" maxLength="False" valuelist="False" calculation="False" alwaysValidateCalculation="False" type="OnlyDuringDataEntry">
    </Validation>
    <Storage autoIndex="True" index="None" indexLanguage="English" global="False" maxRepetition="1">
    </Storage>
  </Field>
</fmxmlsnippet>
```

### Format 2: `FMObjectTransfer`
**Schema**: `fmobjecttransfer-22.0.4.xsd`

**Used by**: Custom Menus, Custom Menu Sets

**Root element**: `<FMObjectTransfer>`

**Example structure**:
```xml
<?xml version="1.0" encoding="UTF-16"?>
<FMObjectTransfer version="1" membercount="1" Source="21.0.2" File="MyDatabase" UUID="..." locale="en_US" timestamp="...">
  <CustomMenuSetCatalog membercount="1">
    <UUID modifications="3" userName="admin" accountName="admin" timestamp="...">...</UUID>
    <TagList></TagList>
    <CustomMenuSetReference id="2" name="Custom Menu Set" UUID="..."/>
    <ObjectList membercount="1">
      <CustomMenuSet id="2" name="Custom Menu Set" UUID="...">
        <!-- menu content -->
      </CustomMenuSet>
    </ObjectList>
  </CustomMenuSetCatalog>
  <PasteIndexList membercount="1">
    <Object id="2"/>
  </PasteIndexList>
</FMObjectTransfer>
```

## Validation Process

### Step 1: Determine Format Type

Check the root element:
```bash
# Check format type
head -n 5 file.xml | grep -E "(fmxmlsnippet|FMObjectTransfer)"
```

### Step 2: Validate Against Schema

```bash
# For fmxmlsnippet format (scripts, fields, tables, layouts, themes, functions, value lists)
xmllint --noout --schema <path-to-schemas>/saxml-22.0.4.xsd file.xml

# For FMObjectTransfer format (custom menus)
xmllint --noout --schema <path-to-schemas>/fmobjecttransfer-22.0.4.xsd file.xml
```

### Step 3: Parse Validation Errors

Common xmllint error patterns:
- `element X: Schemas validity error : Element 'Y': This element is not expected.`
- `attribute 'Z' is required but missing`
- `Invalid attribute value`

## Common Errors and Fixes

### Error 1: Wrong Root Element
**Problem**: Using `<fmxmlsnippet>` for custom menus or vice versa

**Fix**:
- Custom menus MUST use `<FMObjectTransfer>` format
- All other objects use `<fmxmlsnippet>` format

### Error 2: Missing Required Attributes

#### For `<fmxmlsnippet>`:
```xml
<!-- WRONG -->
<fmxmlsnippet>

<!-- CORRECT -->
<fmxmlsnippet type="FMObjectList">
```

#### For Field definitions:
```xml
<!-- WRONG -->
<Field name="MyField">

<!-- CORRECT -->
<Field id="1" dataType="Text" fieldType="Normal" name="MyField">
```

### Error 3: Missing Required Child Elements

#### For Field definitions:
Every `<Field>` MUST have:
- `<AutoEnter>` with attributes and `<ConstantData>`
- `<Validation>` with attributes
- `<Storage>` with attributes

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

### Error 4: Incorrect Encoding

#### For fmxmlsnippet:
```xml
<?xml version="1.0" encoding="UTF-8"?>
```

#### For FMObjectTransfer:
```xml
<?xml version="1.0" encoding="UTF-16"?>
```

### Error 5: Invalid Attribute Values

**dataType** must be one of:
- `Text`
- `Number`
- `Date`
- `Time`
- `Timestamp`
- `Binary`

**fieldType** must be one of:
- `Normal`
- `Calculated`
- `Summary`

**index** must be one of:
- `None`
- `All`
- `Some`
- `Minimal`

### Error 6: CDATA for Calculations

Calculations with special characters MUST use CDATA:

```xml
<!-- WRONG -->
<Calculation>field1 > 10 & field2 < 5</Calculation>

<!-- CORRECT -->
<Calculation><![CDATA[field1 > 10 & field2 < 5]]></Calculation>
```

### Error 7: Boolean Attributes

FileMaker uses string "True" and "False" (capitalized):

```xml
<!-- WRONG -->
<AutoEnter allowEditing="true" constant="false">

<!-- CORRECT -->
<AutoEnter allowEditing="True" constant="False">
```

## Object Type Reference

### Scripts
```xml
<fmxmlsnippet type="FMObjectList">
  <Script id="1" name="My Script" include="True">
    <Step index="1" id="68" name="Set Field">
      <Field table="Contacts" name="Status"/>
      <Calculation><![CDATA["Active"]]></Calculation>
    </Step>
  </Script>
</fmxmlsnippet>
```

### Field Definitions
```xml
<fmxmlsnippet type="FMObjectList">
  <Field id="1" dataType="Text" fieldType="Normal" name="FirstName">
    <AutoEnter allowEditing="True" constant="False" furigana="False" lookup="False" calculation="False">
      <ConstantData></ConstantData>
    </AutoEnter>
    <Validation message="False" maxLength="False" valuelist="False" calculation="False" alwaysValidateCalculation="False" type="OnlyDuringDataEntry">
    </Validation>
    <Storage autoIndex="True" index="None" indexLanguage="English" global="False" maxRepetition="1">
    </Storage>
  </Field>
</fmxmlsnippet>
```

### Base Table with Fields
```xml
<fmxmlsnippet type="FMObjectList">
  <BaseTable id="1" name="Contacts">
    <Field id="1" dataType="Text" fieldType="Normal" name="FirstName">
      <AutoEnter allowEditing="True" constant="False" furigana="False" lookup="False" calculation="False">
        <ConstantData></ConstantData>
      </AutoEnter>
      <Validation message="False" maxLength="False" valuelist="False" calculation="False" alwaysValidateCalculation="False" type="OnlyDuringDataEntry">
      </Validation>
      <Storage autoIndex="True" index="None" indexLanguage="English" global="False" maxRepetition="1">
      </Storage>
    </Field>
  </BaseTable>
</fmxmlsnippet>
```

### Custom Function
```xml
<fmxmlsnippet type="FMObjectList">
  <CustomFunction functionArity="2" id="1" name="FullName" parameters="firstName;lastName" visible="True">
    <Calculation><![CDATA[firstName & " " & lastName]]></Calculation>
  </CustomFunction>
</fmxmlsnippet>
```

### Value List
```xml
<fmxmlsnippet type="FMObjectList">
  <ValueList id="1" name="Status">
    <Source type="custom">
      <CustomValues>
        <text>Active</text>
        <text>Inactive</text>
        <text>Pending</text>
      </CustomValues>
    </Source>
  </ValueList>
</fmxmlsnippet>
```

### Layout Object
```xml
<fmxmlsnippet type="FMObjectList">
  <Layout enclosingRectTop="0" enclosingRectLeft="0" enclosingRectBottom="100" enclosingRectRight="200">
    <Object type="Button" name="MyButton">
      <Bounds top="10" left="10" bottom="40" right="110"/>
      <TextObj>
        <Font-family platform="mac" familyId="1" face="0" characterSet="0" name="Arial"/>
        <Font-size pointSize="12"/>
        <text>Click Me</text>
      </TextObj>
      <ButtonObj>
        <Step index="1" id="68" name="Set Field">
          <Field table="Contacts" name="Status"/>
          <Calculation><![CDATA["Active"]]></Calculation>
        </Step>
      </ButtonObj>
    </Object>
  </Layout>
</fmxmlsnippet>
```

### Custom Menu
```xml
<?xml version="1.0" encoding="UTF-16"?>
<FMObjectTransfer version="1" membercount="1" Source="21.0.2" File="MyDatabase" UUID="..." locale="en_US" timestamp="2024-01-01T12:00:00">
  <CustomMenuSetCatalog membercount="1">
    <UUID modifications="3" userName="admin" accountName="admin" timestamp="2024-01-01T12:00:00">12345678-1234-1234-1234-123456789012</UUID>
    <TagList></TagList>
    <CustomMenuSetReference id="2" name="My Menu Set" UUID="12345678-1234-1234-1234-123456789012"/>
    <ObjectList membercount="1">
      <CustomMenuSet id="2" name="My Menu Set" UUID="12345678-1234-1234-1234-123456789012">
        <CustomMenuList membercount="1">
          <CustomMenuReference id="1" name="File" source="standard"/>
        </CustomMenuList>
      </CustomMenuSet>
    </ObjectList>
  </CustomMenuSetCatalog>
  <PasteIndexList membercount="1">
    <Object id="2"/>
  </PasteIndexList>
</FMObjectTransfer>
```

## Your Workflow

### AUTOMATIC MODE (Proactive Validation):

**This is the default mode.** Whenever you generate or modify FileMaker XML:

1. **Write/Edit the XML file** using Write or Edit tool
2. **Immediately validate** using the validation script (don't wait for user to ask)
3. **If validation fails**:
   - Fix the errors automatically
   - Validate again
   - Repeat until validation succeeds
4. **Only then** show the result to the user
5. **Inform the user**: "✓ Validated against FileMaker SAXML schema"

**Example flow**:
```
User: "Create a text field called CustomerName"
You:
  → Write the XML file
  → Run validation script
  → (If errors found) Fix them
  → Run validation again
  → (Validation passes) ✓
  → Show user: "Created CustomerName field (validated ✓)"
```

### When User Provides XML to Validate/Fix:

1. **Read the XML file**
   ```
   Read tool: /path/to/file.xml
   ```

2. **Identify format type** by checking root element
   - `<fmxmlsnippet>` → Use saxml-22.0.4.xsd
   - `<FMObjectTransfer>` → Use fmobjecttransfer-22.0.4.xsd

3. **Validate against schema**
   ```bash
   xmllint --noout --schema <path-to-schemas>/saxml-22.0.4.xsd file.xml
   ```

4. **If validation fails**:
   - Parse the error messages
   - Identify the specific issues
   - Explain what's wrong in user-friendly terms
   - Provide corrected XML using Edit or Write tool

5. **If validation succeeds**:
   - Confirm the XML is valid
   - Optionally suggest improvements (if any)

### When User Asks to Build New XML:

1. **Ask clarifying questions**:
   - What FileMaker object type? (Script, Field, Table, Layout, Custom Function, Value List, Custom Menu)
   - What specific properties/attributes?
   - Any special requirements?

2. **Use appropriate template** from Object Type Reference above

3. **Generate complete XML** with:
   - Correct root element and attributes
   - Proper encoding declaration
   - All required child elements
   - Valid attribute values
   - CDATA where needed

4. **Validate the generated XML** against schema

5. **Write to file** using Write tool

## Reference Files

### XSD Schemas:
- Main SAXML schema: `saxml-22.0.4.xsd` (place in a known directory, adjust paths as needed)
- FMObjectTransfer schema: `fmobjecttransfer-22.0.4.xsd`

### Example Files:
- See the `examples/` directory in this skill for broken/fixed XML pairs covering the most common errors.

### Spec:
- See [agentskills.io/specification](https://agentskills.io/specification) for the Agent Skills format standard.

## Key Principles

1. **Always validate** - Never assume XML is correct without validation
2. **Use correct format** - fmxmlsnippet vs FMObjectTransfer based on object type
3. **Complete structures** - FileMaker requires all child elements even if empty
4. **Proper encoding** - UTF-8 for fmxmlsnippet, UTF-16 for FMObjectTransfer
5. **Boolean capitalization** - "True" and "False" not "true" and "false"
6. **CDATA for formulas** - Wrap calculations in CDATA sections
7. **Refer to samples** - Check samples/ directory for real-world examples

## Example Interaction

**User**: "Fix this FileMaker field XML - it's not validating"

**You**:
1. Read the provided XML file
2. Run xmllint validation
3. If errors found:
   - "I found 3 validation errors in your Field definition:
     1. Missing required `dataType` attribute on `<Field>` element
     2. Missing required `<Storage>` child element
     3. Boolean value 'true' should be 'True' (capitalized)

     Let me fix these issues..."
4. Edit the file with corrections
5. Validate again to confirm
6. "Fixed! The XML now validates correctly against the SAXML schema."

## Success Criteria

Your response is successful when:
- ✅ XML validates against appropriate XSD schema without errors
- ✅ All required elements and attributes are present
- ✅ Attribute values match allowed types/enums
- ✅ Proper encoding is used (UTF-8 or UTF-16)
- ✅ Structure matches FileMaker's format exactly
- ✅ User understands what was wrong and why it was fixed
