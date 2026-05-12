# FileMaker SAXML Quick Reference

**Author**: Francesc Sans <fsans@ntwk.es> | Barcelona, 2025 | Version 0.0.27

---

## Format Decision Tree

```
Is it a Custom Menu or Menu Set?
├─ YES → Use FMObjectTransfer format (UTF-16, fmobjecttransfer-22.0.4.xsd)
└─ NO  → Use fmxmlsnippet format (UTF-8, saxml-22.0.4.xsd)
```

## Validation Commands

```bash
# fmxmlsnippet format
xmllint --noout --schema /path/to/saxml-22.0.4.xsd file.xml

# FMObjectTransfer format
xmllint --noout --schema /path/to/fmobjecttransfer-22.0.4.xsd file.xml
```

## Required Root Structures

### fmxmlsnippet Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<fmxmlsnippet type="FMObjectList">
  <!-- objects here -->
</fmxmlsnippet>
```

### FMObjectTransfer Format
```xml
<?xml version="1.0" encoding="UTF-16"?>
<FMObjectTransfer version="1" membercount="N" Source="21.0.2" File="DbName" UUID="..." locale="en_US" timestamp="...">
  <!-- catalog structure here -->
</FMObjectTransfer>
```

## Field Definition Checklist

```xml
<Field id="N" dataType="Type" fieldType="Type" name="Name">
  ✓ <AutoEnter allowEditing="True/False" constant="True/False" furigana="True/False" lookup="True/False" calculation="True/False">
      ✓ <ConstantData></ConstantData>
    </AutoEnter>
  ✓ <Validation message="True/False" maxLength="True/False" valuelist="True/False" calculation="True/False" alwaysValidateCalculation="True/False" type="Type">
    </Validation>
  ✓ <Storage autoIndex="True/False" index="None|All|Some|Minimal" indexLanguage="Language" global="True/False" maxRepetition="N">
    </Storage>
</Field>
```

## Valid Attribute Values

### dataType
- `Text`
- `Number`
- `Date`
- `Time`
- `Timestamp`
- `Binary`

### fieldType
- `Normal`
- `Calculated`
- `Summary`

### index
- `None`
- `All`
- `Some`
- `Minimal`

### Boolean Values
**ALWAYS** use capitalized: `True` or `False` (NOT "true" or "false")

## Calculation Rules

```xml
<!-- WRONG: No CDATA -->
<Calculation>field1 & " " & field2</Calculation>

<!-- CORRECT: With CDATA -->
<Calculation><![CDATA[field1 & " " & field2]]></Calculation>
```

## Common Object Templates

### Text Field
```xml
<Field id="1" dataType="Text" fieldType="Normal" name="FieldName">
  <AutoEnter allowEditing="True" constant="False" furigana="False" lookup="False" calculation="False">
    <ConstantData></ConstantData>
  </AutoEnter>
  <Validation message="False" maxLength="False" valuelist="False" calculation="False" alwaysValidateCalculation="False" type="OnlyDuringDataEntry">
  </Validation>
  <Storage autoIndex="True" index="None" indexLanguage="English" global="False" maxRepetition="1">
  </Storage>
</Field>
```

### Number Field
```xml
<Field id="2" dataType="Number" fieldType="Normal" name="Amount">
  <AutoEnter allowEditing="True" constant="False" furigana="False" lookup="False" calculation="False">
    <ConstantData></ConstantData>
  </AutoEnter>
  <Validation message="False" maxLength="False" valuelist="False" calculation="False" alwaysValidateCalculation="False" type="OnlyDuringDataEntry">
  </Validation>
  <Storage autoIndex="True" index="None" indexLanguage="English" global="False" maxRepetition="1">
  </Storage>
</Field>
```

### Calculated Field
```xml
<Field id="3" dataType="Text" fieldType="Calculated" name="FullName">
  <AutoEnter allowEditing="False" constant="False" furigana="False" lookup="False" calculation="True">
    <Calculation><![CDATA[FirstName & " " & LastName]]></Calculation>
  </AutoEnter>
  <Validation message="False" maxLength="False" valuelist="False" calculation="False" alwaysValidateCalculation="False" type="OnlyDuringDataEntry">
  </Validation>
  <Storage autoIndex="True" index="None" indexLanguage="English" global="False" maxRepetition="1">
  </Storage>
</Field>
```

### Custom Function
```xml
<CustomFunction functionArity="2" id="1" name="FunctionName" parameters="param1;param2" visible="True">
  <Calculation><![CDATA[param1 & " " & param2]]></Calculation>
</CustomFunction>
```

### Value List (Custom)
```xml
<ValueList id="1" name="ListName">
  <Source type="custom">
    <CustomValues>
      <text>Value 1</text>
      <text>Value 2</text>
      <text>Value 3</text>
    </CustomValues>
  </Source>
</ValueList>
```

### Value List (Field-based)
```xml
<ValueList id="2" name="FieldBasedList">
  <Source type="field">
    <PrimaryField table="TableName" name="FieldName"/>
  </Source>
</ValueList>
```

### Script
```xml
<Script id="1" name="ScriptName" include="True">
  <Step index="1" id="68" name="Set Field">
    <Field table="TableName" name="FieldName"/>
    <Calculation><![CDATA["Value"]]></Calculation>
  </Step>
</Script>
```

### Script Step
```xml
<Step index="1" id="68" name="Set Field">
  <Field table="TableName" name="FieldName"/>
  <Calculation><![CDATA["Value"]]></Calculation>
</Step>
```

### Base Table
```xml
<BaseTable id="1" name="TableName">
  <!-- Fields go here -->
</BaseTable>
```

## Encoding Reminder

| Format | Encoding |
|--------|----------|
| fmxmlsnippet | UTF-8 |
| FMObjectTransfer | UTF-16 |

## Error Quick Fixes

| Error Message | Quick Fix |
|---------------|-----------|
| Element 'fmxmlsnippet': Missing child element | Add missing required child elements |
| The attribute 'type' is required | Add `type="FMObjectList"` to fmxmlsnippet |
| The attribute 'dataType' is required | Add `dataType="Text"` (or Number, Date, etc.) |
| Invalid attribute value | Check against valid values list above |
| This element is not expected | Check element nesting/order |
| parser error : EntityRef: expecting ';' | Wrap calculation in CDATA |

## File Extensions

FileMaker XML snippets typically use:
- `.xml` - Standard XML extension
- `.fmxmlsnippet` - FileMaker-specific extension (rare)

Both are valid, `.xml` is more common.
