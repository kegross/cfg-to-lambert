# cfg-to-lambert

An attempt at creating a program that takes in a context free rewrite grammar [link?] and creates a Lambert graph from the inputted context free grammar.

A Lambert graph is also known as a Strongly Directed Hypergraph, and can be described as a directed hypergraph where the edges are ordered. This order comes from zero-indexed numbers listed within the tails of a hyperedge.

[add image here?]

# Simplifications

The use of context free grammars specifically is an attempt at making displaying a Lambert graph possible in all cases. Attempting all possible rewrite grammars would necessitate significant changes to the code, and might not be similar in nature to this project. Some grammars also may be impossible, so some check would need to be preformed before the rules go through the code to ensure it is possible to create a DFBTA which would then result in a Lambert graph.

Another simplification was to limit the alphabet for CFGs to all lowercase letters of the english alphabet, and nonterminal symbols limited to the capitalized versions of these same letters. This code could be edited with relative ease to change this, but the focus is on attempting images of strongly directed hypergraphs.

The creation of the lambert graph visual had its own challenges, discussed in the following section

# The Creation of the Lambert Graph Visual

Instead of trying to solve the problem of displaying a directed hypergraph (a difficult problem without the "strongly directed" nature), we create a "faked" version of a hypergraph using extra nodes in a directed graph for hyperedges. 

This gives most aspects of the visual appearance desired, and adds a maximum of k nodes where k is the number of edges. As the number of edges comes from the number of rules, complexity of the context free grammar does weigh significantly in the ability to create a display, however, for most applications, this method of creating a "strongly directed hypergraph" should suffice.

This project uses graphvis to display the directed graph, but the code could be modified to use the graph displaying module of your choice.

# Commands

"help" or "h" - Pulls up an explanation of how to enter input, and how to quit the program

"quit" or "q" - Quits the program

# How to Enter a CFG

The alphabet of the CFG must be a subset of the lowercase english characters, and the terminal symbols must be a subset of the uppercase english characters.
The CFG must be entered as a rewrite grammar, rules separated by semicolons. The arrows should be typed using n-dash - greater than (->).

An example:

A rewrite grammar for a^nb^n could be written as follows: S->aSb;S->ab

The program will try to tell you what you may have missed if you mistype or don't follow the rules of a context free grammar.
