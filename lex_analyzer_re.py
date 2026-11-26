import re
from collections import Counter

KEYWORDS = {"if", "else", "while", "int", "float","farouk"}

TOKEN_SPECIFICATION = [
    ("COMMENT", r"//[^\n]*"),
    ("NUMALPHA", r"[0-9]+[A-Za-z_]+[0-9-A-Za-z_]*"),
    ("NUMBER", r"\d+(\.\d+)?"),
    ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OPERATOR", r"==|!=|<=|>=|[+\-*/<>]"),
    ("ASSIGNMENT", r"="),
    ("SEPARATOR", r"[;,(){}]"),
    ("WHITESPACE", r"\s+"),
    ("INVALID", r"."),
]

def lexical_analysis(source_code):
    tokens = []
    errors = []

    pattern = "|".join(
        f"(?P<{name}>{regex})"
        for name, regex in TOKEN_SPECIFICATION
    )

    line = 1
    column = 1

    for match in re.finditer(pattern, source_code):
        token_type = match.lastgroup
        lexeme = match.group()

        start_line = line
        start_column = column

        if token_type not in ("COMMENT", "WHITESPACE"):

            if token_type == "INVALID":
                errors.append(
                    f"Lexical error: {lexeme!r} "
                    f"at line {start_line}, column {start_column}"
                )
            elif token_type == "NUMALPHA":
                            errors.append(
                                f"Lexical error: {lexeme!r} "
                                f"at line {start_line}, column {start_column}"
                            )
            else:
                
                if token_type == "IDENTIFIER" and lexeme in KEYWORDS:
                    token_type = "KEYWORD"

                if token_type == "NUMBER":
                    if "." in lexeme:
                        token_type = "REAL"
                    else:
                        token_type = "INTEGER"
                        if len(lexeme) > 1 and lexeme[0] == "0":
                            errors.append(
                                            f"Lexical error: {lexeme!r} "
                                            f"at line {start_line}, column {start_column} "
                                            f"you can't start an INTEGER with 0"
                                            )
                            continue

                
                tokens.append((token_type, lexeme, start_line))

        
        if "\n" in lexeme:
            line += lexeme.count("\n")
            column = len(lexeme.rsplit("\n", 1)[-1]) + 1
        else:
            column += len(lexeme)

    statistics = Counter(token[0] for token in tokens)

    return tokens, errors, statistics


source = """int x = 010; // initialize x
float y@ = 2.5;
1farouk = 0;"""

tokens, errors, statistics = lexical_analysis(source)

print("TOKENS:")
for token in tokens:
    print(f"{token=}")

print("\nLEXICAL ERRORS:")
if errors:
    for error in errors:
        print(error)
else:
    print("No lexical errors.")

print("\nTOKEN STATISTICS:")
print("Total tokens:", len(tokens))

for token_type, count in sorted(statistics.items()):
    print(f"{token_type}: {count}")