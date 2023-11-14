# CS50 - Introduction to AI - Project: Crossword

## Task: Write an AI to generate crossword puzzles

### $ python generate.py data/structure1.txt data/words1.txt output.png

-> constraint satisfaction problem

- each sequence of squares as a variable, for which its value needs to be decided => which words of possible words to fill in here

- each variable defined by four values:

  - row it begins on (i)
  - column it begins on (j)
  - direction of word (h/v or down/across)
  - word length

- unary and binary constraints

  - unary -> given by length, if a value doesn't satisfy a variable's unary constraint, it can be removed from the variable's domain immediately (e.g. three-character words in this example)

  - binary -> given by overlap with neighbours, for each pair of neighbouring values, there is a shared overlap (square that's common for both)
    - representation of that overlap as the character index in each variable's word that must be the same character
  - e.g. overlap between Variable 1 and Variable 2 might be represented as the pair (1, 0), meaning that Variable 1’s character at index 1 necessarily must be the same as Variable 2’s character at index 0

- additional constraint - all words should be different

-> CHALLENGE: Program should find a different word (from given vocabulary list) for each variable that meets all of the unary and binary constraints.
