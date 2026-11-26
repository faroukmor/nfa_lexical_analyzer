from collections import Counter

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
IDENTIFIER_CHARS = LETTERS + DIGITS + "_"
WHITESPACES = " \t\n\r"

KEYWORDS = {"if", "else", "while", "int", "float", "farouk"}

EPSILON = None  

CHAR_CLASSES = {
    "LETTER": LETTERS,
    "DIGIT": DIGITS,
    "IDENTIFIER_CHAR": IDENTIFIER_CHARS,
    "WHITESPACE": WHITESPACES,
    "SINGLE_OPERATOR": "+-*/<>",
    "DOUBLE_OPERATOR": "<>=!",
}

class NFA:

    def __init__(self, transitions, start, final):
        """
        M = (Q, Σ, δ, q0, F)
        Q: مجموعة الحالات.
        δ: دالة الانتقال  {state: [(symbol, next_state), ...]}
        q0: الحالة الابتدائية.
        F: مجموعة الحالات النهائية.
        """
        self.transitions = transitions
        self.start = start
        self.final = final
        self.states = (
            {start} | set(final) | set(transitions)
            | {t for arcs in transitions.values() for _, t in arcs}
        )

    def matches(self, label, char):
        if label == "NOT_NEWLINE":
            return char != "\n"
        if label in CHAR_CLASSES:
            return char in CHAR_CLASSES[label]
        return char == label

    def epsilon_closure(self, states): # تحددلنا التنقلات لي نقدرو نوصلولهم بلاما نستخدمواي حرف 
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for symbol, nxt in self.transitions.get(state, []):
                if symbol is EPSILON and nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)

        return closure

    def run(self, source, start):
        current = self.epsilon_closure({self.start})
        last_accepted = start if current & self.final else None

        for i in range(start, len(source)):
            next_states = {
                target
                for state in current
                for symbol, target in self.transitions.get(state, [])
                if symbol is not EPSILON and self.matches(symbol, source[i])
            }

            if not next_states:
                break

            current = self.epsilon_closure(next_states)

            if current & self.final:
                last_accepted = i + 1

        if last_accepted is None:
            return None
        return source[start:last_accepted], last_accepted


def one_or_more(label):
    """NFA INTEGER , WHITESPACE"""
    return NFA(
        {"q0": [(label, "q1")], "q1": [(label, "q1")]},
        "q0", {"q1"},
    )



def create_keyword_nfa():
    transitions = {"q0": []}
    final = set()

    for index, word in enumerate(sorted(KEYWORDS)):
        previous = f"k{index}_0"
        transitions["q0"].append((EPSILON, previous))

        for j, char in enumerate(word):
            nxt = f"k{index}_{j + 1}"
            transitions.setdefault(previous, []).append((char, nxt))
            previous = nxt

        final.add(previous)

    return NFA(transitions, "q0", final)


def create_identifier_nfa():
    return NFA(
        {
            "q0": [("LETTER", "q1"), ("_", "q1")],
            "q1": [("IDENTIFIER_CHAR", "q1")],
        },
        "q0", {"q1"},
    )


def create_integer_nfa():
    return one_or_more("DIGIT")


def create_real_nfa():
    return NFA(
        {
            "q0": [("DIGIT", "q1")],
            "q1": [("DIGIT", "q1"), (".", "q2")],
            "q2": [("DIGIT", "q3")],
            "q3": [("DIGIT", "q3")],
        },
        "q0", {"q3"},
    )


def create_numalpha_nfa():
    return NFA(
        {
            "q0": [("DIGIT", "q1")],
            "q1": [("DIGIT", "q1"), ("LETTER", "q2"), ("_", "q2")],
            "q2": [("IDENTIFIER_CHAR", "q2")],
        },
        "q0", {"q2"},
    )


def create_operator_nfa():
    return NFA(
        {
            "q0": [(EPSILON, "q1"), (EPSILON, "q2")],
            "q1": [("SINGLE_OPERATOR", "q4")],   # + - * / < >
            "q2": [("DOUBLE_OPERATOR", "q3")],   # < > = !
            "q3": [("=", "q4")],                 # <= >= == !=
        },
        "q0", {"q4"},
    )


def create_assignment_nfa():
    return NFA({"q0": [("=", "q1")]}, "q0", {"q1"})


def create_separator_nfa():
    return NFA({"q0": [(c, "q1") for c in ";,(){}"]}, "q0", {"q1"})


def create_comment_nfa():
    return NFA(
        {
            "q0": [("/", "q1")],
            "q1": [("/", "q2")],
            "q2": [("NOT_NEWLINE", "q2")],
        },
        "q0", {"q2"},
    )


def create_whitespace_nfa():
    return one_or_more("WHITESPACE")


AUTOMATA = [
    ("WHITESPACE", create_whitespace_nfa()),
    ("COMMENT", create_comment_nfa()),
    ("KEYWORD", create_keyword_nfa()),
    ("IDENTIFIER", create_identifier_nfa()),
    ("NUMALPHA", create_numalpha_nfa()),
    ("REAL", create_real_nfa()),
    ("INTEGER", create_integer_nfa()),
    ("OPERATOR", create_operator_nfa()),
    ("ASSIGNMENT", create_assignment_nfa()),
    ("SEPARATOR", create_separator_nfa()),
]

IGNORED = {"COMMENT", "WHITESPACE"}


def error_message(token_type, lexeme):
    if token_type == "NUMALPHA":
        return "IDENTIFIER cannot start with a number"
    if token_type == "INTEGER" and len(lexeme) > 1 and lexeme[0] == "0":
        return "INTEGER cannot start with 0"
    return None

def lexical_analysis(source):
    tokens, errors = [], []
    i, line, column = 0, 1, 1

    while i < len(source):

        best_type, best_end = None, i
        for token_type, automaton in AUTOMATA:
            result = automaton.run(source, i)
            if result and result[1] > best_end:
                best_type, best_end = token_type, result[1]

        if best_type is None:
            errors.append(
                f"Lexical error: {source[i]!r} at line {line}, column {column}"
            )
            i += 1
            column += 1
            continue

        lexeme = source[i:best_end]
        message = error_message(best_type, lexeme)

        if message:
            errors.append(
                f"Lexical error: {lexeme!r} at line {line}, "
                f"column {column}: {message}"
            )
        elif best_type not in IGNORED:
            tokens.append((best_type, lexeme, line))

        newlines = lexeme.count("\n")
        if newlines:
            line += newlines
            column = len(lexeme) - lexeme.rfind("\n")
        else:
            column += len(lexeme)

        i = best_end

    statistics = Counter(token[0] for token in tokens)
    return tokens, errors, statistics


def main():
    source = """int ab = 0;
    integer 0bc = 11;
    khalil = 011;
    drif = gg"""

    tokens, errors, statistics = lexical_analysis(source)

    print("TOKENS:")
    for token in tokens:
        print(token)

    print("\nLEXICAL ERRORS:")
    print("\n".join(errors) if errors else "No lexical errors.")

    print("\nTOKEN STATISTICS:")
    print("Total tokens:", len(tokens))
    for token_type, count in sorted(statistics.items()):
        print(f"{token_type}: {count}")


if __name__ == "__main__":
    main()