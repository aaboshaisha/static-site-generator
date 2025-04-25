import unittest
from enum import Enum

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text nod", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, 'boot.dev')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("This text should be bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This text should be bold")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This text should be italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This text should be italic")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {'href': "https://www.example.com"})

    def test_image(self):
        node = TextNode("Example image", TextType.IMAGE, url="https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': "https://www.example.com/image.png", 'alt': "Example image"})

    def test_unrecognized_type(self):
        class UnknownTextType(Enum):
            UNKNOWN = 'unknown'
        node = TextNode("Unknown type", UnknownTextType.UNKNOWN)
        with self.assertRaisesRegex(Exception, "unknown Not a recognized type"):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unitest.main()
