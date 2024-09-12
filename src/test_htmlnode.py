import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        
        # Testing props to html conversion
        hNode = HTMLNode("a", "this is a value for the a tag", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(hNode.props_to_html(), ' href="https://www.google.com" target="_blank"')

        hNode2 = HTMLNode("img", "Heading 1", None, {"src": "someCatImage.jpeg", "alt": "meow"})
        self.assertEqual(hNode2.props_to_html(), ' src="someCatImage.jpeg" alt="meow"')


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_no_props(self):
        # testing html conversion without props/html attributes
        lNode = LeafNode("p", "This is a paragraph of text.")
        lNode2 = LeafNode("h1", "This is a Header!")
        self.assertEqual(lNode.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(lNode2.to_html(), "<h1>This is a Header!</h1>")

    def test_to_html_with_props(self):
        # testing html conversion with props/html attributes
        lNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        lNode2 = LeafNode("img", "This is a cat photo", {"src": "funnyCatImage.png", "alt": "MEOW"})
        self.assertEqual(lNode.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(lNode2.to_html(), '<img src="funnyCatImage.png" alt="MEOW">This is a cat photo</img>')
        
    def test_to_html_with_empty_value(self):
        # testing empty value
        lNode = LeafNode("a", props={'href': "somelink.com"})
        lNode2 = LeafNode("p")
        self.assertRaises(ValueError, lNode.to_html)
        self.assertRaises(ValueError, lNode2.to_html)

    def test_to_html_with_empty_tag(self):
        # testing empty tag
        lNode = LeafNode(value="some random text here")
        lNode2 = LeafNode(value="empty tag example here with props", props={'href': "somethingCrazy.com"})
        self.assertEqual(lNode.to_html(), "some random text here")
        self.assertEqual(lNode2.to_html(), "empty tag example here with props")

class TestParentNode(unittest.TestCase):

    def test_to_html_tag_error(self):
        # testing 1st level deep nesting
        pNode = ParentNode(None, [LeafNode(None, "something here")])

        # testing 2nd level deep nesting
        pNode2 = ParentNode("img", [LeafNode(None, "maybe something here"), ParentNode(None, "im in trouble hehe")])
        
        # testing 3rd level deep nesting
        pNode3 = ParentNode("img", 
                            [
                                LeafNode("h1", "Big Head Here"),
                                ParentNode("h2", [ParentNode(None, "Yippie")])
                            ]
                            )
        self.assertRaises(ValueError, pNode.to_html)
        self.assertRaises(ValueError, pNode2.to_html)
        self.assertRaises(ValueError, pNode3.to_html)
    
    def test_to_html_children_error(self):
        # testing 1 level deep w/ no children
        pNode = ParentNode("img", None)

        # testing 2 level deep w/ no children
        pNode2 = ParentNode("img", 
                            [
                                LeafNode(None, "something normal here nothing to see here"),
                                ParentNode("b", [])
                            ])
        
        # testing 3 level deep w/ no children
        pNode3 = ParentNode("a", 
                            [
                                LeafNode("input", "Enter stuff here: "),
                                ParentNode("script", [ParentNode("input", [])])

                            ]
                        )
        self.assertRaises(ValueError, pNode.to_html)
        self.assertRaises(ValueError, pNode2.to_html)
        self.assertRaises(ValueError, pNode3.to_html)


    def test_to_html_no_props(self):
        # testing 1 level deep 
        pNode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        
        # testing varied leaf nodes 1 level deep
        pNode2 = ParentNode("div", 
                           [
                               LeafNode(None, "Some Normal Text."),
                               LeafNode(None, "And some more normal Text"),
                           ]
                           )
        self.assertEqual(pNode.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertEqual(pNode2.to_html(), "<div>Some Normal Text.And some more normal Text</div>")

    def test_to_html_no_props_multi_level(self):
        # testing 2 level deep
        pNode = ParentNode("p", 
                           [
                               LeafNode("b", "VERY BOLD TEXT"),
                               ParentNode("a", 
                                          [
                                              LeafNode(None, "this link takes you to Yippie land"),
                                              LeafNode("b", "CLICK ME! NO VIRUS, TRUST ME.")
                                          ]
                                        ),
                           ]
                        )
        
        # testing 3 level deep
        pNode2 = ParentNode("body", 
                            [
                                LeafNode("h1", "Meme Page"),
                                ParentNode("div", 
                                           [
                                                ParentNode("div", [LeafNode("table", "bunch of values here")]),
                                                LeafNode("h3", "Put head here and win a prize!")
                                           ]
                                        )
                            ]
                        )

        # testing 4 level deep
        pNode3 = ParentNode("body", 
                            [
                                LeafNode("h1", "How to meet the quota in Lethal Company"),
                                LeafNode("p", "first things first dont die"),
                                LeafNode("p", "then try to find as many items"),
                                ParentNode("div", 
                                           [
                                                ParentNode("table", [ParentNode("ul", [LeafNode("l", "ez money"), LeafNode("l","ez life")])])
                                           ]
                                           )
                            ]
                            )
        self.assertEqual(pNode.to_html(), "<p><b>VERY BOLD TEXT</b><a>this link takes you to Yippie land<b>CLICK ME! NO VIRUS, TRUST ME.</b></a></p>")
        self.assertEqual(pNode2.to_html(), "<body><h1>Meme Page</h1><div><div><table>bunch of values here</table></div><h3>Put head here and win a prize!</h3></div></body>")
        self.assertEqual(pNode3.to_html(), "<body><h1>How to meet the quota in Lethal Company</h1><p>first things first dont die</p><p>then try to find as many items</p><div><table><ul><l>ez money</l><l>ez life</l></ul></table></div></body>")


    def test_to_html_with_props(self):
        # testing 1 level deep w/ props on ParentNode
        pNode = ParentNode(
                            tag="body", 
                            children=[LeafNode("p", "something here about finding the one piece")],
                            props={"class": "body_mod", "id": "body_mod", "width": "1px"}
                            )
        
        # testing 1 level deep w/ props on both ParentNode and LeafNode
        pNode2 = ParentNode(
                            tag="body",
                            children=[LeafNode("p", "maybe the one piece is not real or maybe it is!?!?!?!?", {"class": "one-piece", "id": "one-piece"})],
                            props={"class": "body_mod", "id": "body_mod", "width": "1px"}
                            )

        self.assertEqual(pNode.to_html(), '<body class="body_mod" id="body_mod" width="1px"><p>something here about finding the one piece</p></body>')
        self.assertEqual(pNode2.to_html(), '<body class="body_mod" id="body_mod" width="1px"><p class="one-piece" id="one-piece">maybe the one piece is not real or maybe it is!?!?!?!?</p></body>')

    def test_to_html_with_props_multi_level(self):
        pNode = ParentNode(
                            tag="div",
                            children=[
                                ParentNode(
                                    tag="div",
                                    children=[
                                        LeafNode("h2", "Level 2"),
                                        LeafNode("b", "some properties here", props={"class" : "YUP", "id" : "YUP"})
                                    ],
                                    props={"class": "hugh-mungus", "id" : "hugh-mungus"}
                                )
                            ],
                            props={"class" : "big-L", "id" : "big-L"}
        )
        pNode2 = ParentNode(
                            tag="div",
                            children=[
                                ParentNode(
                                    tag="div",
                                    children=[
                                        LeafNode("h2", "Level 2"),
                                        ParentNode(
                                            tag="div",
                                            children=[
                                                LeafNode("h3", "Level 3")
                                            ],
                                            props={"class" : "CDs", "id" : "CDs"}
                                        )
                                    ],
                                    props={"class" : "ligma", "id" : "ligma"}
                                )
                            ],
                            props={"class" : "BOBA", "id" : "BOBA"}
        )
        self.assertEqual(pNode2.to_html(), '<div class="BOBA" id="BOBA"><div class="ligma" id="ligma"><h2>Level 2</h2><div class="CDs" id="CDs"><h3>Level 3</h3></div></div></div>')
        self.assertEqual(pNode.to_html(), '<div class="big-L" id="big-L"><div class="hugh-mungus" id="hugh-mungus"><h2>Level 2</h2><b class="YUP" id="YUP">some properties here</b></div></div>')

if __name__ == "__main__":
    unittest.main()