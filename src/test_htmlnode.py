import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_node_without_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), '')

    def test_node_with_single_prop(self):
        node = HTMLNode(tag="a", props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')

    def test_node_with_multiple_props(self):
        node = HTMLNode(tag="img", props={"src": "image.png", "alt": "An image", "width": "100"})
        expected_output = ' src="image.png" alt="An image" width="100"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_node_with_empty_props(self):
        node = HTMLNode(tag="span", props={})
        self.assertEqual(node.props_to_html(), '')

    def test_node_with_props_containing_special_characters(self):
        node = HTMLNode(tag="input", props={"data-value": "some value with spaces", "class": "btn primary"})
        expected_output = ' data-value="some value with spaces" class="btn primary"'
        self.assertEqual(node.props_to_html(), expected_output)

