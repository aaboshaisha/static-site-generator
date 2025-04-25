from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,tag, value=None, props=None):
        if value is None:
            raise ValueError('All leaf nodes must have a value.')
        super().__init__(tag=tag, value=value, children=None, props=props)
        

    def to_html(self):
        if self.value is None:
            raise ValueError('All leaf nodes must have a value.')
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        parts = []
        if self.tag: parts.append(f'tag="{self.tag}"')
        parts.append(f'value="{self.value}"')
        if self.props: parts.append(f'props={self.props}')
        return f'LeafNode({", ".join(parts)})'
