import sys
import re
from collections import defaultdict
from datetime import datetime

def parse_lua_file(file_path):
    """
    Parse the Lua file to extract annotations, page numbers, and group them by chapter.
    """
    annotations = defaultdict(list)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex to capture each annotation block
    annotation_pattern = re.compile(r"\[(\d+)] = \{(.*?)\},", re.DOTALL)
    matches = annotation_pattern.findall(content)

    for _, annotation_block in matches:
        page_match = re.search(r'\["pageno\"] = (\d+)', annotation_block)
        chapter_match = re.search(r'\["chapter\"] = "(.*?)"', annotation_block)
        text_match = re.search(r'\["text"\]\s*=\s*"((?:[^"\\]|\\.)*)"', annotation_block, re.DOTALL)

        if chapter_match and text_match and page_match:
            page_number = page_match.group(1)
            chapter = chapter_match.group(1)
            text = text_match.group(1)
            text = text.replace('\r', ' ').replace('[', '').replace(']', '').replace('\n',' ')
            annotations[chapter].append((page_number, text))

    return annotations

def annotations_to_markdown(annotations):
    """
    Convert annotations grouped by chapter into Markdown format with page numbers, indents, and datetime.
    """
    markdown_lines = []
    for chapter, annotations_list in annotations.items():
        markdown_lines.append(f"## {chapter}")  # Page header with chapter number
        markdown_lines.append("")  # Add a blank line after the header
        for page_number, text in annotations_list:
            markdown_lines.append(f"### Page {page_number}")  # Page number header
            markdown_lines.append(f"> {text}")  # Indented annotation
            markdown_lines.append(f"  - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  # Datetime of annotation
        markdown_lines.append("")  # Add a blank line after each chapter
    return "\n".join(markdown_lines)

def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_annotations.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        annotations = parse_lua_file(file_path)
        markdown_output = annotations_to_markdown(annotations)
        print(markdown_output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

