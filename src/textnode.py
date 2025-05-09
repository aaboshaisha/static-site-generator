from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


def text_node_to_html_node(text_node):
    text_type = text_node.text_type.value
    if text_type == 'text':
        return LeafNode(tag=None, value=text_node.text)
    elif text_type == 'bold':
        return LeafNode(tag='b', value=text_node.text)
    elif text_type == 'italic':
        return LeafNode(tag='i', value=text_node.text)
    elif text_type == 'code':
        return LeafNode(tag='code', value=text_node.text)
    elif text_type == 'link':
        return LeafNode(tag='a', value=text_node.text, props={'href':text_node.url})
    elif text_type == 'image':
        return LeafNode(tag='img', value='', props={'src':text_node.url, 'alt':text_node.text})
    else:
        raise Exception(f'{text_type} Not a recognized type')



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT or (delimiter not in node.text):
            new_nodes.append(node) # we only attempt to split "text" type objects
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(f'Invalid markdown. "{delimiter}" not closed.')
           
            split_nodes = []
            for i, part in enumerate(parts):
                if part == "":
                    continue
                else:
                    split_nodes.append(TextNode(part, [TextType.TEXT, text_type][i%2]))
            new_nodes.extend(split_nodes)
    return new_nodes


import re

def extract_markdown_images(text):
    pat = r'!\[([^\]]*)\]\(([^)]*)\)'
    return re.findall(pat, text)

def extract_markdown_links(text):
    pat = r'(?<!!)\[([^\]]*)\]\(([^)]*)\)'
    return re.findall(pat, text)


# both functions behave same - refactor
def split_nodes(old_nodes, pat, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        pattern = pat
        parts = re.split(pattern, node.text)
    
        i, split_nodes = 0, []
        
        while i < len(parts):
            if parts[i] == "":
                i += 1
                continue
            if i % 3 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
                i += 1
            else:
                split_nodes.append(TextNode(parts[i], text_type, parts[i+1]))
                i += 2
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    img_pattern = r'!\[([^\]]*)\]\(([^)]*)\)'
    return split_nodes(old_nodes, img_pattern, TextType.IMAGE)

def split_nodes_link(old_nodes):
    link_pattern = r'(?<!!)\[([^\]]*)\]\(([^)]*)\)'
    return split_nodes(old_nodes, link_pattern, TextType.LINK)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, type_ in [('**', TextType.BOLD), ('_', TextType.ITALIC), ('`', TextType.CODE)]:
        nodes = split_nodes_delimiter(nodes, delimiter, type_)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)
