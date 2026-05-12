#!/usr/bin/env python3
"""
FileMaker SVG Validator
Validates SVG files against the FileMaker Pro 14 SVG Grammar specification.
"""

import xml.etree.ElementTree as ET
import re
import sys
from pathlib import Path


class FileMakerSVGValidator:
    """Validates SVG files against FileMaker Pro 14 SVG Grammar specification."""

    SVG_NS = "http://www.w3.org/2000/svg"
    XLINK_NS = "http://www.w3.org/1999/xlink"

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_file(self, filepath):
        """Validate an SVG file and return results."""
        self.errors = []
        self.warnings = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            self.errors.append("File must use UTF-8 encoding (UTF-16 not supported)")
            return False
        except FileNotFoundError:
            self.errors.append(f"File not found: {filepath}")
            return False

        # Check XML declaration
        self._check_xml_declaration(content)

        # Parse XML
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            self.errors.append(f"XML parsing error: {e}")
            return False

        # Validate root element
        self._check_root_element(root)

        # Validate all elements recursively
        self._validate_element(root)

        return len(self.errors) == 0

    def _check_xml_declaration(self, content):
        """Check for proper XML declaration."""
        if not content.startswith('<?xml'):
            self.errors.append("Missing XML declaration: must start with <?xml version=\"1.0\" encoding=\"utf-8\"?>")
        elif 'encoding="utf-8"' not in content.split('\n')[0].lower():
            self.errors.append("XML declaration must specify encoding=\"utf-8\"")

    def _check_root_element(self, root):
        """Validate root SVG element requirements."""
        # Remove namespace from tag for comparison
        tag = root.tag.replace(f"{{{self.SVG_NS}}}", "")

        if tag != 'svg':
            self.errors.append(f"Root element must be <svg>, found <{tag}>")
            return

        # Check namespace declarations
        if root.get('{http://www.w3.org/2000/xmlns/}xmlns') != self.SVG_NS and \
           root.tag != f"{{{self.SVG_NS}}}svg":
            self.errors.append(f"Missing xmlns=\"{self.SVG_NS}\" on root <svg> element")

        # Check for xlink namespace (optional but common)
        xlink_attr = root.get('{http://www.w3.org/2000/xmlns/}xlink')
        if xlink_attr and xlink_attr != self.XLINK_NS:
            self.errors.append(f"xmlns:xlink must be \"{self.XLINK_NS}\" if present")

        # Check required width and height
        if 'width' not in root.attrib:
            self.errors.append("Root <svg> element must have 'width' attribute")
        if 'height' not in root.attrib:
            self.errors.append("Root <svg> element must have 'height' attribute")

        # Check width and height values
        if 'width' in root.attrib:
            self._check_coordinate_value(root.get('width'), 'width', allow_negative=False)
        if 'height' in root.attrib:
            self._check_coordinate_value(root.get('height'), 'height', allow_negative=False)

        # Check if <defs> is first child (if present)
        children = list(root)
        if children:
            first_child_tag = children[0].tag.replace(f"{{{self.SVG_NS}}}", "")
            has_defs = any(child.tag.replace(f"{{{self.SVG_NS}}}", "") == 'defs' for child in children)
            if has_defs and first_child_tag != 'defs':
                self.warnings.append("<defs> should be the first child of root <svg> element")

    def _validate_element(self, element):
        """Recursively validate SVG element and its children."""
        tag = element.tag.replace(f"{{{self.SVG_NS}}}", "")

        # Validate element-specific requirements
        if tag == 'circle':
            self._validate_circle(element)
        elif tag == 'ellipse':
            self._validate_ellipse(element)
        elif tag == 'rect':
            self._validate_rect(element)
        elif tag == 'line':
            self._validate_line(element)
        elif tag == 'polyline' or tag == 'polygon':
            self._validate_poly(element, tag)
        elif tag == 'linearGradient':
            self._validate_linear_gradient(element)
        elif tag == 'radialGradient':
            self._validate_radial_gradient(element)

        # Check all coordinate attributes for units
        self._check_coordinate_attributes(element)

        # Recursively validate children
        for child in element:
            self._validate_element(child)

    def _validate_circle(self, element):
        """Validate circle element."""
        if 'r' in element.attrib:
            r_value = element.get('r')
            try:
                r = float(r_value)
                if r < 0:
                    self.errors.append(f"<circle> radius 'r' must be ≥ 0, found: {r_value}")
            except ValueError:
                self.errors.append(f"<circle> radius 'r' must be a number, found: {r_value}")

    def _validate_ellipse(self, element):
        """Validate ellipse element."""
        for attr in ['rx', 'ry']:
            if attr in element.attrib:
                value = element.get(attr)
                try:
                    num = float(value)
                    if num < 0:
                        self.errors.append(f"<ellipse> radius '{attr}' must be ≥ 0, found: {value}")
                except ValueError:
                    self.errors.append(f"<ellipse> radius '{attr}' must be a number, found: {value}")

    def _validate_rect(self, element):
        """Validate rect element."""
        for attr in ['rx', 'ry']:
            if attr in element.attrib:
                value = element.get(attr)
                try:
                    num = float(value)
                    if num < 0:
                        self.errors.append(f"<rect> corner radius '{attr}' must be ≥ 0, found: {value}")
                except ValueError:
                    self.errors.append(f"<rect> corner radius '{attr}' must be a number, found: {value}")

        # Check width and height
        for attr in ['width', 'height']:
            if attr in element.attrib:
                value = element.get(attr)
                try:
                    num = float(value)
                    if num < 0:
                        self.errors.append(f"<rect> '{attr}' must be ≥ 0, found: {value}")
                except ValueError:
                    self.errors.append(f"<rect> '{attr}' must be a number, found: {value}")

    def _validate_line(self, element):
        """Validate line element."""
        required_attrs = ['x1', 'y1', 'x2', 'y2']
        for attr in required_attrs:
            if attr not in element.attrib:
                self.errors.append(f"<line> missing required attribute '{attr}'")

    def _validate_poly(self, element, tag):
        """Validate polyline or polygon element."""
        if 'points' not in element.attrib:
            self.errors.append(f"<{tag}> missing required 'points' attribute")
            return

        points_str = element.get('points').strip()
        # Split by whitespace or commas
        coords = re.split(r'[\s,]+', points_str)
        # Filter out empty strings
        coords = [c for c in coords if c]

        if len(coords) % 2 != 0:
            self.errors.append(f"<{tag}> 'points' must have even number of coordinates, found {len(coords)}")

    def _validate_linear_gradient(self, element):
        """Validate linearGradient element."""
        if 'id' not in element.attrib:
            self.warnings.append("<linearGradient> should have 'id' attribute for referencing")

    def _validate_radial_gradient(self, element):
        """Validate radialGradient element."""
        if 'id' not in element.attrib:
            self.warnings.append("<radialGradient> should have 'id' attribute for referencing")

        if 'r' in element.attrib:
            r_value = element.get('r')
            # Check if it's a percentage
            if not r_value.endswith('%'):
                try:
                    r = float(r_value)
                    if r < 0:
                        self.errors.append(f"<radialGradient> radius 'r' must be ≥ 0, found: {r_value}")
                except ValueError:
                    pass  # Might be percentage format

    def _check_coordinate_attributes(self, element):
        """Check coordinate attributes for unit symbols."""
        coordinate_attrs = ['x', 'y', 'x1', 'y1', 'x2', 'y2', 'cx', 'cy',
                          'width', 'height', 'r', 'rx', 'ry']

        for attr in coordinate_attrs:
            if attr in element.attrib:
                value = element.get(attr)
                self._check_coordinate_value(value, attr)

    def _check_coordinate_value(self, value, attr_name, allow_negative=True):
        """Check if coordinate value has forbidden unit symbols."""
        if not value:
            return

        # Skip percentage values (allowed for gradients)
        if value.endswith('%'):
            return

        # Check for unit symbols
        unit_pattern = r'(px|pt|pc|cm|mm|in|em|ex|rem)$'
        if re.search(unit_pattern, value.lower()):
            self.errors.append(
                f"Attribute '{attr_name}' has unit symbol in value '{value}'. "
                f"Only user coordinate units allowed (no px, pt, etc.)"
            )

    def get_results(self):
        """Return validation results."""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings
        }

    def print_results(self):
        """Print validation results to console."""
        if self.errors:
            print("\n❌ VALIDATION ERRORS:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ SVG is valid according to FileMaker Pro 14 SVG Grammar!")
        elif not self.errors:
            print("\n✅ SVG is valid (with warnings)")
        else:
            print(f"\n❌ Validation failed with {len(self.errors)} error(s)")


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python validate_filemaker_svg.py <svg-file>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Validating: {filepath}")
    print("=" * 60)

    validator = FileMakerSVGValidator()
    is_valid = validator.validate_file(filepath)
    validator.print_results()

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
