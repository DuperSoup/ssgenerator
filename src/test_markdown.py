import unittest

from extract_markdown import *
from textnode import *
from split_nodes import *
from other_functions import *

class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_delimiter_code_in_middle(self): # this is the example test
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_code_at_start(self):
        node = TextNode("`code block` is now at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code block", TextType.CODE),
            TextNode(" is now at the start", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple_pairs_of_delimiters(self):
        node = TextNode("`first code block` and then the `second code block` comes after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("first code block", TextType.CODE),
            TextNode(" and then the ", TextType.TEXT),
            TextNode("second code block", TextType.CODE),
            TextNode(" comes after", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_one_delimiter(self):
        node = TextNode("code block` with only one delimter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("code block but no delimter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code block but no delimter", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("`first code block` and then the `second code block` comes after", TextType.TEXT)
        node2 = TextNode("`third code block` and finally the `fourth`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("first code block", TextType.CODE),
            TextNode(" and then the ", TextType.TEXT),
            TextNode("second code block", TextType.CODE),
            TextNode(" comes after", TextType.TEXT),
            TextNode("third code block", TextType.CODE),
            TextNode(" and finally the ", TextType.TEXT),
            TextNode("fourth", TextType.CODE)
        ])

    def test_split_nodes_delimiter_all_inside_delimiter(self):
        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code block", TextType.CODE)
        ])

    def test_split_nodes_image_1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and more text.",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and more text.", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_split_nodes_image_2(self):
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_0(self):
        node = TextNode(
            "This is text with no image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_image_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) followed by text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" followed by text.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_multiple_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and more text.",
            TextType.TEXT,
        )
        node2 = TextNode(
            "New text with a different ![picture](https://i.imgur.com/D2CL71k.jpeg) and something else.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and more text.", TextType.TEXT),
                TextNode("New text with a different ", TextType.TEXT),
                TextNode("picture", TextType.IMAGE, "https://i.imgur.com/D2CL71k.jpeg"),
                TextNode(" and something else.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_link_1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and more text.",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and more text.", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_split_nodes_link_2(self):
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

    def test_split_nodes_link_0(self):
        node = TextNode(
            "This is text with no link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_link_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) followed by text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" followed by text.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_link_only(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_multiple_nodes(self):
        node1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and more text.",
            TextType.TEXT,
        )
        node2 = TextNode(
            "New text with a different [to youtube](https://www.youtube.com/@bootdotdev) and something else.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and more text.", TextType.TEXT),
                TextNode("New text with a different ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" and something else.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                        [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_reverse_order(self):
        text = "[link](https://boot.dev) and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block` and an _italic_ word with a **bold.**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                        [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word with a ", TextType.TEXT),
                TextNode("bold.", TextType.BOLD),
            ],
            new_nodes
        )

    def test_text_to_textnodes_only_1(self):
        text = "This is **text** with an "
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                        [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
            ],
            new_nodes
        )

    def test_text_to_textnodes_none(self):
        text = "This is text."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                        [
                TextNode("This is text.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_text_to_textnodes_no_text(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                        [
            ],
            new_nodes
        )

    def test_markdown_to_blocks_normal(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_markdown_to_blocks_many_lines_between_blocks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_1_block(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_1_line(self):
        md = """



This is **bolded** paragraph



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )

    def test_block_to_block_type_HEADING(self):
        block = "#### This is a heading."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_CODE(self):
        block = "```This is a code block.```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_QUOTE(self):
        block = """>This is a quote.
>This quote continues.
>And again.
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_UNORDERED_LIST(self):
        block = """
- One of the lines.
- Another line.
- And one more.
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ORDERED_LIST(self):
        block = """
1. First item
2. Second item
3. Third item
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_SHOULDNT_BE_HEADING(self):
        block = "####This is not a heading."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_SHOULDNT_BE_CODE(self):
        block = "```This is not a code block.``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_SHOULDNT_BE_QUOTE(self):
        block = """
>This is not a quote.
-It doesn't continue.
>No more.
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_SHOULDNT_BE_UNORDERED_LIST(self):
        block = """
- One of the lines.
A fake!
- But it goes on.
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_SHOULDNT_BE_ORDERED_LIST(self):
        block = """
1. First item
3. But it's cooked
2. It's joever
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_empty(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)  

    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_unordered_list(self):
        md = """
- First **bolded** element
- Second _italic_ element
- Third `code` element
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First <b>bolded</b> element</li><li>Second <i>italic</i> element</li><li>Third <code>code</code> element</li></ul></div>",
        )

    def test_markdown_to_html_node_ordered_list(self):
        md = """
1. First **bolded** element
2. Second _italic_ element
3. Third `code` element
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First <b>bolded</b> element</li><li>Second <i>italic</i> element</li><li>Third <code>code</code> element</li></ol></div>",
        )

    def test_markdown_to_html_node_quote(self):
        md = """
> This is a quote with **bold**
> that spans with _italics_
> multiple lines of `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b>that spans with <i>italics</i>multiple lines of <code>code</code></blockquote></div>",
        )

    def test_markdown_to_html_node_headings(self):
        md = """
# **bold** heading

first paragraph

## _italics_ heading

second paragraph

### `code` heading

third paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1><b>bold</b> heading</h1><p>first paragraph</p><h2><i>italics</i> heading</h2><p>second paragraph</p><h3><code>code</code> heading</h3><p>third paragraph</p></div>"
        )

    def test_extract_title_single_line_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_h1_with_extra_whitespace(self):
        self.assertEqual(extract_title("   #   Hello World   "), "Hello World")

    def test_extract_title_h1_not_first_line(self):
        markdown = """
        Some intro text
        ## Subtitle
        # Main Title
        More content
        """
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_ignores_h2_and_lower(self):
        markdown = """
        ## Subtitle
        ### Subsubtitle
        """
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_multiple_h1_returns_first(self):
        markdown = """
        # First Title
        # Second Title
        """
        self.assertEqual(extract_title(markdown), "First Title")

    def test_no_h1_raises_exception(self):
        markdown = """
        Some text
        ## Subtitle
        """
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()