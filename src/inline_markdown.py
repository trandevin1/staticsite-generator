import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    )



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
            
        
        text_content = node.text.split(delimiter)

        nodes = []

        if len(text_content) % 2 == 0:
            # checking to see if theres a missing closing/opening delimiter
            raise Exception(f"Missing closing/opening {delimiter}")

        for index in range(len(text_content)):
            
            if text_content[index] == "":
                continue

            if index % 2 == 0:
                # Even index means text type content
                nodes.append(TextNode(text_content[index], text_type_text))
            else:
                # Odd index means delimited content
                nodes.append(TextNode(text_content[index], text_type))
        
        new_nodes.extend(nodes)

    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)


def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)

def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:
        
        # add as is if its not a text type
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
    
        split_nodes = []
        
        images = extract_markdown_images(node.text)

        if not images:
            # just in case if there are no matches
            new_nodes.append(node)  
            continue
    
        buffer = node.text

        for index in range(len(images)):
            image_tuple = images[index]

            matched = f"![{image_tuple[0]}]({image_tuple[1]})"
            buffer = buffer.split(matched, 1)

            if len(buffer) != 2:
                raise Exception("Invalid markdown, image section not closed off!")


            # checking to see if its not an empty string
            if buffer[0]:
                split_nodes.append(TextNode(buffer[0], text_type_text))
            
            split_nodes.append(TextNode(image_tuple[0], text_type_image, image_tuple[1]))
            buffer = buffer[1]
        
        # need to possibly do post processing of the buffer
        if buffer:
            split_nodes.append(TextNode(buffer, text_type_text))

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_link(old_nodes):
    
    new_nodes = []

    for node in old_nodes:

        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        split_nodes = []

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        
        buffer = node.text
        for index in range(len(links)):
            link_tuple = links[index]

            matched = f"[{link_tuple[0]}]({link_tuple[1]})"
            buffer = buffer.split(matched, 1)

            if len(buffer) != 2:
                raise Exception("Invalid markdown, link section not closed off!")

            # checking to see if empty string
            if buffer[0] != "":
                split_nodes.append(TextNode(buffer[0], text_type_text))
            
            split_nodes.append(TextNode(link_tuple[0], text_type_link, link_tuple[1]))

            # set the new buffer to the next string to be split
            buffer = buffer[1]

        if buffer:
            split_nodes.append(TextNode(buffer, text_type_text))

        
        new_nodes.extend(split_nodes)

    return new_nodes
        

def text_to_textnodes(text):
    bold_delimiter = "**"
    italic_delimiter = "*"
    code_delimiter = "`"
    textnode = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(textnode, bold_delimiter, text_type_bold)
    nodes = split_nodes_delimiter(nodes, italic_delimiter, text_type_italic)
    nodes = split_nodes_delimiter(nodes, code_delimiter, text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
