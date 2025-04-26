import re

def markdown_to_blocks(md):
    """takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings"""
    blocks = re.split(r'\n\s*\n', md.strip())
    return [block.strip() for block in blocks if block.strip()]


