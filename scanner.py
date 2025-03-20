import re
from enum import Enum
import sys

class InvalidTokenException(Exception):
    pass


class Scanner:
    class Token(Enum):
        INTEGER = 1
        OPERATOR = 2
        BRACKET = 3
        IDENTIFIER = 4
    
    def __init__(self):
        self.tokens = {t for t in self.Token}

        # conditions for when a character c at position i doesn't make the given token invalid
        self.conditions = {
            self.Token.OPERATOR : lambda i, c: (i == 0 and c in {'+', '-', '*', '/'}),
            self.Token.BRACKET: lambda i, c: (i == 0 and c in {'(', ')'}),
            self.Token.INTEGER: lambda i, c: (ord(c) in range(48, 58) and not (i == 0 and c == '0')),
            self.Token.IDENTIFIER: lambda i, c: (ord(c) in range(65, 91) or ord(c) in range(97,123) or c == "_" or ord(c) in range(48, 58)
                                                    and not (i == 0 and ord(c) in range(48, 58))),
        }
    

    def _removeWhitespace(self, string: str) -> str:
        output: str = re.sub(r"\s", "", string)
        return output


    def _scanNext(self, input: str):
        possibleTokens = self.tokens.copy()
        possibleTokensHistory = []

        for i, c in enumerate(input):
            for key in self.Token:
                if not self.conditions[key](i, c):
                    possibleTokens.discard(key)
            
            possibleTokensHistory.append((i, possibleTokens.copy()))
        
        for historyInstance in reversed(possibleTokensHistory):
            tset = historyInstance[1]
            index = historyInstance[0]
            if len(tset) == 1:
                return index, [t for t in tset][0], input[:index + 1]

        return None
        
    
    def scanAll(self, input: str):
        tokens = []


        i = 0
        error = False
        while i != len(input):
            while input[i] in " \t\n":
                i += 1
                if i == len(input):
                    return tokens
            
            lastScan = self._scanNext(input[i:])

            if lastScan == None:
                error = True
                break
            else:
                _, token, v = lastScan
                
                tokens.append((i, token, v))
                # print(f"i: {i}, token: {token.name}, value: {v}")
                i += lastScan[0] + 1
                
        if error:
            # print(f"There was an error at {i}")
            raise InvalidTokenException(f"There was an error at {i}")

        return tokens


if __name__ == "__main__":
    input = str(sys.argv[1])
    print(input)
    
    scanner = Scanner()
    tokens = scanner.scanAll(input)

    for t in tokens:
        print(f"i: {t[0]}, token: {t[1].name}, value: {t[2]}")

