### Grammar Parser and Augmentation
_This Python project is designed to manipulate and process formal grammars, particularly in the context of computational linguistics. The key functionalities of this code include grammar augmentation, closure calculation, state generation, and the computation of the FIRST and FOLLOW sets for grammar symbols._

### Features:
#### Grammar Augmentation:

_The function **grammarAugmentation** adds a new start symbol (S') and augments the grammar accordingly. This is often useful for certain parsing algorithms like LR parsers._

#### Closure Calculation:

_The function **findClosure** computes the closure of a set of items given an input state. This is critical in algorithms like the LR parsing algorithm to explore all possible derivations from a given point._

#### State Generation:

_The **generateStates** function helps in generating all the possible states in an LR parser by performing GOTO operations, which shifts the parsing process from one state to another based on grammar rules._

#### FIRST and FOLLOW Set Calculation:

- The first function computes the FIRST set of a given grammar rule.
- The follow function computes the FOLLOW set for non-terminal symbols, which helps in determining what symbols can follow a non-terminal in a derivation.

#### Functions:
- **grammarAugmentation(rules, nonterm_userdef, start_symbol)**: Augments the grammar by adding a new start symbol.

- **findClosure(input_state, dotSymbol, separatedRulesList, init_start_symbol)**: Computes the closure of a set of items.

- **compute_GOTO(state, statesDict, stateMap, separatedRulesList)**: Generates all the states based on the GOTO operation for LR parsing.

- **GOTO(state, charNextToDot, statesDict, stateMap, separatedRulesList)**: Calculates the transition to the next state based on the current dot position in the rule.

- **first(rule, diction, term_userdef)**: Computes the FIRST set for a given rule.

- **follow(nt, diction, start_symbol, term_userdef)**: Computes the FOLLOW set for a non-terminal symbol.

#### Usage:
- Grammar Input: Provide a set of grammar rules to the functions as input.

- Generate Parsing Tables: Use the functions to generate the necessary parsing tables and sets for use in an LR parser.

- Closure and GOTO: Use the closure and GOTO functions to perform state transitions and augment the parsing process.

This code is intended to assist in the development of parsers, particularly for formal grammar analysis and implementation of parsing algorithms.
