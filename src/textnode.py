from enum import Enum
from htmlnode import LeafNode
# from split_nodes import *

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
            self.text = text
            self.text_type = TextType(text_type)
            self.url = url
    
    def __eq__(self, textnode):
         if self.text == textnode.text and self.text_type == textnode.text_type and self.url == textnode.url:
              return True
         return False
    
    def __repr__(self):
         return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
     match text_node.text_type:
          case TextType.TEXT:
               return LeafNode(tag=None, value=text_node.text)
          case TextType.BOLD:
               return LeafNode(tag="b", value=text_node.text)
          case TextType.ITALIC:
               return LeafNode(tag="i", value=text_node.text)
          case TextType.CODE:
               return LeafNode(tag="code", value=text_node.text)
          case TextType.LINK:
               return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
          case TextType.IMAGE:
               return LeafNode(tag="img", value = "", 
                                   props={"src": text_node.url, "alt": text_node.text})
          case _:
               raise Exception("No TextNode type given")
    
# works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
# def text_to_children(text):
#      text_nodes = text_to_textnodes(text)
#      children_nodes = []
#      for text_node in text_nodes:
#           html_node = text_node_to_html_node(text_node)
#           children_nodes.append(html_node)
     
#      return children_nodes