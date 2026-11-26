# Lexical Analysis Project
## Technical Report and Code Documentation

**Course:** Compilation  
**Project Topic:** Lexical Analysis Using Regular Expressions and Non-Deterministic Finite Automata (NFA)  
**Programming Language:** Python 3

---

# Table of Contents

1. Introduction
2. Project Objectives
3. Project Structure
4. General Concepts of Lexical Analysis
5. Implementation 1: Regular Expressions
   - 5.1. Required Libraries
   - 5.2. Keywords Definition
   - 5.3. Token Specification
   - 5.4. Input and Initialization
   - 5.5. Regular Expression Construction
   - 5.6. Source Code Scanning
   - 5.7. Token Classification
   - 5.8. Lexical Error Detection
   - 5.9. Line and Column Tracking
   - 5.10. Token Statistics
   - 5.11. Program Output
6. Implementation 2: Non-Deterministic Finite Automata
   - 6.1. Character Definitions
   - 6.2. The NFA Class
   - 6.3. NFA Simulation
   - 6.4. Epsilon Closure
   - 6.5. Automata Construction
   - 6.6. Token Automata
   - 6.7. Automata Organization
   - 6.8. Longest Match Rule
   - 6.9. Lexical Analysis Process
   - 6.10. Error Handling
   - 6.11. Program Output
7. Input and Output Specifications
8. Practical Execution Examples
9. Comparison Between the Two Implementations
10. Limitations and Observations
11. Conclusion

---

# 1. Introduction

Lexical analysis is the first phase of a compiler. Its main responsibility is to read a sequence of characters representing source code and transform it into a sequence of meaningful units called **tokens**.

A token represents a category of lexical elements, such as:

- Keywords
- Identifiers
- Integer numbers
- Real numbers
- Operators
- Assignment symbols
- Separators
- Comments
- Whitespace

During this process, the lexical analyzer also detects invalid character sequences and reports lexical errors.

This project implements two lexical analyzers in Python using two different approaches:

**Implementation 1: Regular Expressions**

The first program uses Python's built-in `re` module to define token patterns and identify lexical elements.

**Implementation 2: Non-Deterministic Finite Automata (NFA)**

The second program constructs individual automata for different token categories and simulates their state transitions to recognize tokens.

Both implementations analyze source code, identify tokens, detect lexical errors, and calculate token statistics.

# 2. Project Objectives

The main objectives of this project are:

1. Understand the role of lexical analysis in the compilation process.
2. Identify different lexical elements in a source program.
3. Implement token recognition using Regular Expressions.
4. Implement token recognition using Non-Deterministic Finite Automata.
5. Understand states, transitions, initial states, and accepting states.
6. Implement epsilon transitions and epsilon closure.
7. Apply the Longest Match Rule when recognizing tokens.
8. Detect invalid lexical sequences.
9. Track source code positions using line and column numbers.
10. Generate statistics about recognized tokens.

# 3. Project Structure

The project contains three files:

```text
cmp_tp_farouk/
│
├── lex_analyzer_re.py
│
├── nfa_lex_analyzer.py
│
└── exo_answers_farouk.pdf
```

| File | Responsibility |
|---|---|
| `lex_analyzer_re.py` | Implements lexical analysis using Regular Expressions. |
| `nfa_lex_analyzer.py` | Implements lexical analysis using manually constructed NFAs. |
| `exo_answers_farouk.pdf` | Contains the PDF exercise answers. |

The two Python files are independent implementations. Each one contains its own input example, lexical analysis function, error detection, and output generation.

---

# 4. General Concepts of Lexical Analysis

Before explaining the implementations, it is important to understand the main concepts used in both programs.

## 4.1. Source Code

The source code is the input text that the lexical analyzer processes.

For example:

```c
int number = 25;
float price = 12.5;
```

The analyzer reads this text character by character or through pattern matching, depending on the implementation.

## 4.2. Lexeme

A lexeme is the actual sequence of characters recognized by the lexical analyzer.

For example, in:

```c
int number = 25;
```

The lexemes are:

```text
int
number
=
25
;
```

## 4.3. Token

A token is the category assigned to a recognized lexeme.

For example:

| Lexeme | Token Type |
|---|---|
| `int` | KEYWORD |
| `number` | IDENTIFIER |
| `=` | ASSIGNMENT |
| `25` | INTEGER |
| `;` | SEPARATOR |

## 4.4. Lexical Error

A lexical error occurs when a sequence of characters violates the lexical rules defined by the analyzer.

Examples in this project include:

```c
010
1farouk
@
```

These sequences are reported as lexical errors according to the implemented rules.

## 4.5. Token Statistics

At the end of the analysis, both programs calculate how many tokens were recognized in each category.

For example:

```text
KEYWORD: 2
IDENTIFIER: 3
INTEGER: 2
```

Comments and whitespace are excluded from the token statistics.

---

# 5. Implementation 1: Lexical Analysis Using Regular Expressions

**Source File:** `lex_analyzer_re.py`

## 5.1. Required Libraries

The program begins by importing two Python libraries:

```python
import re
from collections import Counter
```

### `re`

The `re` module provides support for Regular Expressions.

It is used to define patterns and search for matching sequences in the source code.

### `Counter`

`Counter` is imported from `collections`.

It counts the occurrences of different token types after lexical analysis.

Both libraries are included in Python's standard library, so no external installation is necessary.

## 5.2. Keywords Definition

```python
KEYWORDS = {"if", "else", "while", "int", "float", "farouk"}
```

This variable contains the reserved words recognized by the language.

A keyword is a predefined word with a special meaning.

For example:

```c
int x;
if (x > 0)
```

The words `int` and `if` are recognized as keywords.

