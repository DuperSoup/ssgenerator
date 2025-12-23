from split_nodes import *
from textnode import *
import os
import shutil
from pathlib import Path

def text_to_textnodes(text):

    base_node = TextNode(text, TextType.TEXT)

    after_bold_nodes = split_nodes_delimiter([base_node], "**", TextType.BOLD)

    after_italics_nodes = split_nodes_delimiter(after_bold_nodes, "_", TextType.ITALIC)

    after_code_nodes = split_nodes_delimiter(after_italics_nodes, "`", TextType.CODE)
  
    after_image_nodes = split_nodes_image(after_code_nodes)

    after_link_nodes = split_nodes_link(after_image_nodes)


    return after_link_nodes

# works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
def text_to_children(text):
     text_nodes = text_to_textnodes(text)
     children_nodes = []
     for text_node in text_nodes:
          html_node = text_node_to_html_node(text_node)
          children_nodes.append(html_node)
     
     return children_nodes

# converts a full markdown document into a single parent HTMLNode
def markdown_to_html_node(markdown):
     # split the markdown into blocks
     blocks = markdown_to_blocks(markdown)

     # print("BLOCKS:", len(blocks))
     # for i, b in enumerate(blocks):
     #    print("\n")
     #    print(f"BLOCK {i}:", repr(b), "TYPE:", block_to_block_type(b))
     #    print("\n")

     # create parent <div> node, then append block nodes as parent.children
     parent = ParentNode("div", [])

     for block in blocks:
          block_type = block_to_block_type(block)

          node = None
          if block_type == BlockType.HEADING:
               # Work only on the first line of the block
               first_line = block.split("\n", 1)[0]

               # Count leading '#'
               count = 0
               for char in first_line:
                    if char == "#":
                         count += 1
                    else:
                         break

               tag = f"h{count}"

               # Remove the leading '#' characters and following space
               # from the first line only
               text = first_line[count:].lstrip()

               children = text_to_children(text)
               node = ParentNode(tag, children)
        
            
          elif block_type == BlockType.QUOTE:
               tag = 'blockquote'
               # 1. Split the block into lines
               lines = block.split("\n")

               # Collect cleaned lines without the "> "
               cleaned_lines = []
               for line in lines:
                    line = line.strip()
                    if not line:
                         continue
                    # remove leading '>' and optional space
                    if line.startswith(">"):
                         line = line[1:].lstrip()
                    cleaned_lines.append(line)

               # Join all lines into one string
               # (the test you showed seems to just glue them together directly;
               # if needed you can add spaces: " ".join(cleaned_lines))
               text = "".join(cleaned_lines)
               children = text_to_children(text)

               node = ParentNode(tag, children)

          elif block_type == BlockType.CODE:
               tag = 'pre'
               inner_tag = 'code'

               # First, remove the ``` lines explicitly
               lines = block.split("\n")
               inner_lines = lines[1:-1]  # drop first and last (both ```)

               # If the first inner line is empty, drop it
               if inner_lines and inner_lines[0].strip() == "":
                    inner_lines = inner_lines[1:]

               # Join back with '\n' and ensure a final '\n'
               text = "\n".join(inner_lines)
               if not text.endswith("\n"):
                    text += "\n"

               # don't do inline parsing with text_to_children
               text_node = TextNode(text, "normal")
               html_leaf = text_node_to_html_node(text_node) # this is the code text

               code_node = ParentNode(inner_tag, [html_leaf]) # this is in <code> tag
               node = ParentNode(tag, children=[code_node]) # this is in <pre> tag

          elif block_type == BlockType.UNORDERED_LIST:
               tag = 'ul'
               # 1. Split the block into lines
               lines = block.split("\n")

               # 2. For each non-empty line, strip the list marker "- " (or "* ")
               li_nodes = []
               for line in lines:
                    line = line.strip()
                    if not line:
                         continue
                    # assume "- " prefix
                    item_text = line[2:]  # everything after "- "
                    # 3. Convert that item_text to children via text_to_children
                    children = text_to_children(item_text)
                    # 4. Wrap in an <li> ParentNode
                    li_node = ParentNode("li", children)
                    li_nodes.append(li_node)

               
               # 5. Wrap all li_nodes in a <ul> ParentNode
               node = ParentNode(tag, li_nodes)

          elif block_type == BlockType.ORDERED_LIST:
               tag = 'ol'
               lines = block.split("\n")
               li_nodes = []
               for line in lines:
                    line = line.strip()
                    if not line:
                         continue
                    # assume something like "1. " prefix
                    # find first space after the "N." part
                    # simplest: split once on ". "
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                         item_text = parts[1]
                    else:
                         # fallback if formatting weird
                         item_text = line

                    children = text_to_children(item_text)
                    li_node = ParentNode("li", children)
                    li_nodes.append(li_node)

               node = ParentNode(tag, li_nodes)

          elif block_type == BlockType.PARAGRAPH:
               # Clean up the block text first
               lines = [line.strip() for line in block.split("\n")]
               # Filter out lines that became empty
               non_empty = [line for line in lines if line != ""]
               if not non_empty:
                    # nothing meaningful here, skip making a node
                    node = None
               else:
                    text = " ".join(non_empty)
                    children = text_to_children(text)
                    node = ParentNode("p", children)
                    # tag may be None for Leaf Nodes, so not defaulting to paragraph tag

          if node is not None:
               parent.children.append(node)
          else:
            print(block_type)

     return parent

