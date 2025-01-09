from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "links"
    IMAGES = "images"

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
    
