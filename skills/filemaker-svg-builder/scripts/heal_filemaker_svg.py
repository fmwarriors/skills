#!/usr/bin/env python3
"""
FileMaker SVG Healer
Automatically fixes SVG files to make them FileMaker Pro 14 SVG Grammar compliant.
"""

import xml.etree.ElementTree as ET
import re
import sys
import math
from pathlib import Path


class FileMakerSVGHealer:
    """Heals/fixes SVG files to be FileMaker-compatible."""

    SVG_NS = "http://www.w3.org/2000/svg"
    XLINK_NS = "http://www.w3.org/1999/xlink"

    def __init__(self):
        self.fixes_applied = []
        self.warnings = []

    def heal_file(self, input_path, output_path=None):
        """
        Heal an SVG file to be FileMaker-compatible.
        If output_path is None, overwrites the input file.
        """
        self.fixes_applied = []
        self.warnings = []

        # Read the file
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try to read with different encoding and convert to UTF-8
            try:
                with open(input_path, 'r', encoding='utf-16') as f:
                    content = f.read()
                self.fixes_applied.append("Converted from UTF-16 to UTF-8 encoding")
            except:
                self.fixes_applied.append("ERROR: Could not read file with UTF-8 or UTF-16 encoding")
                return False

        # Fix XML declaration
        content = self._fix_xml_declaration(content)

        # Parse the XML
        try:
            # Register namespaces to preserve them
            ET.register_namespace('', self.SVG_NS)
            ET.register_namespace('xlink', self.XLINK_NS)

            tree = ET.parse(input_path)
            root = tree.getroot()
        except ET.ParseError as e:
            self.fixes_applied.append(f"ERROR: Cannot parse XML: {e}")
            return False

        # Apply fixes
        self._fix_root_element(root)
        self._fix_elements_recursively(root)

        # Write the fixed file
        output_path = output_path or input_path
        try:
            # Write with proper XML declaration
            with open(output_path, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
                tree.write(f, encoding='utf-8', xml_declaration=False)

            return True
        except Exception as e:
            self.fixes_applied.append(f"ERROR: Could not write file: {e}")
            return False

    def _fix_xml_declaration(self, content):
        """Ensure proper XML declaration."""
        lines = content.split('\n')

        if not lines[0].startswith('<?xml'):
            self.fixes_applied.append("Added missing XML declaration")
            return '<?xml version="1.0" encoding="utf-8"?>\n' + content

        if 'encoding="utf-8"' not in lines[0].lower():
            # Replace the first line with proper declaration
            lines[0] = '<?xml version="1.0" encoding="utf-8"?>'
            self.fixes_applied.append("Fixed XML declaration encoding to UTF-8")
            return '\n'.join(lines)

        return content

    def _fix_root_element(self, root):
        """Fix root SVG element issues."""

        # Ensure it's an SVG element
        if not root.tag.endswith('svg'):
            self.warnings.append(f"Root element is not <svg>, found: {root.tag}")
            return

        # Add xmlns if missing
        if root.tag != f"{{{self.SVG_NS}}}svg":
            root.set('xmlns', self.SVG_NS)
            self.fixes_applied.append(f"Added xmlns=\"{self.SVG_NS}\"")

        # Note: xmlns:xlink will be handled by ET.register_namespace() at the top
        # ElementTree automatically includes it when xlink:href is used

        # Add width and height if missing
        if 'width' not in root.attrib:
            width = self._extract_dimension_from_viewbox(root, 'width')
            if width:
                root.set('width', str(width))
                self.fixes_applied.append(f"Added width=\"{width}\" (extracted from viewBox)")
            else:
                root.set('width', '100')
                self.fixes_applied.append("Added default width=\"100\" (no viewBox found)")

        if 'height' not in root.attrib:
            height = self._extract_dimension_from_viewbox(root, 'height')
            if height:
                root.set('height', str(height))
                self.fixes_applied.append(f"Added height=\"{height}\" (extracted from viewBox)")
            else:
                root.set('height', '100')
                self.fixes_applied.append("Added default height=\"100\" (no viewBox found)")

        # Fix width and height if they have units
        for attr in ['width', 'height']:
            if attr in root.attrib:
                old_value = root.get(attr)
                new_value = self._remove_units(old_value)
                if new_value != old_value:
                    root.set(attr, new_value)
                    self.fixes_applied.append(f"Removed units from {attr}: \"{old_value}\" → \"{new_value}\"")

        # Remove fill attribute from root SVG element
        # FileMaker wraps content in <g class="fm_fill">, so root svg should not have fill
        if 'fill' in root.attrib:
            del root.attrib['fill']
            self.fixes_applied.append("Removed fill attribute from root <svg> element (FileMaker adds fm_fill wrapper)")

    def _extract_dimension_from_viewbox(self, root, dimension):
        """Extract width or height from viewBox attribute."""
        viewbox = root.get('viewBox')
        if not viewbox:
            return None

        parts = viewbox.split()
        if len(parts) == 4:
            if dimension == 'width':
                return parts[2]
            elif dimension == 'height':
                return parts[3]

        return None

    def _fix_elements_recursively(self, element):
        """Fix all elements recursively."""

        tag = element.tag.replace(f"{{{self.SVG_NS}}}", "")

        # Fix element-specific issues
        if tag == 'circle':
            self._fix_circle(element)
        elif tag == 'ellipse':
            self._fix_ellipse(element)
        elif tag == 'rect':
            self._fix_rect(element)
        elif tag == 'polyline' or tag == 'polygon':
            self._fix_poly(element, tag)
        elif tag == 'path':
            self._fix_path(element)

        # Fix coordinate attributes
        self._fix_coordinate_attributes(element)

        # Fix transform attribute (degrees to radians)
        self._fix_transform(element)

        # Fix fill and stroke attributes for FileMaker compatibility
        self._fix_fill_and_stroke(element, tag)

        # Remove unsupported attributes
        self._remove_unsupported_attributes(element, tag)

        # Recursively fix children
        for child in element:
            self._fix_elements_recursively(child)

    def _fix_circle(self, element):
        """Fix circle element."""
        if 'r' in element.attrib:
            r_value = element.get('r')
            r_clean = self._remove_units(r_value)

            try:
                r = float(r_clean)
                if r < 0:
                    element.set('r', '0')
                    self.fixes_applied.append(f"Fixed negative circle radius: {r_value} → 0")
                elif r_clean != r_value:
                    element.set('r', r_clean)
                    self.fixes_applied.append(f"Removed units from circle radius: {r_value} → {r_clean}")
            except ValueError:
                pass

    def _fix_ellipse(self, element):
        """Fix ellipse element."""
        for attr in ['rx', 'ry']:
            if attr in element.attrib:
                value = element.get(attr)
                clean_value = self._remove_units(value)

                try:
                    num = float(clean_value)
                    if num < 0:
                        element.set(attr, '0')
                        self.fixes_applied.append(f"Fixed negative ellipse {attr}: {value} → 0")
                    elif clean_value != value:
                        element.set(attr, clean_value)
                        self.fixes_applied.append(f"Removed units from ellipse {attr}: {value} → {clean_value}")
                except ValueError:
                    pass

    def _fix_rect(self, element):
        """Fix rect element."""
        for attr in ['rx', 'ry', 'width', 'height']:
            if attr in element.attrib:
                value = element.get(attr)
                clean_value = self._remove_units(value)

                try:
                    num = float(clean_value)
                    if num < 0:
                        element.set(attr, '0')
                        self.fixes_applied.append(f"Fixed negative rect {attr}: {value} → 0")
                    elif clean_value != value:
                        element.set(attr, clean_value)
                        self.fixes_applied.append(f"Removed units from rect {attr}: {value} → {clean_value}")
                except ValueError:
                    pass

    def _fix_poly(self, element, tag):
        """Fix polyline or polygon element."""
        if 'points' not in element.attrib:
            return

        points_str = element.get('points').strip()
        # Remove units from points
        cleaned = self._remove_units_from_points(points_str)

        if cleaned != points_str:
            element.set('points', cleaned)
            self.fixes_applied.append(f"Removed units from {tag} points")

        # Check for odd number of coordinates
        coords = re.split(r'[\s,]+', cleaned)
        coords = [c for c in coords if c]

        if len(coords) % 2 != 0:
            # Remove the last coordinate to make it even
            coords = coords[:-1]
            element.set('points', ' '.join(coords))
            self.fixes_applied.append(f"Fixed odd number of coordinates in {tag} (removed last coordinate)")

    def _fix_path(self, element):
        """Fix path element."""
        if 'd' not in element.attrib:
            return

        # Path data is complex, just remove obvious units
        d_value = element.get('d')
        cleaned = self._remove_units_from_path(d_value)

        if cleaned != d_value:
            element.set('d', cleaned)
            self.fixes_applied.append("Removed units from path data")

    def _fix_fill_and_stroke(self, element, tag):
        """Remove fill attributes for FileMaker theme compatibility."""
        # Shape elements that FileMaker can make theme-responsive
        shape_elements = ['path', 'circle', 'ellipse', 'rect', 'polygon', 'polyline']

        if tag not in shape_elements:
            return

        # Remove fill attribute for theme-responsive shapes
        # FileMaker wraps content in <g class="fm_fill"> and shapes inherit from parent
        # Only keep fill if it's a URL reference (gradient) or explicit "none"
        if 'fill' in element.attrib:
            fill_value = element.get('fill')
            # Keep gradients (url(#...)) and explicit "none"
            if not (fill_value.startswith('url(') or fill_value == 'none'):
                del element.attrib['fill']
                self.fixes_applied.append(f"Removed fill attribute from <{tag}> (will inherit from FileMaker fm_fill wrapper)")

        # Also check style attribute for fill
        if 'style' in element.attrib:
            style = element.get('style', '')
            if 'fill:' in style and 'url(' not in style:
                # Remove fill from style, keep other properties
                style_parts = [s.strip() for s in style.split(';') if s.strip()]
                new_style_parts = [s for s in style_parts if not s.startswith('fill:') or 'url(' in s or 'none' in s]
                if len(new_style_parts) != len(style_parts):
                    new_style = ';'.join(new_style_parts)
                    if new_style:
                        element.set('style', new_style)
                    else:
                        del element.attrib['style']
                    self.fixes_applied.append(f"Removed fill from style attribute of <{tag}> (will inherit from FileMaker fm_fill wrapper)")

        # Keep stroke attributes - FileMaker preserves these
        # No changes needed for stroke

    def _fix_coordinate_attributes(self, element):
        """Fix coordinate attributes by removing units."""
        coordinate_attrs = ['x', 'y', 'x1', 'y1', 'x2', 'y2', 'cx', 'cy']

        for attr in coordinate_attrs:
            if attr in element.attrib:
                value = element.get(attr)
                clean_value = self._remove_units(value)

                if clean_value != value:
                    element.set(attr, clean_value)
                    self.fixes_applied.append(f"Removed units from {attr}: \"{value}\" → \"{clean_value}\"")

    def _fix_transform(self, element):
        """Fix transform attribute - convert degrees to radians if needed."""
        if 'transform' not in element.attrib:
            return

        transform = element.get('transform')

        # Common degree values that should be converted
        common_degrees = [45, 90, 135, 180, 225, 270, 315, 360]

        # Look for rotate() with potentially large values (likely degrees)
        # Pattern allows spaces or commas as separators
        rotate_pattern = r'rotate\s*\(\s*([-+]?\d+\.?\d*)\s*(?:[,\s]+\s*([-+]?\d+\.?\d*)\s*[,\s]+\s*([-+]?\d+\.?\d*))?\s*\)'

        def convert_rotate(match):
            angle_str = match.group(1)
            angle = float(angle_str)
            abs_angle = abs(angle)

            # Convert if: value > 6.28 (2π) OR matches common degree values
            should_convert = abs_angle > 6.28 or abs_angle in common_degrees

            if should_convert:
                angle_rad = angle * math.pi / 180
                self.fixes_applied.append(f"Converted rotation from degrees to radians: {angle}° → {angle_rad:.4f} rad")

                if match.group(2) and match.group(3):
                    return f"rotate({angle_rad:.6f},{match.group(2)},{match.group(3)})"
                else:
                    return f"rotate({angle_rad:.6f})"
            elif abs_angle > 0 and abs_angle <= 6.28:
                # Might be degrees or radians - warn user
                self.warnings.append(
                    f"Transform rotate({angle}) - unclear if degrees or radians. "
                    f"FileMaker requires radians. If this is in degrees, manually convert to {angle * math.pi / 180:.4f} radians"
                )

            return match.group(0)

        new_transform = re.sub(rotate_pattern, convert_rotate, transform)

        # Similar for skewX and skewY
        skew_pattern = r'(skewX|skewY)\s*\(\s*([-+]?\d+\.?\d*)\s*\)'

        def convert_skew(match):
            func = match.group(1)
            angle_str = match.group(2)
            angle = float(angle_str)
            abs_angle = abs(angle)

            should_convert = abs_angle > 6.28 or abs_angle in common_degrees

            if should_convert:
                angle_rad = angle * math.pi / 180
                self.fixes_applied.append(f"Converted {func} from degrees to radians: {angle}° → {angle_rad:.4f} rad")
                return f"{func}({angle_rad:.6f})"
            elif abs_angle > 0 and abs_angle <= 6.28:
                self.warnings.append(
                    f"Transform {func}({angle}) - unclear if degrees or radians. "
                    f"FileMaker requires radians. If this is in degrees, manually convert to {angle * math.pi / 180:.4f} radians"
                )

            return match.group(0)

        new_transform = re.sub(skew_pattern, convert_skew, new_transform)

        if new_transform != transform:
            element.set('transform', new_transform)

    def _remove_unsupported_attributes(self, element, tag):
        """Remove attributes not supported by FileMaker."""
        # List of commonly unsupported attributes
        unsupported = [
            'class',  # Not needed (except fm_fill which FileMaker adds)
            'xmlns:svg',  # Wrong namespace prefix
        ]

        for attr in list(element.attrib.keys()):
            if attr in unsupported:
                del element.attrib[attr]
                self.fixes_applied.append(f"Removed unsupported attribute '{attr}' from <{tag}>")

    def _remove_units(self, value):
        """Remove unit symbols from a value string."""
        if not value:
            return value

        # Skip percentages (allowed in gradients)
        if value.endswith('%'):
            return value

        # Remove unit symbols
        unit_pattern = r'(px|pt|pc|cm|mm|in|em|ex|rem)$'
        return re.sub(unit_pattern, '', value.strip(), flags=re.IGNORECASE)

    def _remove_units_from_points(self, points_str):
        """Remove units from points attribute."""
        # Replace any number followed by units with just the number
        pattern = r'([-+]?\d+\.?\d*)(px|pt|pc|cm|mm|in|em|ex|rem)'
        return re.sub(pattern, r'\1', points_str, flags=re.IGNORECASE)

    def _remove_units_from_path(self, path_data):
        """Remove units from path data."""
        pattern = r'([-+]?\d+\.?\d*)(px|pt|pc|cm|mm|in|em|ex|rem)'
        return re.sub(pattern, r'\1', path_data, flags=re.IGNORECASE)

    def get_results(self):
        """Return healing results."""
        return {
            'fixes_applied': self.fixes_applied,
            'warnings': self.warnings
        }

    def print_results(self):
        """Print healing results to console."""
        if self.fixes_applied:
            print("\n✅ FIXES APPLIED:")
            for i, fix in enumerate(self.fixes_applied, 1):
                if fix.startswith("ERROR:"):
                    print(f"  {i}. ❌ {fix}")
                else:
                    print(f"  {i}. {fix}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        if not self.fixes_applied and not self.warnings:
            print("\n✅ No fixes needed - SVG is already FileMaker-compatible!")


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python heal_filemaker_svg.py <input-svg-file> [output-svg-file]")
        print("\nIf output file is not specified, the input file will be overwritten.")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(input_path).exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    print(f"Healing: {input_path}")
    if output_path:
        print(f"Output: {output_path}")
    else:
        print(f"Output: {input_path} (will be overwritten)")
    print("=" * 60)

    healer = FileMakerSVGHealer()
    success = healer.heal_file(input_path, output_path)
    healer.print_results()

    if success:
        print(f"\n✅ Healed SVG saved successfully!")
        print(f"\n💡 Tip: Run validation to confirm FileMaker compliance:")
        output_file = output_path or input_path
        print(f"    python3 scripts/validate_filemaker_svg.py {output_file}")
        sys.exit(0)
    else:
        print(f"\n❌ Healing failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
