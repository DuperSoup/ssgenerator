from textnode import *


def main():
    testnode = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(testnode.__repr__())


if __name__ == "__main__":
    main()