The program initially recognizes words matching the identifier pattern as `IDENTIFIER`. It then checks whether their lexemes belong to the `KEYWORDS` set.

If a match is found, the token type is changed to `KEYWORD`.

## 5.3. Token Specification

The program defines the supported token patterns in a list named `TOKEN_SPECIFICATION`.

```python
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
```

Each element contains:

1. A token name.
2. A regular expression describing the characters accepted for that token.

### A. COMMENT

```python
("COMMENT", r"//[^\n]*")
```

Recognizes single-line comments.

Explanation:

- `//` identifies the beginning of a comment.
- `[^\n]` matches any character except a newline.
- `*` allows zero or more repetitions.

Example:

```c
// This is a comment
```

Comments are recognized but not included in the final token list.

### B. NUMALPHA

```python
("NUMALPHA", r"[0-9]+[A-Za-z_]+[0-9-A-Za-z_]*")
```

Recognizes sequences that begin with digits and are followed by letters or underscores.

Examples:

```text
123abc
1farouk
25_name
```

These sequences are treated as lexical errors because an identifier cannot start with a number under the implemented rules.

### C. NUMBER

```python
("NUMBER", r"\d+(\.\d+)?")
```

Recognizes integer and decimal numeric sequences.

Explanation:

- `\d+` matches one or more digits.
- `\.` matches a decimal point.
- `?` makes the decimal part optional.

Examples:

```text
25
100
12.5
3.14
```

The program later classifies these matches into `INTEGER` or `REAL`.

### D. IDENTIFIER

```python
("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*")
```

Recognizes identifiers such as variable names.

Rules:

- The first character must be a letter or underscore.
- The remaining characters can be letters, digits, or underscores.

Examples:

```text
number
student1
_myVariable
```

### E. OPERATOR

```python
("OPERATOR", r"==|!=|<=|>=|[+\-*/<>]")
```

Recognizes arithmetic and comparison operators.

Examples:

```text
+
-
*
/
<
>
==
!=
<=
>=
```

The multi-character operators are placed before the single-character alternatives to prioritize their recognition.

### F. ASSIGNMENT

```python
("ASSIGNMENT", r"=")
```

Recognizes the assignment operator.

Example:

```c
x = 10;
```

The symbol `=` is classified as `ASSIGNMENT`.

### G. SEPARATOR

```python
("SEPARATOR", r"[;,(){}]")
```

Recognizes punctuation symbols used to separate instructions and expressions.

Supported symbols:

```text
;
,
(
)
{
}
```

### H. WHITESPACE

```python
("WHITESPACE", r"\s+")
```

Recognizes one or more whitespace characters.

Examples include:

- Spaces
- Tabs
- Newlines

These characters are necessary for formatting source code but are ignored in the final token list.

### I. INVALID

```python
("INVALID", r".")
```

Recognizes any character not matched by the preceding token patterns.

It acts as a fallback pattern that allows the analyzer to report unrecognized characters instead of silently ignoring them.

Example:

```text
@
```

The character `@` generates a lexical error.

## 5.4. Input and Initialization

The main function responsible for processing the input is:

```python
def lexical_analysis(source_code):
```

It receives one parameter:

- `source_code`: A string containing the source program to analyze.

At the beginning, two empty lists are created:

```python
tokens = []
errors = []
```

Their purposes are:

| Variable | Purpose |
|---|---|
| `tokens` | Stores valid recognized tokens. |
| `errors` | Stores lexical error messages. |

The program also initializes the source position:

```python
line = 1
column = 1
```

Both counters start at 1 because the first character is located at line 1, column 1.

## 5.5. Building the Combined Regular Expression

Instead of processing every regular expression separately, the program combines all token patterns into one expression.

```python
pattern = "|".join(
    f"(?P<{name}>{regex})"
    for name, regex in TOKEN_SPECIFICATION
)
```

The `|` symbol represents alternation, meaning that a match can correspond to one of several alternatives.

The expression:

```python
(?P<NAME>REGEX)
```

creates a named capturing group.

This allows the program to identify which token pattern matched.

For example, a recognized integer can be associated with the `NUMBER` group.

## 5.6. Scanning the Source Code

The following instruction performs the actual scanning:

```python
for match in re.finditer(pattern, source_code):
```

`re.finditer()` searches the source code for successive non-overlapping matches.

For every match, the program extracts two values:

```python
token_type = match.lastgroup
lexeme = match.group()
```

- `match.lastgroup` returns the name of the matched token pattern.
- `match.group()` returns the actual matched characters.

For example, if the source contains:

```c
int x = 10;
```

One iteration may produce:

```text
token_type = IDENTIFIER
lexeme = x
```

The program also saves the current source position:

```python
start_line = line
start_column = column
```

These values are used when generating lexical errors.

## 5.7. Token Classification

After identifying a lexeme, the program determines whether it should be ignored, reported as an error, or added to the token list.

### A. Ignoring Comments and Whitespace

```python
if token_type not in ("COMMENT", "WHITESPACE"):
```

The program excludes comments and whitespace from the final token list.

### B. Recognizing Keywords

```python
if token_type == "IDENTIFIER" and lexeme in KEYWORDS:
    token_type = "KEYWORD"
```

If an identifier matches a reserved word, its category is changed to `KEYWORD`.

### C. Classifying Numbers

```python
if token_type == "NUMBER":
    if "." in lexeme:
        token_type = "REAL"
    else:
        token_type = "INTEGER"
```

The program checks whether the recognized number contains a decimal point.

- If it contains `.`, it becomes `REAL`.
- Otherwise, it becomes `INTEGER`.

For example:

| Lexeme | Final Type |
|---|---|
| `10` | INTEGER |
| `0` | INTEGER |
| `2.5` | REAL |
| `100.75` | REAL |

