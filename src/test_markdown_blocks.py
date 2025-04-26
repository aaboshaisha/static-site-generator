import unittest

from markdown_blocks import markdown_to_blocks

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


if __name__ == "__main__":
    unittest.main()
