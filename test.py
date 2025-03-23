from scanner import Scanner, InvalidTokenException, Token

def testScannerSimpleExpression():
    sc = Scanner()

    exp = "(5+6)/7*8*a"

    res = sc.scanAll(exp)

    assert res == [
        (0, Token.BRACKET, "("),
        (1, Token.INTEGER, "5"),
        (2, Token.OPERATOR, "+"),
        (3, Token.INTEGER, "6"),
        (4, Token.BRACKET, ")"),
        (5, Token.OPERATOR, "/"),
        (6, Token.INTEGER, "7"),
        (7, Token.OPERATOR, "*"),
        (8, Token.INTEGER, "8"),
        (9, Token.OPERATOR, "*"),
        (10, Token.IDENTIFIER, "a")
    ]


def testScannerWithWhitespace():
    sc = Scanner()

    exp = "\n5 + 6  \t"

    res = sc.scanAll(exp)

    assert res == [
        (1, Token.INTEGER, "5"),
        (3, Token.OPERATOR, "+"),
        (5, Token.INTEGER, "6")
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