### D. Storing Tokens

```python
tokens.append((token_type, lexeme, start_line))
```

Valid tokens are stored as tuples containing three elements:

```text
(Token Type, Lexeme, Line Number)
```

Example:

```python
("INTEGER", "25", 1)
```

## 5.8. Lexical Error Detection

The first implementation detects three types of lexical errors.

### A. Invalid Characters

```python
if token_type == "INVALID":
```

If a character matches the `INVALID` pattern, the program generates an error message.

Example:

```text
Lexical error: '@' at line 2, column 8
```

### B. Identifiers Starting With Numbers

```python
elif token_type == "NUMALPHA":
```

If a sequence starts with digits and continues with letters or underscores, it is reported as a lexical error.

Example:

```text
1farouk
```

### C. Integers Starting With Zero

```python
if len(lexeme) > 1 and lexeme[0] == "0":
```

The program rejects integer numbers that contain multiple digits and start with zero.

Example:

```text
010
```

The generated error is:

```text
Lexical error: '010' at line 1, column 9 you can't start an INTEGER with 0
```

The instruction `continue` prevents this invalid integer from being added to the token list.

## 5.9. Line and Column Tracking

After processing a lexeme, the program updates its current position.

```python
if "\n" in lexeme:
    line += lexeme.count("\n")
    column = len(lexeme.rsplit("\n", 1)[-1]) + 1
else:
    column += len(lexeme)
```

Two situations are handled.

**Case 1: The lexeme contains a newline.**

The program:

1. Counts the newline characters.
2. Increases the line number.
3. Calculates the column after the last newline.

**Case 2: The lexeme does not contain a newline.**

The column is increased by the length of the lexeme.

This mechanism allows the analyzer to report the location of lexical errors.

## 5.10. Calculating Token Statistics

After scanning the complete source code, the program executes:

```python
statistics = Counter(token[0] for token in tokens)
```

The expression `token[0]` extracts the token type from each tuple.

`Counter` then counts how many tokens belong to each category.

For example:

```text
KEYWORD: 2
IDENTIFIER: 3
INTEGER: 4
```

Finally, the function returns:

```python
return tokens, errors, statistics
```

The three returned objects are:

1. Recognized tokens.
2. Lexical errors.
3. Token statistics.

## 5.11. Main Program and Input Data

At the bottom of the file, the program defines its test input:

```python
source = """int x = 010; // initialize x
float y@ = 2.5;
1farouk = 0;"""
```

This input contains several examples designed to test the analyzer.

| Input | Purpose |
|---|---|
| `int` | Tests keyword recognition. |
| `x` | Tests identifier recognition. |
| `=` | Tests assignment recognition. |
| `010` | Tests the leading-zero error. |
| `// initialize x` | Tests comment recognition and ignoring. |
| `float` | Tests another keyword. |
| `y` | Tests identifier recognition. |
| `@` | Tests invalid-character detection. |
| `2.5` | Tests real-number recognition. |
| `1farouk` | Tests identifiers beginning with numbers. |
| `0` | Tests a valid single-digit integer. |

The input is passed to the analyzer:

```python
tokens, errors, statistics = lexical_analysis(source)
```

The results are then displayed.

## 5.12. Output Generation

The program prints three main sections.

### A. TOKENS

Displays all valid recognized tokens.

Each token contains:

```text
Token Type
Lexeme
Line Number
```

### B. LEXICAL ERRORS

Displays every detected lexical error.

If no errors exist, the program prints:

```text
No lexical errors.
```

### C. TOKEN STATISTICS

Displays:

- Total number of valid tokens.
- Number of occurrences of each token type.

The statistics are sorted alphabetically by token type.

---

# 6. Implementation 2: Lexical Analysis Using NFA

**Source File:** `nfa_lex_analyzer.py`

The second implementation performs the same general task using Non-Deterministic Finite Automata instead of regular expression matching.

Unlike the first implementation, it explicitly defines states and transitions for each token category.

## 6.1. Required Library

```python
from collections import Counter
```

The program only imports `Counter`.

It uses this class to calculate token statistics.

All automata and their simulation mechanisms are implemented manually in Python.

## 6.2. Character Definitions

The program starts by defining the character groups:

```python
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
IDENTIFIER_CHARS = LETTERS + DIGITS + "_"
WHITESPACES = " \t\n\r"
```

These variables simplify the construction of the automata.

| Variable | Description |
|---|---|
| `LETTERS` | Uppercase and lowercase English letters. |
| `DIGITS` | Numeric characters from 0 to 9. |
| `IDENTIFIER_CHARS` | Letters, digits, and underscores. |
| `WHITESPACES` | Space, tab, newline, and carriage return. |

The keyword set is also defined:

```python
KEYWORDS = {"if", "else", "while", "int", "float", "farouk"}
```

The constant:

```python
EPSILON = None
```

represents an epsilon transition.

An epsilon transition allows an automaton to move from one state to another without consuming an input character.

## 6.3. Character Classes

```python
CHAR_CLASSES = {
    "LETTER": LETTERS,
    "DIGIT": DIGITS,
    "IDENTIFIER_CHAR": IDENTIFIER_CHARS,
    "WHITESPACE": WHITESPACES,
    "SINGLE_OPERATOR": "+-*/<>",
    "DOUBLE_OPERATOR": "<>=!",
}
```

This dictionary associates symbolic labels with groups of characters.

For example:

```python
("DIGIT", "q1")
```

means that the transition can be followed when the current character is a digit.

This approach avoids writing separate transitions for every digit or letter.

---

# 7. The NFA Class

The most important component of the second implementation is the `NFA` class.

```python
class NFA:
```

It provides a reusable structure for defining and simulating finite automata.

