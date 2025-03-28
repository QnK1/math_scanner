from scanner import Scanner, Token

class SyntaxHighlighter:
    def __init__(self):
        self.scanner = Scanner()
        self.syntaxMapping = {
            Token.BRACKET : lambda x: f"<span style=\"color: grey;\">{x}</span>",
            Token.KEYWORD : lambda x: f"<span style=\"color: purple;\">{x}</span>",
            Token.INTEGER : lambda x: f"<span style=\"color: orange;\">{x}</span>",
            Token.IDENTIFIER : lambda x: f"<span style=\"color: yellow;\">{x}</span>",
            Token.OPERATOR : lambda x: f"<span style=\"color: lightblue;\">{x}</span>",
        }
    

    def highlightSyntax(self, fileInName, fileOutName):
        with open(fileInName, 'r') as fIn:
            text = fIn.read()
            print(text)

            res = self.scanner.scanAll(text)

            new = ""
            prevEnd = -1
            for t in res:
                new += text[prevEnd + 1:t[0]] + self.syntaxMapping[t[1]](t[2]) 
                prevEnd = t[0] + len(t[2]) - 1
            
            text = new
            text = text.replace('\n','<br>')
            
            with open(fileOutName, 'w') as fOut:
                fOut.write("<body style=\"background: #111;\">")
                fOut.write(text)
                fOut.write("</body>")


if __name__ == "__main__":
    syntaxHighlighter = SyntaxHighlighter()

    syntaxHighlighter.highlightSyntax("in.txt", "out.html")

