from textnode import TextNode
from textnode import TextType
from extract_markdown import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)

        else:
            # split_sections can and will include empty strings which are skipped later
            split_sections = node.text.split(delimiter)
            # print(split_sections)
            # print("\n")
            
            # if len(split_sections) == 1: # only 1 section means delimiter was not found
            #     raise Exception("delimiter not found")

            # check if the number of sections is even, which is invalid because that would indicate an odd number of delimiters
            if len(split_sections) % 2 == 0:
                raise ValueError("invalid markdown, unmatched delimiter")
            
            for i, section in enumerate(split_sections):
                if section == "": # skip empty strings
                    continue

                if i % 2 == 0: # index is even, so outside delimiter, so plain TEXT
                    temp_node = TextNode(section, TextType.TEXT)

                else: # index is odd, so inside delimter, so use text_type)
                    temp_node = TextNode(section, text_type)

                new_nodes.append(temp_node)              
                    
            
    return new_nodes


def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:
        
        # text type is not TEXT, append and continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        
        # no images found in node text, append original TextNode to list
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        current_text = node.text

        # for each tuple in the list of matches, split the text node text once based on each of the alt texts and links
        for tuple in matches:
            image_alt = tuple[0]
            image_link = tuple[1]
            
            # split_sections is a list of strings. it is split before and after the image text
            split_sections = current_text.split(f"![{image_alt}]({image_link})", 1)
            before_image = split_sections[0]
            after_image = split_sections[1]

            # create plain text node for before image
            if before_image != "":
                temp_node = TextNode(before_image, TextType.TEXT)
                new_nodes.append(temp_node)

            # create image text node
            temp_node = TextNode(image_alt, TextType.IMAGE, image_link)
            new_nodes.append(temp_node)

            # assign after_image to be the next current_text to be split and evaluated
            current_text = after_image                    

        # add the text after the image as a plain text node if there is text
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    # print(new_nodes)        
    return new_nodes

def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:
        
        # text type is not TEXT, append and continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        
        # no links found in node text, append original TextNode to list
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        current_text = node.text

        # for each tuple in the list of matches, split the text node text once based on each of the alt texts and links
        for tuple in matches:
            link_alt = tuple[0]
            link_link = tuple[1]
            
            # split_sections is a list of strings. it is split before and after the link text
            split_sections = current_text.split(f"[{link_alt}]({link_link})", 1)
            before_link = split_sections[0]
            after_link = split_sections[1]

            # create plain text node for before link
            if before_link != "":
                temp_node = TextNode(before_link, TextType.TEXT)
                new_nodes.append(temp_node)

            # create link text node
            temp_node = TextNode(link_alt, TextType.LINK, link_link)
            new_nodes.append(temp_node)

            # assign after_link to be the next current_text to be split and evaluated
            current_text = after_link                    

        # add the text after the link as a plain text node if there is text
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    # print(new_nodes)        
    return new_nodes

def text_to_textnodes(text):
    base_node = TextNode(text, TextType.TEXT)
    # print(base_node)
    # print("\n")
    after_bold_nodes = split_nodes_delimiter([base_node], "**", TextType.BOLD)
    # print(after_bold_nodes)
    # print("\n")
    after_italics_nodes = split_nodes_delimiter(after_bold_nodes, "_", TextType.ITALIC)
    # print(after_italics_nodes)
    # print("\n")
    after_code_nodes = split_nodes_delimiter(after_italics_nodes, "`", TextType.CODE)
    # print(after_code_nodes)
    # print("\n")    
    after_image_nodes = split_nodes_image(after_code_nodes)
    # print(after_image_nodes)
    # print("\n")
    after_link_nodes = split_nodes_link(after_image_nodes)
    # print(after_link_nodes)
    # print("\n")

    return after_link_nodes