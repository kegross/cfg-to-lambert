# cfg-to-lambert

An attempt at creating a program that takes in a context free rewrite grammar and 
creates a Lambert graph from the inputted context free grammar.

A Lambert graph is also known as a Strongly Directed Hypergraph, and can be described as a directed 
hypergraph where the edges are ordered. This order comes from zero-indexed numbers listed within the 
tails of a hyperedge.

The use of context free grammars is an attempt at making displaying a Lambert graph possible in all cases.

Some other simplifications were to make the alphabet for CFGs all lowercase letters of the english alphabet, and 
nonterminal symbols limited to the capitalized versions of these same letters.