from textnode import TextNode, TextType

def main():
    textnode = TextNode('This is some anchor text', TextType.link, 'https://www.boot.dev')

    print(textnode)

main()
