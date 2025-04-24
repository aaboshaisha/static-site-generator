import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unitest.main()
