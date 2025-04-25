from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        if children is None or children == []:
            raise ValueError('Parent node must have at least one child.')
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('Parent node must have tag.')
        if self.children is None or []:
            raise ValueError('Parent node must have at least one child.')
        
        def helper(node, s=''):
            if hasattr(node, 'children'):
                for c in node.children:
                    s += c.to_html()
                return f'<{self.tag}>{s}</{self.tag}>'
            return node.to_html()
        return helper(self)

