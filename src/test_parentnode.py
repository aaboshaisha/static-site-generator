import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_raises_no_children_exception(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("p")
        self.assertEqual(str(context.exception), 'Parent node must have at least one child.')
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_with_many_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),],)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_tree(self):
        s1 = LeafNode('span', 'span1')
        s2 = LeafNode('span', 'span2')
        s3 = LeafNode('span', 'span3')
        s4 = LeafNode('span', 'span4')
        
        h4 = ParentNode('h4', [s4])
        h3 = ParentNode('h3', [s3, h4])
        h2 = ParentNode('h2', [s2, h3])
        h1 = ParentNode('h1', [s1, h2])
        
        out = "<h1><span>span1</span><h2><span>span2</span><h3><span>span3</span><h4><span>span4</span></h4></h3></h2></h1>"
        
        self.assertEqual(h1.to_html(), out)
