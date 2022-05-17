# cfg-to-lambert

An attempt at creating a program that takes in a context free rewrite grammar and creates a Lambert graph from the inputted context free grammar.

A Lambert graph is also known as a Strongly Directed Hypergraph, and can be described as a directed hypergraph where the edges are ordered. This order comes from zero-indexed numbers listed within the tails of a hyperedge.

The use of context free grammars is an attempt at making displaying a Lambert graph possible in all cases.

Another simplification was to limit the alphabet for CFGs to all lowercase letters of the english alphabet, and nonterminal symbols limited to the capitalized versions of these same letters. This code could be edited with relative ease to change this, but the focus is on attempting images of strongly directed hypergraphs.

# Commands

"help" or "h" - Pulls up an explanation of how to enter input, and how to quit the program

"quit" or "q" - Quits the program

# How to Enter a CFG

The alphabet of the CFG must be a subset of the lowercase english characters, and the terminal symbols must be a subset of the uppercase english characters.
The CFG must be entered as a rewrite grammar, rules separated by semicolons. The arrows should be typed using n-dash - greater than (->).

An example:

A rewrite grammar for a^nb^n could be written as follows: S->aSb;S->ab

The program will try to tell you what you may have missed if you mistype or don't follow the rules of a context free grammar.
