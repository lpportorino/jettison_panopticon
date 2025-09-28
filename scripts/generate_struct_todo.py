#!/usr/bin/env python3
import json
import sys
from typing import Dict, List, Any

def extract_struct_hierarchy(obj: Any, path: str = "", parent_path: str = "") -> List[Dict[str, Any]]:
    """
    Recursively extract all structures and their fields from the JSON.
    Returns a list of dictionaries with structure info.
    """
    structs = []

    if isinstance(obj, dict):
        if "type" in obj and obj["type"] == "structure" and "name" in obj:
            # Create entry for this structure
            struct_info = {
                "name": obj.get("name", "unnamed"),
                "path": path,
                "parent_path": parent_path,
                "fields": []
            }

            # Get fields
            if "fields" in obj:
                for field in obj["fields"]:
                    field_info = {
                        "name": field.get("name", "unnamed"),
                        "ctype": field.get("ctype", "unknown"),
                        "array_length": field.get("array_length", None)
                    }
                    struct_info["fields"].append(field_info)

                    # Recursively process nested structures
                    if "details" in field:
                        nested_path = f"{path}.{field['name']}" if path else field["name"]
                        nested_structs = extract_struct_hierarchy(
                            field["details"],
                            nested_path,
                            path
                        )
                        structs.extend(nested_structs)

                    # Process array element details
                    if "element_details" in field:
                        nested_path = f"{path}.{field['name']}[]" if path else f"{field['name']}[]"
                        nested_structs = extract_struct_hierarchy(
                            field["element_details"],
                            nested_path,
                            path
                        )
                        structs.extend(nested_structs)

            structs.append(struct_info)

        # Process fields at top level
        elif "fields" in obj:
            for field in obj["fields"]:
                if "details" in field:
                    field_path = f"{path}.{field['name']}" if path else field["name"]
                    nested_structs = extract_struct_hierarchy(
                        field["details"],
                        field_path,
                        path
                    )
                    structs.extend(nested_structs)

                if "element_details" in field:
                    field_path = f"{path}.{field['name']}[]" if path else f"{field['name']}[]"
                    nested_structs = extract_struct_hierarchy(
                        field["element_details"],
                        field_path,
                        path
                    )
                    structs.extend(nested_structs)

    return structs

def generate_markdown_todo(structs: List[Dict[str, Any]]) -> str:
    """
    Generate markdown content with todo items for each structure.
    """
    md_lines = []
    md_lines.append("# Struct Verification Todo List")
    md_lines.append("")
    md_lines.append("This document contains todo items for verifying that all struct fields are properly printed in the state view and documented in the report.")
    md_lines.append("")
    md_lines.append("## Todo Format")
    md_lines.append("- [ ] **Check struct printing**: Verify all fields are included in state view")
    md_lines.append("  - [ ] **Add to report**: Document findings for this struct in the report file")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    # Group structs by top-level path component
    top_level_groups = {}
    for struct in structs:
        if struct["path"]:
            top_level = struct["path"].split(".")[0]
        else:
            top_level = "root"

        if top_level not in top_level_groups:
            top_level_groups[top_level] = []
        top_level_groups[top_level].append(struct)

    # Generate todos for each group
    for group_name, group_structs in sorted(top_level_groups.items()):
        if group_name == "root":
            md_lines.append("## Root Structure")
        else:
            md_lines.append(f"## Field: `{group_name}`")
        md_lines.append("")

        for struct in sorted(group_structs, key=lambda x: x["path"]):
            # Main struct header
            if struct["path"]:
                md_lines.append(f"### `{struct['path']}` ({struct['name']})")
            else:
                md_lines.append(f"### Main Structure ({struct['name']})")
            md_lines.append("")

            # Todo items
            md_lines.append(f"- [ ] **Verify printing of `{struct['name']}`**")
            md_lines.append(f"  - Check that all {len(struct['fields'])} fields are printed in state view:")

            # List fields for reference
            for field in struct["fields"]:
                field_str = f"    - `{field['name']}` ({field['ctype']}"
                if field["array_length"]:
                    field_str += f", array[{field['array_length']}]"
                field_str += ")"
                md_lines.append(field_str)

            md_lines.append(f"  - [ ] **Add report entry for `{struct['name']}`**")
            md_lines.append(f"    - Document which fields are correctly printed")
            md_lines.append(f"    - Note any missing or incorrectly formatted fields")
            md_lines.append(f"    - Add recommendations for fixes if needed")
            md_lines.append("")

    # Add summary section
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## Summary Statistics")
    md_lines.append("")
    md_lines.append(f"- Total structures to verify: {len(structs)}")
    md_lines.append(f"- Total todo items: {len(structs) * 2} (2 per struct)")
    md_lines.append("")
    md_lines.append("## Completion Tracking")
    md_lines.append("")
    md_lines.append("- [ ] All struct printing verified")
    md_lines.append("- [ ] All report entries added")
    md_lines.append("- [ ] Final review completed")

    return "\n".join(md_lines)

def main():
    # Read JSON file
    json_file = "/home/jare/git/jettison_panopticon/c_data_python_bindings/jon_gui_state.json"
    output_file = "/tmp/struct_verification_todos.md"

    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    # Extract all structures
    structs = extract_struct_hierarchy(data)

    # Generate markdown
    markdown_content = generate_markdown_todo(structs)

    # Write output file
    try:
        with open(output_file, 'w') as f:
            f.write(markdown_content)
        print(f"Successfully generated todo list with {len(structs)} structures")
        print(f"Output written to: {output_file}")
        print(f"Total todo items created: {len(structs) * 2}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()