Instead of implementing a separate simulation algorithm for every token, the program uses one general-purpose NFA class.

## 7.1. Mathematical Representation

A finite automaton is represented by:

\[
M = (Q,\Sigma,\delta,q_0,F)
\]

Where:

- \(Q\): Set of states.
- \(\Sigma\): Input alphabet.
- \(\delta\): Transition function.
- \(q_0\): Initial state.
- \(F\): Set of accepting states.

The class stores these elements through its attributes.

## 7.2. Constructor: `__init__()`

```python
def __init__(self, transitions, start, final):
```

The constructor receives three parameters.

### A. `transitions`

Contains the transition rules of the automaton.

Its structure is:

```python
{
    state: [(symbol, next_state), ...]
}
```

For example:

```python
{
    "q0": [("DIGIT", "q1")],
    "q1": [("DIGIT", "q1")]
}
```

This means:

- From `q0`, the automaton moves to `q1` when it reads a digit.
- From `q1`, it can read another digit and remain in `q1`.

### B. `start`

Defines the initial state.

For example:

```python
"q0"
```

### C. `final`

Contains the accepting states.

For example:

```python
{"q1"}
```

A string is accepted if the automaton reaches an accepting state after consuming the appropriate input.

### D. Collecting States

```python
self.states = (
    {start} | set(final) | set(transitions)
    | {t for arcs in transitions.values() for _, t in arcs}
)
```

This expression collects the states appearing in:

- The initial state.
- The accepting states.
- The transition dictionary.
- The destinations of transitions.

The result is stored in `self.states`.

## 7.3. The `matches()` Method

```python
def matches(self, label, char):
```

This method checks whether an input character matches a transition label.

It handles three situations.

**1. NOT_NEWLINE**

```python
if label == "NOT_NEWLINE":
    return char != "\n"
```

Accepts any character except a newline.

This condition is used by the comment automaton.

**2. Character Classes**

```python
if label in CHAR_CLASSES:
    return char in CHAR_CLASSES[label]
```

Checks whether the character belongs to a predefined character class.

For example, if the label is `DIGIT`, the method checks whether the character is between `0` and `9`.

**3. Direct Character Matching**

```python
return char == label
```

If the label is not a character class or special condition, the method compares the input character directly with the label.

This is used for symbols such as:

```text
=
.
/
;
```

## 7.4. The `epsilon_closure()` Method

```python
def epsilon_closure(self, states):
```

This method calculates the epsilon closure of a set of states.

The epsilon closure contains:

- The original states.
- All states reachable through epsilon transitions.
- States reachable through additional epsilon transitions.

The method begins with:

```python
closure = set(states)
stack = list(states)
```

- `closure` stores the discovered states.
- `stack` contains states that still need to be explored.

It then explores the transitions:

```python
while stack:
    state = stack.pop()
```

For each state, it checks its outgoing transitions:

```python
for symbol, nxt in self.transitions.get(state, []):
```

If the transition is an epsilon transition and the destination has not already been visited:

```python
if symbol is EPSILON and nxt not in closure:
    closure.add(nxt)
    stack.append(nxt)
```

The destination is added to both the closure and the stack.

Finally:

```python
return closure
```

The method returns all states reachable without consuming input characters.

This operation is essential for correctly simulating an NFA.

## 7.5. The `run()` Method

```python
def run(self, source, start):
```

This method simulates the NFA on the source code.

It receives:

- `source`: The complete input source code.
- `start`: The position where the automaton should begin scanning.

### Step 1: Initialize the Current States

```python
current = self.epsilon_closure({self.start})
```

The simulation starts from the initial state and calculates its epsilon closure.

### Step 2: Initialize the Last Accepted Position

```python
last_accepted = start if current & self.final else None
```

The program checks whether the current state set already contains an accepting state.

If it does, the initial position is stored as an accepted position.

Otherwise, `last_accepted` is initialized to `None`.

### Step 3: Read Input Characters

```python
for i in range(start, len(source)):
```

The automaton processes characters starting from the given position.

### Step 4: Calculate Possible Next States

```python
next_states = {
    target
    for state in current
    for symbol, target in self.transitions.get(state, [])
    if symbol is not EPSILON and self.matches(symbol, source[i])
}
```

This is the main NFA transition operation.

The program examines all current states and their outgoing transitions.

For every matching transition, its destination is added to `next_states`.

Since an NFA can have multiple possible transitions, the result is a set of states rather than a single state.

### Step 5: Stop When No Transition Is Possible

```python
if not next_states:
    break
```

If none of the current states can consume the input character, the simulation stops.

### Step 6: Calculate the New Epsilon Closure

```python
current = self.epsilon_closure(next_states)
```

After consuming a character, the program calculates all states reachable through epsilon transitions.

### Step 7: Record Accepting Positions

```python
if current & self.final:
    last_accepted = i + 1
```

If at least one accepting state is reached, the program records the position immediately after the consumed character.

It continues scanning so that a longer valid match can be found.

### Step 8: Return the Result

```python
if last_accepted is None:
    return None

return source[start:last_accepted], last_accepted
```

If no accepting state was reached, the function returns `None`.

Otherwise, it returns:

1. The recognized lexeme.
2. The ending position of that lexeme.

This mechanism allows the main lexical analyzer to compare the results of different automata.

---

# 8. Constructing the Individual Token Automata

Each token category has a separate function responsible for constructing its NFA.

## 8.1. `one_or_more()`

```python
def one_or_more(label):
    return NFA(
        {"q0": [(label, "q1")], "q1": [(label, "q1")]},
        "q0", {"q1"},
    )
```

This function creates a reusable NFA that recognizes one or more characters belonging to a given character class.

It contains two states:

