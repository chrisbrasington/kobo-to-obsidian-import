import sys
import re
from collections import defaultdict

def parse_lua_file(file_path):
    """
    Parse the Lua file to extract annotations and group them by chapter.
    """
    annotations = defaultdict(list)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex to capture each annotation block
    annotation_pattern = re.compile(r"\[(\d+)] = \{(.*?)\},", re.DOTALL)
    matches = annotation_pattern.findall(content)

    for _, annotation_block in matches:
        chapter_match = re.search(r'\["chapter\"] = \"(.*?)\"', annotation_block)
        text_match = re.search(r'\["text\"] = \"(.*?)\"', annotation_block)

        if chapter_match and text_match:
            chapter = chapter_match.group(1)
            text = text_match.group(1)
            annotations[chapter].append(text)

    return annotations

def annotations_to_markdown(annotations):
    """
    Convert annotations grouped by chapter into Markdown format.
    """
    markdown_lines = []
    for chapter, texts in annotations.items():
        markdown_lines.append(f"# {chapter}")
        markdown_lines.append("")  # Add a blank line after the header
        for text in texts:
            markdown_lines.append(f"- {text}")
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

