class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        attribute_string = ""

        for key, value in self.props.items():
            temp = f' {key}="{value}"'

            attribute_string += temp

        return attribute_string

    def __repr__(self):
        return (
            f"tag: {self.tag}\n"
            f"value: {self.value}\n"
            f"children: {self.children}\n"
            f"props: {self.props}\n"
        )

    def __eq__(self, value: object) -> bool:

        return (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes require a value!")

        if self.tag == None:
            return self.value

        beginning_tag = (
            f"<{self.tag}{self.props_to_html()}>"
            if self.props is not None
            else f"<{self.tag}>"
        )
        ending_tag = f"</{self.tag}>"

        return beginning_tag + self.value + ending_tag

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, value: object) -> bool:
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.props == value.props
        )


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Value Error: no Tag provided")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Value Error: no children provided")

        s = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            s += child.to_html()

        return s + f"</{self.tag}>"

    def __repr__(self):
        return f"Parent Node({self.tag}, {self.children}, {self.props})"

    def __eq__(self, value: object) -> bool:
        return (
            self.tag == value.tag
            and self.props == value.props
            and self.children == value.children
        )


def main():
    # testing repr
    hNode = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
    lNode = LeafNode("a", "some hyper link here", {"href": "something.com"})
    # print(hNode)
    # print(lNode)


if __name__ == "__main__":
    main()
