from scanner import Scanner, InvalidTokenException

def testScannerSimpleExpression():
    sc = Scanner()

    exp = "(5+6)/7*8*a"

    res = sc.scanAll(exp)

    assert res == [
        (0, Scanner.Token.BRACKET, "("),
        (1, Scanner.Token.INTEGER, "5"),
        (2, Scanner.Token.OPERATOR, "+"),
        (3, Scanner.Token.INTEGER, "6"),
        (4, Scanner.Token.BRACKET, ")"),
        (5, Scanner.Token.OPERATOR, "/"),
        (6, Scanner.Token.INTEGER, "7"),
        (7, Scanner.Token.OPERATOR, "*"),
        (8, Scanner.Token.INTEGER, "8"),
        (9, Scanner.Token.OPERATOR, "*"),
        (10, Scanner.Token.IDENTIFIER, "a")
    ]


def testScannerWithWhitespace():
    sc = Scanner()

    exp = "\n5 + 6  \t"

    res = sc.scanAll(exp)

    assert res == [
        (1, Scanner.Token.INTEGER, "5"),
        (3, Scanner.Token.OPERATOR, "+"),
        (5, Scanner.Token.INTEGER, "6")
    ]


def testScannerInvalidToken():
    sc = Scanner()

    exp = "&"

    exception_thrown = False

    try:
        sc.scanAll(exp)
    except InvalidTokenException:
        exception_thrown = True
    

    assert exception_thrown == True


if __name__ == "__main__":
    testScannerSimpleExpression()
    testScannerWithWhitespace()
    testScannerInvalidToken()