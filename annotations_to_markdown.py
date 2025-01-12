import json
import sys
from collections import defaultdict

def parse_annotations(file_path):
    # Read the JSON file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    annotations = data.get("annotations", {})
    chapters = defaultdict(list)

    # Group annotations by chapter
    for annotation in annotations.values():
        chapter = annotation.get("chapter", "Unknown Chapter")
        text = annotation.get("text", "").strip()
        if text:
            chapters[chapter].append(text)

    return chapters

def generate_markdown(chapters):
    # Generate Markdown content
    markdown = []
    for chapter, texts in chapters.items():
        markdown.append(f"# {chapter}\n")
        for text in texts:
            markdown.append(f"- {text}\n")
        markdown.append("")  # Blank line between chapters
    return "\n".join(markdown)

def main():
    if len(sys.argv) != 2:
        print("Usage: python annotations_to_markdown.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    chapters = parse_annotations(file_path)
    markdown = generate_markdown(chapters)

    # Output the Markdown to stdout
    print(markdown)

if __name__ == "__main__":
    main()

