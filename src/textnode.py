from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

tag_type_bold = "b"
tag_type_italic = "i"
tag_type_code = "code"
tag_type_link = "a"
tag_type_image = "img"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return (
            self.text == node.text
            and self.text_type == node.text_type
            and self.url == node.url
        )

    def __repr__(self):
        return f"TEXTNODE({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):

    text_type = text_node.text_type

    if text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_type == text_type_bold:
        return LeafNode(tag_type_bold, text_node.text)
    if text_type == text_type_italic:
        return LeafNode(tag_type_italic, text_node.text)
    if text_type == text_type_code:
        return LeafNode(tag_type_code, text_node.text)
    if text_type == text_type_link:
        return LeafNode(tag_type_link, text_node.text, props={"href": text_node.url})
    if text_type == text_type_image:
        return LeafNode(
            tag_type_image, "", props={"src": text_node.url, "alt": text_node.text}
        )

    raise ValueError(f"Unknown type: {text_node.text_type}")
