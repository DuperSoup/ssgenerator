import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "example text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "example text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)

    def test_diff_tag(self):
        node = HTMLNode("p", "example text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", "example text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_diff_value(self):
        node = HTMLNode("p", "example text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "different text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_eq_children(self):
        node = HTMLNode("p", "example text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "example text", children=node, props={"href": "https://www.google.com", "target": "_blank"})
        node3 = HTMLNode("p", "example text", children=node, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node2, node3)

    def test_props_to_html(self):
        node = HTMLNode("p", "example text", children=None, props={"href": "https://www.google.com", "target": "_blank"})
        testtext = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), testtext)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "example text", props={"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode("p", "example text", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)

    def test_leaf_props_to_html(self):
        node = LeafNode("p", "example text", props={"href": "https://www.google.com", "target": "_blank"})
        testtext = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), testtext)

    # def test_leaf_to_html_novalue(self):
    #     node = LeafNode("p", value=None, props={"href": "https://www.google.com", "target": "_blank"})
    #     self.assertEqual(node.to_html(), ValueError)

    def test_leaf_to_html_notag(self):
        node = LeafNode(tag=None, value="example text", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.value, "example text")

    def test_leaf_to_html_ptag(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_to_html_atag(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("tele", "child2")
        child_node3 = LeafNode("woru", "child3")
        parent_node = ParentNode("div", children = 
                                 [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), 
                         "<div><span>child1</span><tele>child2</tele><woru>child3</woru></div>")
        
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")



if __name__ == "__main__":
    unittest.main()