def extract_title(markdown):
     for line in markdown.splitlines():
          line = line.strip()
          # Match an h1: exactly one leading '# ' (not '##')
          if line.startswith("# ") and not line.startswith("##"):
               return line[2:].strip()

     raise ValueError("No h1 header found in markdown")

def copy_files_from_src_to_dst(src, dst):
    # Ensure the source exists
    if not os.path.isdir(src):
        raise ValueError(f"Source directory does not exist: {src}")
    
    # If destination exists, delete everything inside it. Else, make the destination directory.
    if os.path.exists(dst):
        for entry in os.listdir(dst):
            path = os.path.join(dst, entry)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    else:
        os.makedirs(dst)

    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)

        if os.path.isdir(src_path):
            # Recurse into subdirectory
            copy_files_from_src_to_dst(src_path, dst_path)
        elif os.path.isfile(src_path):
            # Copy regular file
            shutil.copy(src_path, dst_path)
        else:
            # Skip non-regular files (e.g., symlinks, sockets, devices)
            pass

def generate_page(from_path, template_path, dest_path):
     # 1. Print status message
     print(f"Generating page from {from_path} to {dest_path} using {template_path}")

     # 2. Read markdown file
     with open(from_path, "r") as f:
          markdown_content = f.read()

     # 3. Read template HTML file
     with open(template_path, "r") as f:
          template_content = f.read()

     # 4. Convert markdown to HTML
     html_node = markdown_to_html_node(markdown_content)
     html_content = html_node.to_html()

     # 5. Extract title
     title = extract_title(markdown_content)

    # 6. Replace placeholders in template
     full_html = template_content \
          .replace("{{ Title }}", title) \
          .replace("{{ Content }}", html_content)
     
     # 7. Write output HTML, creating directories if needed
     dest_dir = os.path.dirname(dest_path)
     if dest_dir:
          os.makedirs(dest_dir, exist_ok=True)

     with open(dest_path, "w") as f:
          f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Crawl every entry in the content directory
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)

        # If it's a directory, recurse into it
        if os.path.isdir(src_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(src_path, template_path, new_dest_dir)

        # If it's a markdown file, generate the HTML page
        elif os.path.isfile(src_path) and src_path.endswith(".md"):
            # Change .md to .html using pathlib
            html_filename = Path(entry).with_suffix(".html").name
            dest_path = os.path.join(dest_dir_path, html_filename)

            generate_page(src_path, template_path, dest_path)