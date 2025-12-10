import re

def extract_markdown_images(text):
    alt_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text

def extract_markdown_links(text):
    alt_text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    final_blocks = []
    for block in blocks:
        if block != "":
            block = block.strip()
            final_blocks.append(block)