- `q0`: Initial state.
- `q1`: Accepting state.

Transitions:

```text
q0 --label--> q1
q1 --label--> q1
```

The first character moves the automaton into the accepting state.

Additional matching characters keep it in the same state.

It is used for integer numbers and whitespace.

## 8.2. `create_keyword_nfa()`

This function creates an automaton that recognizes reserved words.

It starts by initializing:

```python
transitions = {"q0": []}
final = set()
```

- `q0` is the initial state.
- `final` stores the accepting states for all keywords.

The function then iterates over the sorted keyword set:

```python
for index, word in enumerate(sorted(KEYWORDS)):
```

For each keyword, it creates a separate sequence of states.

The initial state connects to the first state of each keyword through an epsilon transition:

```python
transitions["q0"].append((EPSILON, previous))
```

Then, every character of the keyword creates a transition to the next state.

For example, the keyword `if` has the following path:

```text
q0
 |
 ε
 v
k..._0 --i--> k..._1 --f--> k..._2
                                  |
                                FINAL
```

The last state of every keyword is added to the final-state set.

This creates one NFA capable of recognizing all words in `KEYWORDS`.

## 8.3. `create_identifier_nfa()`

This function recognizes identifiers.

Its transitions are:

```python
{
    "q0": [("LETTER", "q1"), ("_", "q1")],
    "q1": [("IDENTIFIER_CHAR", "q1")],
}
```

The automaton has two main states:

- `q0`: Initial state.
- `q1`: Accepting state.

The first character must be a letter or underscore.

After entering `q1`, the automaton can consume any number of letters, digits, or underscores.

Example:

```text
student
student1
_myVariable
```

All these sequences are accepted.

## 8.4. `create_integer_nfa()`

```python
def create_integer_nfa():
    return one_or_more("DIGIT")
```

This function constructs the integer automaton using the reusable `one_or_more()` function.

It accepts one or more digits.

Examples:

```text
0
1
25
100
```

The additional restriction concerning leading zeros is checked later by the error-handling function.

## 8.5. `create_real_nfa()`

This function recognizes real numbers.

Its transition structure is:

```python
{
    "q0": [("DIGIT", "q1")],
    "q1": [("DIGIT", "q1"), (".", "q2")],
    "q2": [("DIGIT", "q3")],
    "q3": [("DIGIT", "q3")],
}
```

The states have the following meanings:

| State | Meaning |
|---|---|
| q0 | Initial state. |
| q1 | Reading the integer part. |
| q2 | Decimal point has been read. |
| q3 | Reading the decimal part; accepting state. |

The automaton follows this sequence:

1. Read at least one digit.
2. Continue reading digits.
3. Read a decimal point.
4. Read at least one digit after the decimal point.
5. Continue reading additional decimal digits.

Example:

```text
12.5
3.14
100.75
```

A number without a decimal part is not accepted by this automaton.

## 8.6. `create_numalpha_nfa()`

This automaton recognizes sequences that begin with digits and continue with letters or underscores.

Transitions:

```python
{
    "q0": [("DIGIT", "q1")],
    "q1": [
        ("DIGIT", "q1"),
        ("LETTER", "q2"),
        ("_", "q2")
    ],
    "q2": [("IDENTIFIER_CHAR", "q2")],
}
```

States:

- `q0`: Initial state.
- `q1`: Reading digits.
- `q2`: Reading letters, digits, or underscores after the initial digits; accepting state.

Example:

```text
123abc
0bc
25_name
```

These sequences are recognized as `NUMALPHA` and later reported as lexical errors.

## 8.7. `create_operator_nfa()`

This function recognizes arithmetic and comparison operators.

Its transitions are:

```python
{
    "q0": [(EPSILON, "q1"), (EPSILON, "q2")],
    "q1": [("SINGLE_OPERATOR", "q4")],
    "q2": [("DOUBLE_OPERATOR", "q3")],
    "q3": [("=", "q4")],
}
```

The initial state has two epsilon transitions.

These create two alternative paths.

### First Path: Single-Character Operators

```text
q0 --ε--> q1 --SINGLE_OPERATOR--> q4
```

Recognizes:

```text
+ - * / < >
```

### Second Path: Double-Character Operators

```text
q0 --ε--> q2 --DOUBLE_OPERATOR--> q3 --=--> q4
```

Recognizes:

```text
<=
>=
==
!=
```

The accepting state is `q4`.

The automaton uses non-deterministic branching to consider both possible operator forms.

## 8.8. `create_assignment_nfa()`

```python
def create_assignment_nfa():
    return NFA({"q0": [("=", "q1")]}, "q0", {"q1"})
```

This automaton recognizes the assignment symbol.

It contains:

- `q0`: Initial state.
- `q1`: Accepting state.

Transition:

```text
q0 --=--> q1
```

Example:

```c
x = 10;
```

The assignment symbol is classified separately from comparison operators.

## 8.9. `create_separator_nfa()`

```python
def create_separator_nfa():
    return NFA(
        {"q0": [(c, "q1") for c in ";,(){}"]},
        "q0", {"q1"},
    )
```

Recognizes punctuation symbols.

Supported separators:

```text
;
,
(
)
{
}
```

Every supported character has a direct transition from `q0` to `q1`.

## 8.10. `create_comment_nfa()`

This function recognizes single-line comments.

Transitions:

```python
{
    "q0": [("/", "q1")],
    "q1": [("/", "q2")],
    "q2": [("NOT_NEWLINE", "q2")],
}
```

The automaton works as follows:

1. Read the first `/` and move from `q0` to `q1`.
2. Read the second `/` and move from `q1` to `q2`.
3. Continue consuming characters while they are not newlines.

State `q2` is the accepting state.

