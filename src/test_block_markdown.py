import unittest
from block_markdown import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_ol,
    block_type_paragraph,
    block_type_quote,
    block_type_ul,
    tag_list_item,
    tag_ol,
    tag_paragraph,
    tag_pre,
    tag_quote,
    tag_ul,
)

from htmlnode import ParentNode, LeafNode


class TestBlockMarkdown(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def test_markdown_to_blocks(self):

        inputs = [
            """This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items""",
            """# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is a list item
            * This is another list item""",
            """### Relational and Hierarchical Database Management Systems

            - ***Hierarchical Databases***
                - IBM first designed this type of database system
                - Stored as a parent-child model but the child has only one parent
                - Structure similar to a tree
                    - Records act like child nodes
                - Top most node is the *root node*
                    - If multiple nodes appear at the top level, then those are called root segments
                - Each node has exactly one parent
                - And one parent can have many children
                """,
            "# This is a header block here\n\n Here is a paragraph block\nAnd here is another line in this particular block\n\n* Here is a list\n* And another one",
        ]

        output = [
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\n            This is the same paragraph on a new line",
                "* This is a list\n            * with items",
            ],
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n            * This is another list item",
            ],
            [
                "### Relational and Hierarchical Database Management Systems",
                "- ***Hierarchical Databases***\n                - IBM first designed this type of database system\n                - Stored as a parent-child model but the child has only one parent\n                - Structure similar to a tree\n                    - Records act like child nodes\n                - Top most node is the *root node*\n                    - If multiple nodes appear at the top level, then those are called root segments\n                - Each node has exactly one parent\n                - And one parent can have many children",
            ],
            [
                "# This is a header block here",
                "Here is a paragraph block\nAnd here is another line in this particular block",
                "* Here is a list\n* And another one",
            ],
        ]

        for index in range(len(inputs)):
            self.assertEqual(markdown_to_blocks(inputs[index]), output[index])

    def test_block_to_block_type(self):

        inputs = [
            "###### this is valid",
            "###### ",
            "# this is also valid",
            "# ",
            "```this is a code block here```",
            "```this is also a code block here but without a closure",
            "here is another code block but this time with only a closure```",
            "> Here is a quote block\n > Here is another one",
            "Here is a missing quote starter\n > but the next line has one",
            "> here im starting with a quote\n but the next line doesn't have one",
            "* here is an unordered list\n* hopefully this works out\n* imagine it not working",
            "- Here is a unordered list with dashes\n- Which reminds me i need to add stuff to my todo list\n- with one of things to do are learning how to use vim",
            "- im using this list to mix dashes\n* and asterisk\n- hopefully they work out\n* if not then ima just cringe",
            "-here im intentionally not putting a space in this unordered list\n-so they should come out as a paragraph block type\n",
            "- next im going to intentionally not have a dash on the last point\n- so itll come out as an incomplete list\nthis should come out as a block type paragraph",
            "* same with the asterisks\n* point 2\npoint 3"
            "point 1\n * point 2\n* point 3",
            " * some space in the front\n * heres another\n * and finally one more",
            "1. heres and ordered list\n2. hopefully this works\n3. please men",
            "1. only 1 item in the list",
            "1. ",
            "2. ",
            "1. this shouldnt work\n2. here im leaving the last one empty\n3. ",
            "1. here im intentionally misnumbering the ordered list\n2. this is the same\n4. here we skipped one\n6. and we jumped with this one",
        ]

        output = [
            block_type_heading,
            block_type_paragraph,
            block_type_heading,
            block_type_paragraph,
            block_type_code,
            block_type_paragraph,
            block_type_paragraph,
            block_type_quote,
            block_type_paragraph,
            block_type_paragraph,
            block_type_ul,
            block_type_ul,
            block_type_ul,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_ol,
            block_type_ol,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
        ]
        for index in range(len(inputs)):
            self.assertEqual(block_to_block_type(inputs[index]), output[index])

    def test_markdown_to_html_node(self):
        markdown_input_1 = """
> lets start real simple
> this is a block quote

# heres a heading **with inline elements**

```
code here
```

some paragraph stuff here
multiline also

* heres an unordered list
* some **with inline elements**

- item 1
- item 2

1. heres an ordered list
2. simple and easy to understand
"""

        children_1 = [
            LeafNode(tag_quote, "lets start real simple\nthis is a block quote", None),
            ParentNode(
                "h1",
                [
                    LeafNode(None, "heres a heading ", None),
                    LeafNode("b", "with inline elements", None),
                ],
                None,
            ),
            ParentNode(
                tag_pre, [LeafNode(block_type_code, "\ncode here\n", None)], None
            ),
            LeafNode(tag_paragraph, "some paragraph stuff here\nmultiline also"),
            ParentNode(
                tag_ul,
                [
                    LeafNode(tag_list_item, "heres an unordered list", None),
                    ParentNode(
                        tag_list_item,
                        [
                            LeafNode(None, "some ", None),
                            LeafNode("b", "with inline elements", None),
                        ],
                        None,
                    ),
                ],
                None,
            ),
            ParentNode(
                tag_ul,
                [
                    LeafNode(tag_list_item, "item 1", None),
                    LeafNode(tag_list_item, "item 2", None),
                ],
                None,
            ),
            ParentNode(
                tag_ol,
                [
                    LeafNode(tag_list_item, "heres an ordered list", None),
                    LeafNode(tag_list_item, "simple and easy to understand", None),
                ],
                None,
            ),
        ]
        output_1 = ParentNode("div", children_1, None)

        self.assertEqual(output_1, markdown_to_html_node(markdown_input_1))
