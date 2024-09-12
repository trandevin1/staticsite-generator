import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_bold,
    text_type_text,
    text_type_code,
    text_type_italic,
    text_type_image,
    text_type_link,
)


class TestInlineMarkdown(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def test_split_nodes_delimiter(self):
        nodes = [
            TextNode(
                "Imagine this is some text with a few *italic* words *here* and *there*.",
                text_type_text,
            ),
            TextNode("Some text with *italic elements*.", text_type_text),
        ]

        self.assertEqual(
            split_nodes_delimiter(nodes, "*", text_type_bold),
            [
                TextNode("Imagine this is some text with a few ", text_type_text),
                TextNode("italic", text_type_bold),
                TextNode(" words ", text_type_text),
                TextNode("here", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("there", text_type_bold),
                TextNode(".", text_type_text),
                TextNode("Some text with ", text_type_text),
                TextNode("italic elements", text_type_bold),
                TextNode(".", text_type_text),
            ],
        )

        nodes_bold = [
            TextNode(
                "Now **here's** a challenge, we're testing a bigger delimiter.",
                text_type_text,
            ),
            TextNode("**Some are sprinkled** here and there.", text_type_text),
            TextNode("**Others might be something like this.**", text_type_text),
        ]

        nodes_bold_correct = [
            TextNode("Now ", text_type_text),
            TextNode("here's", text_type_bold),
            TextNode(" a challenge, we're testing a bigger delimiter.", text_type_text),
            TextNode("Some are sprinkled", text_type_bold),
            TextNode(" here and there.", text_type_text),
            TextNode("Others might be something like this.", text_type_bold),
        ]

        self.assertEqual(
            split_nodes_delimiter(nodes_bold, "**", text_type_bold), nodes_bold_correct
        )

    def test_split_nodes_exception(self):

        bold = "**"
        italic = "*"
        nodes = [
            TextNode("Here are some *wrong closing delimiters!", text_type_text),
            TextNode("Random stuff here*, don't mind me.", text_type_text),
            TextNode("*What if we had it start in the beginning?", text_type_text),
            TextNode("And what if we had it end like this?*", text_type_text),
        ]

        for node in nodes:
            self.assertRaises(
                Exception, split_nodes_delimiter, [node], italic, text_type_italic
            )

        nodes1 = [
            TextNode(
                "**Here im also doing the same thing but with bold stuff.",
                text_type_text,
            ),
            TextNode("Maybe we have some here at the end**!", text_type_text),
            TextNode("And might as well throw in **some here also.", text_type_text),
            TextNode("With some sprinkled here** in the middle!", text_type_text),
        ]

        for nodes in nodes1:
            self.assertRaises(
                Exception, split_nodes_delimiter, nodes1, bold, text_type_bold
            )

    def test_extract_markdown_images(self):
        texts = [
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
            "This is another text with ![crazy wacky image](https://sample.image.googleapi.com/whomadethislol) and ![surprise another one!](https://cutecatpictures.googleapi.com/cutecatsheremeow)",
        ]

        output = [
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
            [
                (
                    "crazy wacky image",
                    "https://sample.image.googleapi.com/whomadethislol",
                ),
                (
                    "surprise another one!",
                    "https://cutecatpictures.googleapi.com/cutecatsheremeow",
                ),
            ],
        ]

        for index in range(len(texts)):
            self.assertEqual(extract_markdown_images(texts[index]), output[index])

    def test_extract_markdown_links(self):
        texts = [
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            "Imagine another text with [a special link](https://www.google.com) and [another link to somewhere sussy](https://www.letsmakeasussybaka.gg)",
        ]

        output = [
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
            [
                ("a special link", "https://www.google.com"),
                (
                    "another link to somewhere sussy",
                    "https://www.letsmakeasussybaka.gg",
                ),
            ],
        ]

        for index in range(len(texts)):
            self.assertEqual(extract_markdown_links(texts[index]), output[index])

    def test_split_images_nodes(self):
        texts = [
            TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) with something extra at the end.",
                text_type_text,
            ),
            TextNode("This is something we need here!", text_type_text),
            TextNode("different text type here", text_type_code),
            TextNode(
                "![1st consecutive image](https://storage.googleapis.com/catMeow.jpg)![2nd consecutive image](storage.googleapis.com/routeApi/catPurr.png)![3rd consecutive image](./images/corn/catSleeping.jpeg)",
                text_type_text,
            ),
        ]

        output = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode(" with something extra at the end.", text_type_text),
            TextNode("This is something we need here!", text_type_text),
            TextNode("different text type here", text_type_code),
            TextNode(
                "1st consecutive image",
                text_type_image,
                "https://storage.googleapis.com/catMeow.jpg",
            ),
            TextNode(
                "2nd consecutive image",
                text_type_image,
                "storage.googleapis.com/routeApi/catPurr.png",
            ),
            TextNode(
                "3rd consecutive image",
                text_type_image,
                "./images/corn/catSleeping.jpeg",
            ),
        ]

        self.assertEqual(split_nodes_image(texts), output)

    def test_split_link_nodes(self):

        texts = [
            TextNode(
                "This is a text with links everywhere [link to something here](https://www.google.com) and another link [not a sussy link here](https://www.yahoo.com). With something ending here!",
                text_type_text,
            ),
            TextNode(
                "Somehow this sentence doesn't have any link markdown.", text_type_text
            ),
            TextNode("This is something else entirely!", text_type_code),
            TextNode(
                "[1st link here](www.crazybooba.gg)[2nd one back to back](www.getbaited.gg)[3rd one in a row](www.google.com)",
                text_type_text,
            ),
        ]

        output = [
            TextNode("This is a text with links everywhere ", text_type_text),
            TextNode(
                "link to something here", text_type_link, "https://www.google.com"
            ),
            TextNode(" and another link ", text_type_text),
            TextNode("not a sussy link here", text_type_link, "https://www.yahoo.com"),
            TextNode(". With something ending here!", text_type_text),
            TextNode(
                "Somehow this sentence doesn't have any link markdown.", text_type_text
            ),
            TextNode("This is something else entirely!", text_type_code),
            TextNode("1st link here", text_type_link, "www.crazybooba.gg"),
            TextNode("2nd one back to back", text_type_link, "www.getbaited.gg"),
            TextNode("3rd one in a row", text_type_link, "www.google.com"),
        ]

        self.assertEqual(split_nodes_link(texts), output)

    def test_text_to_textnodes(self):
        texts = [
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)",
            "![Here is an image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/lole.png) **with** *back* **to** *back* `bold and italic elements` with a sneaky code block. [With a link at the end](www.writegoodtests.gg)",
            "![What if we had an image](https://storage.someapi.com/vault/assets/cat.jpg) [with a link right after it?](www.destiny.gg) After that what if we had **things that are VERY IMPORTANT HERE** and *something to accentuate here!* [Also heres another link](www.google.com)",
        ]

        outputs = [
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            [
                TextNode(
                    "Here is an image",
                    text_type_image,
                    url="https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/lole.png",
                ),
                TextNode(" ", text_type_text),
                TextNode("with", text_type_bold),
                TextNode(" ", text_type_text),
                TextNode("back", text_type_italic),
                TextNode(" ", text_type_text),
                TextNode("to", text_type_bold),
                TextNode(" ", text_type_text),
                TextNode("back", text_type_italic),
                TextNode(" ", text_type_text),
                TextNode("bold and italic elements", text_type_code),
                TextNode(" with a sneaky code block. ", text_type_text),
                TextNode(
                    "With a link at the end",
                    text_type_link,
                    url="www.writegoodtests.gg",
                ),
            ],
            [
                TextNode(
                    "What if we had an image",
                    text_type_image,
                    url="https://storage.someapi.com/vault/assets/cat.jpg",
                ),
                TextNode(" ", text_type_text),
                TextNode(
                    "with a link right after it?", text_type_link, url="www.destiny.gg"
                ),
                TextNode(" After that what if we had ", text_type_text),
                TextNode("things that are VERY IMPORTANT HERE", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("something to accentuate here!", text_type_italic),
                TextNode(" ", text_type_text),
                TextNode(
                    "Also heres another link", text_type_link, url="www.google.com"
                ),
            ],
        ]

        for index in range(len(texts)):
            self.assertEqual(text_to_textnodes(texts[index]), outputs[index])

    def test_empty_text_to_textnodes(self):
        pass
