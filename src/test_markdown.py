import unittest

from extract_markdown import *
from textnode import *
from split_nodes import *

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

# tests for markdown_to_blocks(markdown)

if __name__ == "__main__":
    unittest.main()