Example:

```c
// This is a comment
```

The comment automaton is designed to consume the comment until the next newline.

## 8.11. `create_whitespace_nfa()`

```python
def create_whitespace_nfa():
    return one_or_more("WHITESPACE")
```

Uses the reusable `one_or_more()` function to recognize one or more whitespace characters.

It supports:

- Spaces
- Tabs
- Newlines
- Carriage returns

Whitespace is recognized but excluded from the final token list.

---

# 9. Organizing the Automata

After constructing the individual automata, the program combines them into one list:

```python
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
```

Each element contains:

1. The token category.
2. Its corresponding NFA object.

The lexical analyzer uses this list to test the input against all available automata.

## 9.1. Ignored Token Categories

```python
IGNORED = {"COMMENT", "WHITESPACE"}
```

Defines the token categories that should not appear in the final token list.

The automata still recognize these elements, but the main lexical analyzer skips storing them.

---

# 10. Longest Match Rule

One of the most important mechanisms in the NFA implementation is the **Longest Match Rule**, also known as Maximal Munch.

The main lexical analyzer tests all automata at the current input position.

Some automata may recognize shorter sequences, while others may recognize longer ones.

The program selects the match that consumes the greatest number of characters.

For example:

```text
>=
```

The operator automaton recognizes the complete two-character sequence.

The selected match is the longest valid match starting at the current position.

This is implemented using:

```python
best_type, best_end = None, i

for token_type, automaton in AUTOMATA:
    result = automaton.run(source, i)

    if result and result[1] > best_end:
        best_type, best_end = token_type, result[1]
```

Variables:

| Variable | Meaning |
|---|---|
| `best_type` | Token category of the current best match. |
| `best_end` | Ending position of the longest match. |
| `result` | Result returned by an individual automaton. |

If two automata recognize sequences of exactly the same length, the first one encountered in `AUTOMATA` remains selected because the condition uses `>` rather than `>=`.

This also affects keyword recognition: when a complete keyword and an identifier have the same length, the keyword automaton appears first and wins the tie.

---

# 11. Error Handling in the NFA Implementation

## 11.1. The `error_message()` Function

```python
def error_message(token_type, lexeme):
```

This function checks whether a recognized sequence represents a specific lexical error.

It handles two cases.

### A. NUMALPHA

```python
if token_type == "NUMALPHA":
    return "IDENTIFIER cannot start with a number"
```

Reports an error when a sequence begins with digits and continues with identifier characters.

### B. INTEGER Starting With Zero

```python
if token_type == "INTEGER" and len(lexeme) > 1 and lexeme[0] == "0":
    return "INTEGER cannot start with 0"
```

Rejects multi-digit integers that start with zero.

Examples:

```text
011
025
0100
```

If neither condition is satisfied, the function returns `None`, indicating that no specific error was found.

## 11.2. Unrecognized Characters

The main lexical analyzer also handles characters that are not accepted by any automaton.

If no automaton produces a valid match:

```python
if best_type is None:
```

The program generates a lexical error containing:

- The invalid character.
- Its line number.
- Its column number.

Then it moves forward by one character to continue the analysis.

This ensures that one invalid character does not stop the entire lexical analysis process.

---

# 12. The Main Lexical Analysis Function (NFA)

```python
def lexical_analysis(source):
```

This function coordinates the complete scanning process.

## 12.1. Initialize the Variables

```python
tokens, errors = [], []
i, line, column = 0, 1, 1
```

The variables are:

| Variable | Purpose |
|---|---|
| `tokens` | Stores valid tokens. |
| `errors` | Stores lexical errors. |
| `i` | Current index in the source string. |
| `line` | Current line number. |
| `column` | Current column number. |

Unlike the first implementation, this program uses an explicit index `i` to control the scanning position.

## 12.2. Start the Scanning Loop

```python
while i < len(source):
```

The loop continues until the end of the source code is reached.

At every iteration, the analyzer attempts to recognize a token starting at position `i`.

## 12.3. Test All Available Automata

```python
best_type, best_end = None, i

for token_type, automaton in AUTOMATA:
    result = automaton.run(source, i)
```

Every automaton is executed using the same starting position.

Each automaton returns either:

- A recognized lexeme and its ending position.
- `None` if no valid match exists.

## 12.4. Select the Longest Match

```python
if result and result[1] > best_end:
    best_type, best_end = token_type, result[1]
```

The analyzer updates its selected token whenever a longer match is found.

This process determines which token category will be assigned to the current lexeme.

## 12.5. Handle Unrecognized Input

If no automaton recognizes the current character:

```python
if best_type is None:
    errors.append(
        f"Lexical error: {source[i]!r} at line {line}, column {column}"
    )
    i += 1
    column += 1
    continue
```

The program:

1. Creates an error message.
2. Increases the input index.
3. Increases the column number.
4. Continues scanning.

## 12.6. Extract the Recognized Lexeme

```python
lexeme = source[i:best_end]
```

Extracts the characters between the current position and the ending position.

## 12.7. Validate the Recognized Lexeme

```python
message = error_message(best_type, lexeme)
```

The program checks whether the selected token represents a lexical error.

If an error message exists, it is added to the `errors` list.

Otherwise, the token is stored unless its category belongs to `IGNORED`.

```python
elif best_type not in IGNORED:
    tokens.append((best_type, lexeme, line))
```

The token structure is:

```text
(Token Type, Lexeme, Line Number)
```

## 12.8. Update Line and Column Positions

```python
newlines = lexeme.count("\n")

if newlines:
    line += newlines
    column = len(lexeme) - lexeme.rfind("\n")
else:
    column += len(lexeme)
```

The program checks whether the recognized lexeme contains newline characters.

