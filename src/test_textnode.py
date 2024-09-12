import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Testing url default value 
        node = TextNode("This is a text node", 'bold')
        node2 = TextNode("This is a text node", 'bold')
        self.assertEqual(node, node2)

    def test_eq_url_value(self):
        # Testing with url value
        node = TextNode("This is a text node", 'underline', 'www.exampleurl.com')
        node2 = TextNode("This is a text node", 'underline', 'www.exampleurl.com')
        self.assertEqual(node, node2)

    def test_eq_false(self):
        # Testing equality with different values
        node = TextNode("This is a text node", 'bold', 'www.somethinghere.com')
        node2 = TextNode("this is a different text node", 'underline', 'www.anothersite.net')
        self.assertFalse(node == node2, "huh?")

    # WIP
    def test_text_to_html(self):
        pass

        tNode = TextNode("some normal text", text_type_text)
        tNode2 = TextNode("VERY BOLD TEXT", text_type_bold)
        tNode3 = TextNode("Some Fancy Text", text_type_italic)
        tNode4 = TextNode("print('Hello World!')", text_type_code)
        tNode5 = TextNode("www.notasuslink.com", text_type_link, url="www.notasuslink.com")
        tNode6 = TextNode("MEOW", text_type_image, url="catPics.org")



    def test_text_to_html_invalid(self):
        tNode = TextNode("invalid text", text_type="something")
        tNode2 = TextNode("somre more invalid text", text_type="hyper")

        self.assertRaises(ValueError, text_node_to_html_node, tNode)
        self.assertRaises(ValueError, text_node_to_html_node, tNode2)


if __name__ == "__main__":
    unittest.main()