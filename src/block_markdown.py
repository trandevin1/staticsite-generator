block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"

tag_list_item = "li"
tag_ul = "ul"
tag_ol = "ol"
tag_quote = "blockquote"
tag_paragraph = "p"
tag_pre = "pre"

from inline_markdown import text_to_textnodes
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):

    if block.startswith("#"):
        split_block = list(filter((lambda word: len(word) != 0), block.split(" ", 1)))

        if len(split_block) < 2 or len(split_block[0]) > 6:
            return block_type_paragraph

        hash = set(split_block[0])

        if len(hash) > 1 and "#" not in hash:
            return block_type_paragraph

        return block_type_heading

    split_lines = list(map(lambda line: line.strip(" "), block.split("\n")))

    if block.startswith("```") and block.endswith("```"):
        return block_type_code

    if block.startswith(">"):
        # check every line

        for line in split_lines:
            if not line.startswith(">"):
                return block_type_paragraph

        return block_type_quote

    if block.startswith("* ") or block.startswith("- "):

        for line in split_lines:
            if not (line.startswith("* ") or line.startswith("- ")):
                return block_type_paragraph

        return block_type_ul

    if split_lines[0].startswith("1. "):

        counter = 1

        for line in split_lines:
            if not line.startswith(f"{counter}. "):
                return block_type_paragraph
            counter += 1

        return block_type_ol

    return block_type_paragraph


def block_to_tag_name(block, block_type):

    if block_type == block_type_quote:
        return tag_quote
    elif block_type == block_type_code:
        return block_type_code
    elif block_type == block_type_ol:
        return tag_ol
    elif block_type == block_type_ul:
        return tag_ul
    elif block_type == block_type_heading:
        header = header_split(block)
        hashtags = header[0]
        if hashtags and len(hashtags) > 0 and len(hashtags) < 7:
            return f"h{len(hashtags)}"

        return tag_paragraph
    else:
        return tag_paragraph


def header_split(header):
    return list(filter((lambda word: len(word) != 0), header.split(" ", 1)))


def is_Parent(tag, children, text):

    if len(children) == 1 and children[0].tag is None:
        return LeafNode(tag, text, None)

    return ParentNode(tag, children, None)


def block_quote_node(tag, block):

    text = "\n".join(map(lambda x: x[2:], block.split("\n")))
    children = text_to_children(text)
    return is_Parent(tag, children, text)


def block_paragraph_node(tag, block):
    children = text_to_children(block)
    return is_Parent(tag, children, block)


def block_code_node(block):
    children = text_to_children(block)
    return ParentNode(tag_pre, children, None)


def block_heading_node(block, block_type):
    headers = []
    block_text = block.split("\n")
    for line in block_text:
        split_text = header_split(line)
        tag = block_to_tag_name(line, block_type)
        children = text_to_children(split_text[-1])
        head_node = is_Parent(tag, children, split_text[-1])
        headers.append(head_node)

    return headers


def block_ol_ul_node(block, block_type):
    items = block.split("\n")
    item_children = []
    tag = block_to_tag_name(block, block_type)

    for item in items:
        # pre proccessing remove *, -, 1.
        item_text = item[3:] if block_type is block_type_ol else item[2:]
        # get item inline markdown
        children = text_to_children(item_text)
        # put them in either a parent or leaf node
        li = is_Parent(tag_list_item, children, item_text)
        item_children.append(li)

    return ParentNode(tag, item_children, None)


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    block_children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_to_tag_name(block, block_type)

        if block_type == block_type_quote:
            block_children.append(block_quote_node(tag, block))

        elif block_type == block_type_heading:
            block_children.extend(block_heading_node(block, block_type))

        elif block_type == block_type_code:
            block_children.append(block_code_node(block))

        elif block_type == block_type_ul:
            block_children.append(block_ol_ul_node(block, block_type))

        elif block_type == block_type_ol:
            block_children.append(block_ol_ul_node(block, block_type))
        else:
            block_children.append(block_paragraph_node(tag, block))

    return ParentNode("div", block_children, None)


def text_to_children(text):

    nodes = text_to_textnodes(text)

    children = list(map(lambda textnode: text_node_to_html_node(textnode), nodes))

    return children
