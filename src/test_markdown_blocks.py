import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

import textwrap

class TestMDtoBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph
            
            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line
            
            - This is a list
            - with items
        """)
        blocks = markdown_to_blocks(md)
        eblocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(blocks, eblocks)
        
    def test_markdown_to_blocks_extra_lines(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph
            
            
            
            
            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line
            
            - This is a list
            - with items
        """)
        blocks = markdown_to_blocks(md)
        eblocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(blocks, eblocks)

    def test_block_types(self):
        mds = [
            ("This is a simple paragraph of text that explains an idea or concept.", BlockType.PARAGRAPH),
            ("# This is a Heading", BlockType.HEADING),
            ("## This is a Heading", BlockType.HEADING),
            ("## This is a Heading", BlockType.HEADING),
            ("#### This is a Heading", BlockType.HEADING),
            ("##### This is a Heading", BlockType.HEADING),
            ("###### This is a Heading", BlockType.HEADING),
            ("####### This is NOT a Heading", BlockType.PARAGRAPH),
            ("```print('Hello, world!')```", BlockType.CODE),
            ("> This is a quoted text from another source.", BlockType.QUOTE),
            ("- Item one\n- Item two\n- Item three", BlockType.ULIST),
            ("1. First item\n2. Second item\n3. Third item", BlockType.OLIST),
            ("""```\ndef hello():\nprint('hi')\n```""", BlockType.CODE),
            ('0. Hello\n 1. World', BlockType.PARAGRAPH),
            ('1. Hello\n 1. World', BlockType.PARAGRAPH),
        ]
        for txt, type_ in mds:
            self.assertEqual(block_to_block_type(txt), type_)


