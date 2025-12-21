class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
            self.tag = tag
            self.value = value
            self.children = children
            self.props = props or {} # use an empty dictionary if props is None

    def to_html(self):
          raise NotImplementedError
    
    def __eq__(self, htmlnode):
         if self.tag == htmlnode.tag and self.value == htmlnode.value and self.children == htmlnode.children and self.props == htmlnode.props:
              return True
         return False
    
    def props_to_html(self):
          if not self.props:
               return ""
          props_html = ""
          for prop in self.props:
               props_html += f' {prop}="{self.props[prop]}"'
          return props_html

    def __repr__(self):
          return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

         
    
class LeafNode(HTMLNode):
     # no children, both value and tag required even though tag may be None
     # props can be optional
    def __init__(self, tag, value, props=None):
        props = props or {}
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")

        # raw text if there's no tag
        if self.tag is None:
            return self.value

        # use props_to_html from HTMLNode for attributes
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
     # tag and children are required
     # doesn't take a value argument
     # props is optional
     def __init__(self, tag, children, props=None):
        props = props or {}
        super().__init__(tag=tag, children=children, props=props)

     def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")

        if self.children is None:
            return ValueError("invalid HTML: no children")

        # use props_to_html from HTMLNode for attributes
        total_text = ""
        for child in self.children:
               child_text = child.to_html()
               total_text += child_text
        return f"<{self.tag}{self.props_to_html()}>{total_text}</{self.tag}>"
        

        




