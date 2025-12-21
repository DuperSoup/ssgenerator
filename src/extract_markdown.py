import re
from enum import Enum
from htmlnode import *
# from split_nodes import *
from textnode import *
# from other_functions import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_markdown_images(text):
    alt_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text

def extract_markdown_links(text):
    alt_text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text

def markdown_to_blocks(markdown): # takes markdown and returns a list of block strings
    blocks = markdown.split("\n\n")

    final_blocks = []
    for block in blocks:
        if block != "":
            block = block.strip() # strip whitespace from block
            final_blocks.append(block)

    return final_blocks

def block_to_block_type(block): # a block is a just a string
    block = block.strip()
    
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == '#':
                count += 1
            else:
                break

        # if the number of # is between 1 and 6 and the character after all of the #s is a space, then it is truly a HEADING block
        if 1 <= count <= 6 and block[count] == ' ':
            return BlockType.HEADING
        

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    elif block.startswith(">"):
        is_quote = True
        lines = block.split("\n")
        for line in lines:
            if line.startswith(">") is False:
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    
    elif block.startswith("- "):
        is_unordered_list = True
        lines = block.split("\n")
        for line in lines:
            if line.startswith("- ") is False:
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    

    elif block.startswith("1. "):
        # have to check if the following lines are "{digit}. " to be considered an ordered list block
        is_ordered_list = True
        lines = block.split("\n")
        n = 1 # n is the expected number in the list
        for line in lines:
            if line.startswith(f"{n}. ") is False:
                is_ordered_list = False # a line doesn't start with "{n}. " so it is a paragraph block
                break
            n += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    

    return BlockType.PARAGRAPH


        