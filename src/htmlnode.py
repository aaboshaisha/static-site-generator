class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("subclasses must implement!")

    def props_to_html(self):
        if self.props:
            return ''.join(f' {k}="{v}"' for k, v in self.props.items())
        return ''

    def __repr__(self):
        if self.children:
            children_repr = f'\n\n'.join(str(i+1) + '.' + child.__repr__() for i, child in enumerate(self.children))
        else:
            children_repr = None
        return f'HTMLNode:\nTag: <{self.tag}>\nValue: {self.value}\nAttribues: {self.props_to_html()}\nChildren: {children_repr}'
                