If it does, it updates the line number and calculates the column after the last newline.

Otherwise, it increases the column by the lexeme length.

## 12.9. Move to the Next Input Position

```python
i = best_end
```

After processing a lexeme, the analyzer moves the scanning index to the position immediately after that lexeme.

This prevents already processed characters from being analyzed again.

## 12.10. Calculate Statistics and Return Results

```python
statistics = Counter(token[0] for token in tokens)

return tokens, errors, statistics
```

As in the first implementation, the function returns:

1. Recognized tokens.
2. Lexical errors.
3. Token statistics.

---

# 13. Main Function and Input Data (NFA)

The second implementation uses a separate sample source program:

```python
source = """int ab = 0;
    integer 0bc = 11;
    khalil = 011;
    drif = gg"""
```

This example tests different lexical situations.

| Input | Purpose |
|---|---|
| `int` | Tests keyword recognition. |
| `ab` | Tests identifier recognition. |
| `=` | Tests assignment recognition. |
| `0` | Tests valid integer recognition. |
| `integer` | Tests identifier recognition. |
| `0bc` | Tests an identifier beginning with a number. |
| `11` | Tests integer recognition. |
| `khalil` | Tests identifier recognition. |
| `011` | Tests the leading-zero rule. |
| `drif` | Tests identifier recognition. |
| `gg` | Tests another identifier. |

The input is passed to the analyzer:

```python
tokens, errors, statistics = lexical_analysis(source)
```

The program then displays the results.

## 13.1. Main Function

```python
def main():
```

The `main()` function organizes the execution of the NFA implementation.

It:

1. Defines the input source code.
2. Calls `lexical_analysis()`.
3. Displays the recognized tokens.
4. Displays lexical errors.
5. Displays token statistics.

## 13.2. Program Entry Point

```python
if __name__ == "__main__":
    main()
```

This condition ensures that `main()` is called when the Python file is executed directly.

It also allows the file to be imported into another Python program without automatically executing the main function.

---

# 14. Input and Output Specifications

Both programs receive source code as a Python string.

They do not require a separate input file or graphical interface.

The test input is defined directly inside each Python file.

## 14.1. Supported Token Categories

The implementations recognize the following general categories:

| Category | Description | Example |
|---|---|---|
| KEYWORD | Reserved words. | `int`, `if` |
| IDENTIFIER | Variable names and identifiers. | `number`, `student1` |
| INTEGER | Whole numbers. | `25`, `0` |
| REAL | Decimal numbers. | `12.5` |
| NUMALPHA | Sequences beginning with digits followed by identifier characters; treated as errors. | `12abc` |
| OPERATOR | Arithmetic and comparison operators. | `+`, `>=` |
| ASSIGNMENT | Assignment symbol. | `=` |
| SEPARATOR | Punctuation symbols. | `;`, `(` |
| COMMENT | Single-line comments. | `// comment` |
| WHITESPACE | Spaces, tabs, and newlines. | Space character |

`INVALID` is explicitly defined in the Regex implementation as a fallback pattern. The NFA implementation handles unmatched characters directly in its main scanning function.

## 14.2. Output Structure

Both lexical analysis functions return three results:

```python
tokens, errors, statistics
```

### Tokens

Each token is represented as a tuple:

```python
(token_type, lexeme, line_number)
```

Example:

```python
("KEYWORD", "int", 1)
```

### Errors

A list of strings containing lexical error descriptions.

Example:

```text
Lexical error: '011' at line 3, column 14: INTEGER cannot start with 0
```

### Statistics

A `Counter` object containing the number of occurrences of every valid token category.

Example:

```text
KEYWORD: 2
IDENTIFIER: 3
INTEGER: 4
```

## 14.3. Ignored Elements

The following elements are recognized but excluded from the token list:

- Comments.
- Whitespace.

Consequently, they are also excluded from the total token count and token statistics.

---

# 15. Practical Execution and Results

## 15.1. Running the First Implementation

Open a terminal in the project directory and execute:

```bash
python lex_analyzer_re.py
```

The program processes its predefined input and displays the results.

### Actual Output

```text
TOKENS:
token=('KEYWORD', 'int', 1)
token=('IDENTIFIER', 'x', 1)
token=('ASSIGNMENT', '=', 1)
token=('SEPARATOR', ';', 1)
token=('KEYWORD', 'float', 2)
token=('IDENTIFIER', 'y', 2)
token=('ASSIGNMENT', '=', 2)
token=('REAL', '2.5', 2)
token=('SEPARATOR', ';', 2)
token=('ASSIGNMENT', '=', 3)
token=('INTEGER', '0', 3)
token=('SEPARATOR', ';', 3)

LEXICAL ERRORS:
Lexical error: '010' at line 1, column 9 you can't start an INTEGER with 0
Lexical error: '@' at line 2, column 8
Lexical error: '1farouk' at line 3, column 1

TOKEN STATISTICS:
Total tokens: 12
ASSIGNMENT: 3
IDENTIFIER: 2
INTEGER: 1
KEYWORD: 2
REAL: 1
SEPARATOR: 3
```

### Results Analysis

The analyzer successfully recognizes:

- Two keywords.
- Two identifiers.
- Three assignment operators.
- One integer.
- One real number.
- Three separators.

It also detects three lexical errors:

1. `010`: An integer starting with zero.
2. `@`: An invalid character.
3. `1farouk`: A sequence starting with a number followed by letters.

The comment is recognized but excluded from the output.

The total number of valid tokens is 12.

## 15.2. Running the Second Implementation

Execute:

```bash
python nfa_lex_analyzer.py
```

The program uses its own predefined input and processes it through the individual NFAs.

### Actual Output

