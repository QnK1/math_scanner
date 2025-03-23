from enum import Enum
import sys
import dataclasses

class InvalidTokenException(Exception):
    pass


class Token(Enum):
        INTEGER = 1
        OPERATOR = 2
        BRACKET = 3
        IDENTIFIER = 4
        KEYWORD = 5
        NONE = 6


@dataclasses.dataclass(frozen=True)
class State:
    accepts: Token
    id: int


@dataclasses.dataclass(frozen=True)
class Edge:
    goal: State
    chars: set[str]


ZERO_TO_NINE = {str(i) for i in range(0, 10)}
ONE_TO_NINE = {str(i) for i in range(1, 10)}
OPERATORS = {'+', '-', '*', '/'}
LOWERCASE = {chr(i) for i in range(97, 123)}
UPPERCASE = {chr(i) for i in range(65, 91)}

class DFA:
    def __init__(self):
        self.states = [
            State(Token.NONE, 0),
            State(Token.INTEGER, 1),
            State(Token.OPERATOR, 2),
            State(Token.IDENTIFIER, 3),
            State(Token.NONE, 4),
            State(Token.KEYWORD, 5),
            State(Token.BRACKET, 6),
            State(Token.NONE, 7),
            State(Token.NONE, 8),
            State(Token.KEYWORD, 9),
            State(Token.NONE, 10),
        ]
        self.currentState = self.states[0]
        self.edges = {
            self.states[0] : [
                Edge(self.states[1], ONE_TO_NINE),
                Edge(self.states[2], OPERATORS),
                Edge(self.states[3], (LOWERCASE | UPPERCASE | {'_'}) - {'i', 'f'}),
                Edge(self.states[4], {'i'}),
                Edge(self.states[6], {'(', ')'}),
                Edge(self.states[7], {'f'}),
            ],
            self.states[1] : [
                Edge(self.states[1], ZERO_TO_NINE),
            ],
            self.states[3] : [
                Edge(self.states[3], LOWERCASE | UPPERCASE | ZERO_TO_NINE | {'_'}),
            ],
            self.states[4] : [
                Edge(self.states[5], {'f'}),
                Edge(self.states[3], (UPPERCASE | LOWERCASE | ZERO_TO_NINE | {'_'} - {'f'})),
            ],
            self.states[5] : [
                Edge(self.states[3], LOWERCASE | UPPERCASE | ZERO_TO_NINE | {'_'}),
            ],
            self.states[7] : [
                Edge(self.states[8], {'o'}),
            ],
            self.states[8] : [
                Edge(self.states[9], {'r'}),
            ],
        }
    
    def move(self, char: str):
        edgeFound = False
        
        if self.currentState in self.edges.keys():
            for e in self.edges[self.currentState]:
                if char in e.chars:
                    self.currentState = e.goal
                    edgeFound = True
                    break
        
        return self.currentState if edgeFound else self.states[10]

class Scanner:
    def __init__(self):
        self.tokens = {t for t in Token}


    def _scanNext(self, input):
        dfa = DFA()

        index = 0
        for i, c in enumerate(input):
            index = i
            prevState = dfa.currentState

            state = dfa.move(c)

            if state.id == 10:
                break
        
        if state.accepts != Token.NONE:
            return input[:index + 1], index, state.accepts
        elif prevState.accepts != Token.NONE:
            # print(input[:index], index - 1, prevState.accepts)
            return input[:index], index - 1, prevState.accepts
        else:
            return None
        

    def scanAll(self, input: str) -> tuple[int, Token, str]:
        tokens = []
        
        i = 0
        while i < len(input):
            while i < len(input) and input[i] in {' ', '\n', '\t'}:
                i += 1

            if i >= len(input):
                break
            
            token = self._scanNext(input[i:])

            if token == None:
                raise InvalidTokenException(f"Invalid token at {i}")
            
            tokens.append((i, token[2], token[0]))
            i += token[1] + 1
        
        return tokens


if __name__ == "__main__":
    input = str(sys.argv[1])
    print(input)
    
    scanner = Scanner()
    tokens = scanner.scanAll(input)

    for t in tokens:
        print(f"i: {t[0]}, token: {t[1].name}, value: {t[2]}")

