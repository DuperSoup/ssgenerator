import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, 'http://localhost:8888')
        node2 = TextNode("This is a text node", TextType.ITALIC, 'http://localhost:8888')
        self.assertEqual(node, node2)

    def test_eq_url_None(self):
        node = TextNode("This is a text node", TextType.CODE, None)
        node2 = TextNode("This is a text node", TextType.CODE, None)
        self.assertEqual(node, node2)

    def test_eq_diff_text(self):
        node = TextNode("This is text node 1", TextType.TEXT)
        node2 = TextNode("This is text node 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_diff_text_type(self):
        node = TextNode("This is text node 1", TextType.TEXT)
        node2 = TextNode("This is text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()