```text
TOKENS:
('KEYWORD', 'int', 1)
('IDENTIFIER', 'ab', 1)
('ASSIGNMENT', '=', 1)
('INTEGER', '0', 1)
('SEPARATOR', ';', 1)
('IDENTIFIER', 'integer', 2)
('ASSIGNMENT', '=', 2)
('INTEGER', '11', 2)
('SEPARATOR', ';', 2)
('IDENTIFIER', 'khalil', 3)
('ASSIGNMENT', '=', 3)
('SEPARATOR', ';', 3)
('IDENTIFIER', 'drif', 4)
('ASSIGNMENT', '=', 4)
('IDENTIFIER', 'gg', 4)

LEXICAL ERRORS:
Lexical error: '0bc' at line 2, column 13: IDENTIFIER cannot start with a number
Lexical error: '011' at line 3, column 14: INTEGER cannot start with 0

TOKEN STATISTICS:
Total tokens: 15
ASSIGNMENT: 4
IDENTIFIER: 5
INTEGER: 2
KEYWORD: 1
SEPARATOR: 3
```

### Results Analysis

The NFA implementation successfully recognizes:

- One keyword.
- Five identifiers.
- Two integers.
- Four assignment operators.
- Three separators.

It detects two lexical errors:

1. `0bc`: An identifier cannot start with a number.
2. `011`: An integer cannot start with zero.

The word `khalil` is recognized as an identifier because it is not included in the `KEYWORDS` set.

The total number of valid tokens is 15.

---

# 16. Comparison Between the Two Implementations

Both implementations perform lexical analysis, but they use different recognition mechanisms.

| Feature | Regex Implementation | NFA Implementation |
|---|---|---|
| Source file | `lex_analyzer_re.py` | `nfa_lex_analyzer.py` |
| Recognition method | Regular Expressions | Non-Deterministic Finite Automata |
| Main mechanism | `re.finditer()` | `NFA.run()` |
| Token definitions | Regular expression patterns | State transition definitions |
| State management | Handled internally by regex processing | Explicitly implemented |
| Epsilon transitions | Not manually implemented | Supported |
| Keyword recognition | Identifier matching followed by set lookup | Dedicated keyword automaton |
| Longest match | Depends on regex matching and pattern order | Explicitly selects the longest accepted match |
| Error detection | Pattern-based | Automata-based and character-based |
| Position tracking | Line and column | Line and column |
| Statistics | `Counter` | `Counter` |

## 16.1. Advantages of the Regex Implementation

- Shorter and more compact code.
- Easy to define and modify token patterns.
- Uses Python's built-in regular expression engine.
- Suitable for understanding pattern-based lexical recognition.

## 16.2. Advantages of the NFA Implementation

- Demonstrates how finite automata work internally.
- Explicitly defines states and transitions.
- Provides a practical implementation of epsilon closure.
- Demonstrates non-deterministic state exploration.
- Makes the Longest Match Rule explicit.
- Provides a reusable NFA class for different token categories.

## 16.3. Main Conceptual Difference

The first implementation describes token structures through regular expressions.

The second implementation describes token structures through automata, where each automaton contains states, transitions, an initial state, and accepting states.

Regular Expressions and Finite Automata are theoretically equivalent in their ability to describe regular languages.

The main difference in this project is the implementation technique.

---

# 17. Limitations and Technical Observations

The following observations describe the actual behavior of the submitted source code.

## 17.1. Different Keyword Examples

The Regex implementation uses:

```python
KEYWORDS = {"if", "else", "while", "int", "float", "farouk"}
```

The NFA implementation uses the same keyword set.

However, their test inputs are different.

The NFA example contains:

```text
khalil
```

Since `khalil` is not a reserved word in the keyword set, it is correctly recognized as an identifier.

## 17.2. Comment Recognition

The Regex implementation recognizes a comment beginning with `//`, including a comment with no characters after the two slashes.

The NFA comment automaton requires at least one character after `//` before reaching its accepting state.

Therefore, a comment containing only:

```text
//
```

is not accepted by the current NFA implementation.

## 17.3. Position Information

Both implementations include the line number in valid token tuples.

However, the column number is only included in error messages.

The token structure does not store the column position.

## 17.4. Leading-Zero Restriction

Both implementations reject multi-digit integers beginning with zero.

However, this is a validation rule applied after recognizing the integer, rather than a restriction built directly into the integer recognition pattern or automaton.

## 17.5. Operator Recognition

The NFA operator automaton explicitly handles single-character and double-character operators.

The assignment operator is implemented using a separate automaton.

This separation allows `=` to be classified as `ASSIGNMENT`, while `==` is classified as `OPERATOR`.

## 17.6. Different Test Inputs

The two programs do not use identical source code examples.

Therefore, their output token counts and error counts cannot be used as a direct performance comparison.

A fair comparison of their results would require passing the same source code to both implementations.

---

# 18. Conclusion

This project demonstrates two practical approaches to implementing a lexical analyzer.

The first implementation uses Regular Expressions to identify lexical patterns. It combines token patterns into a single expression, scans the source code, classifies recognized lexemes, detects errors, and generates statistics.

The second implementation uses a manually constructed NFA framework. It defines individual automata for different token categories and provides methods for matching characters, calculating epsilon closures, simulating state transitions, and selecting the longest recognized sequence.

The project provides practical experience with important compilation concepts, including:

- Lexical structures and token categories.
- Regular Expressions.
- Finite Automata.
- NFA state transitions.
- Epsilon transitions.
- Accepting states.
- Longest Match Rule.
- Lexical error detection.
- Source position tracking.
- Token statistics.

**Overall, the project demonstrates how lexical analysis can be implemented using two theoretically related but practically different recognition techniques: Regular Expressions and Non-Deterministic Finite Automata.**