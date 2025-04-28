import re
from enum import Enum
from parentnode import *
from leafnode import *
from textnode import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(md):
    """takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings"""
    blocks = re.split(r'\n\n', md.strip())
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):
    def is_heading(s): return True if re.match(r'#{1,6}\s.+', s) else False
    def is_quote(s): return all([line.startswith('> ') for line in s.split('\n')])
    def is_unordered_list(s): return all([line.startswith('- ') for line in s.split('\n')])
    def is_code(s): return True if re.match(r'^```[\s\S]*?```$', s) else False
    def is_ordered_list(s):
        matches = [re.match(r'^([0-9]+)\.\s', line.lstrip()) for line in s.splitlines()]
        if not all(matches): return False
        nums = [int(mo.group(1)) for mo in matches if mo]
        if nums[0] != 1: return False
        
        for i in range(0, len(nums)-1): # is it increasing
            if nums[i+1] != nums[i] + 1:
                return False
        return True


    block = block.strip()
    if is_heading(block): return BlockType.HEADING
    elif is_quote(block): return BlockType.QUOTE
    elif is_code(block): return BlockType.CODE
    elif is_unordered_list(block): return BlockType.ULIST
    elif is_ordered_list(block): return BlockType.OLIST
    else: return BlockType.PARAGRAPH


def text_to_children(text):
    """takes a string of text and returns a list of HTMLNodes that represent the inline markdown """
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in textnodes]

def parse_paragraphs(text):
    ps = [p.replace('\n', ' ') for p in text.strip().split('\n\n')]
    nodes = [ParentNode('p', text_to_children(p)) for p in ps]
    return nodes

def parse_code(text):
    type_ = block_to_block_type(text)
    if type_!= BlockType.CODE:
        raise ValueError(f'Not a CODE type: {type_}')
    
    raw_txt = text.strip()[4:-3]
    leaf_node = text_node_to_html_node(TextNode(raw_txt, TextType.CODE))
    return ParentNode('pre', [leaf_node,])

def parse_quote(text):
    lines = [line for line in text.split('\n') if line]
    fmt_lines = []
    for line in lines:
        if not line.startswith('> '):
            raise ValueError('No a valid blockquote')
        fmt_lines.append(line.lstrip('>').strip())
    lines = ' '.join(fmt_lines)
    children = []
    for line in lines:
        children.extend(text_to_children(line))
    return ParentNode('blockquote', children)

def parse_heading(text):
    mo = re.match(r'(#+)\s', text)
    level = len(mo.group(1))
    return ParentNode(f'h{level}', text_to_children(text[level+1:]))

def parse_lists(text):
    tag, ix, type_= '', 0, block_to_block_type(text)
    
    if type_ == BlockType.ULIST: tag, ix = 'ul', 2
    elif type_ == BlockType.OLIST: tag, ix = 'ol', 3
    else: raise ValueError(f'Not a LIST type: {type_}')

    lines = [line[ix:] for line in text.strip().split('\n')]
    nodes = [ParentNode('li', text_to_children(line)) for line in lines]
    return ParentNode(tag, nodes)
    

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    children = []
    for block in blocks:
        type_ = block_to_block_type(block)
        if type_ == BlockType.PARAGRAPH:
            node = parse_paragraphs(block)
        elif type_ == BlockType.QUOTE:
            node = parse_quote(block)
        elif type_ == BlockType.CODE:
            node = parse_code(block)
        elif type_ == BlockType.HEADING:
            node = parse_heading(block)
        elif type_ in [BlockType.ULIST, BlockType.OLIST]:
            node = parse_lists(block)
        else:
            raise ValueError('Unknown block type')
        
        if isinstance(node, list): children.extend(node)
        else: children.extend([node])
    return ParentNode('div', children)
