import unittest
from enum import Enum

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_link, split_nodes_image

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

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_single_delimiter_raises_error(self):
        nodes = [TextNode("Text with one ` delimiter", TextType.TEXT)]
        with self.assertRaisesRegex(ValueError, 'Invalid markdown. "`" not closed.'):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_valid_delimiter(self):
        nodes = [TextNode("Text before `code` after", TextType.TEXT)]
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_valid_delimiter_at_start(self):
        nodes = [TextNode("`code` after", TextType.TEXT)]
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_valid_delimiter_at_end(self):
        nodes = [TextNode("Text before `code`", TextType.TEXT)]
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)


    def test_non_text_node_is_preserved(self):
        bold_node = TextNode("Bold text", TextType.BOLD)
        nodes = [TextNode("Text before `code` after", TextType.TEXT), bold_node]
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delimiter_is_empty_string_raises_error(self):
        nodes = [TextNode("Some text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "", TextType.CODE)


class TestExtractImgsLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        test_cases = [
            ("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", [("image", "https://i.imgur.com/zjjcJKZ.png")]),
            ("![alt text](relative/path/img.jpg)", [("alt text", "relative/path/img.jpg")]),
            ("Multiple images: ![img1](url1) and ![img2](url2)", [("img1", "url1"), ("img2", "url2")]),
            ("Text before ![img](url)", [("img", "url")]),
            ("![img](url) text after", [("img", "url")]),
            ("![alt](url \"Image Title\")", [("alt", "url \"Image Title\"")]),
            ("![](/path/no_alt.png)", [("", "/path/no_alt.png")]), # No alt text
            ("No image here", []),
            ("[not an image](url)", []), # Should not match links
        ]
        for text, expected in test_cases:
            matches = extract_markdown_images(text)
            self.assertListEqual(expected, matches)

    def test_extract_markdown_links(self):
        test_cases = [
            ("This has a [link](https://example.com).", [("link", "https://example.com")]),
            ("[Link with title](https://anothersite.org \"Title\")", [("Link with title", "https://anothersite.org \"Title\"")]),
            ("Multiple links: [one](url1) and [two](url2)", [("one", "url1"), ("two", "url2")]),
            ("Text before [link](url)", [("link", "url")]),
            ("[link](url) text after", [("link", "url")]),
            ("[simple link](url)", [("simple link", "url")]),
            ("No link here", []),
            ("![not a link](url)", []), # Should not match images
            ("[link](url with spaces)", [("link", "url with spaces")]),
            ("[link](url?param=value)", [("link", "url?param=value")]),
            ("[link](url#fragment)", [("link", "url#fragment")]),
            ("[link]()", [("link", "")]), # Empty URL
            ("[](url)", [("", "url")]), # Empty link text
        ]
        for text, expected in test_cases:
            matches = extract_markdown_links(text)
            self.assertListEqual(expected, matches)

class TestSplitLinksImages(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_and_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )



if __name__ == "__main__":
    unitest.main()
