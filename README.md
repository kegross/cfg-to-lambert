# cfg-to-lambert

An attempt at creating a program that takes in a [context-free rewrite grammar](https://en.wikipedia.org/wiki/Context-free_grammar) and creates a Lambert graph from the inputted context-free grammar.

A Lambert graph is also known as a Strongly Directed Hypergraph, and can be described as a [directed hypergraph](https://www.sciencedirect.com/science/article/pii/S0304397516002097) where the edges are ordered. This order comes from zero-indexed numbers listed within the tails of a hyperedge.

Here is an example output based on the a<sup>n</sup>b<sup>n</sup> language generated by
S->aSb
S->ab

![Image of output from cfg-to-lambert](https://github.com/kegross/cfg-to-lambert/blob/main/aSbLambertGraph.pdf)

# Dependencies

This code uses [graphviz](https://graphviz.org/) to generate the lambert graph image. Other graph visualization software may be used, but a new createLambertVisual function would be needed, and the main function would need to be edited slightly.

# Simplifications

The use of context-free grammars specifically is an attempt at displaying a Lambert graph for cases where it is definitely possible. Attempting all possible rewrite grammars would necessitate significant changes to the code, and might not be similar in nature to this project. Some grammars also may be impossible, so some check would need to be preformed before the rules go through the code to ensure it is possible to create a DFBTA which would then result in a Lambert graph.

Another simplification was to limit the alphabet for CFGs to all lowercase letters of the english alphabet, and nonterminal symbols limited to the capitalized versions of these same letters. This code could be edited with relative ease to change this, but the focus is on attempting images of strongly directed hypergraphs.

It was also assumed that the start variable of the rewrite grammar was in the first rule written on the left side. This is standard convention anyway and requires less back-and-forth between user and program.

Of note is that one non-alphabatical character is allowed to represent the empty string. For this program, "\\" was chosen if the user wishes to create a rule involving the empty string.

The creation of the lambert graph visual had its own challenges, discussed in the following section.

# The Creation of the Lambert Graph Visual

Instead of trying to solve the problem of displaying a directed hypergraph (a difficult problem without the "strongly directed" nature), we create a "faked" version of a hypergraph using extra nodes in a directed graph for hyperedges. 

This gives most aspects of the visual appearance desired, and adds a maximum of k nodes where k is the number of edges. As the number of edges comes from the number of rules, complexity of the context-free grammar does weigh significantly in the ability to create a display, however, for most applications, this method of creating a "strongly directed hypergraph" should suffice.

This project uses graphviz to display the directed graph, but the code could be modified to use the graph displaying module of your choice.

This does display an image that is very close to a strongly directed hypergraph, and it is readable as a strongly directed hypergraph. While not the most beautiful image, it does capture all parts necessary to view and understand the Lambert Graph.

# Commands

"help" or "h" - Pulls up an explanation of how to enter input, and how to quit the program

"quit" or "q" - Quits the program

# How to Enter a CFG

The alphabet of the CFG must be a subset of the lowercase english characters, and the terminal symbols must be a subset of the uppercase english characters.
The CFG must be entered as a rewrite grammar, rules separated by semicolons. The arrows should be typed using n-dash - greater than (->). "\" (backslash) may be used as the empty string for rules of the form A->\ only, as empty strings elsewhere are pointless.

An example:

A rewrite grammar for a<sup>n</sup>b<sup>n</sup> could be written as follows: S->aSb;S->ab

The image for this is displayed ![here](https://github.com/kegross/cfg-to-lambert/blob/main/aSbLambertGraph.pdf)

A rewrite grammar for a<sup>i</sup>b<sup>k</sup> or b<sup>k</sup>a<sup>i</sup> could be written as follows: S->AB;S->BA;A->Aa;A->\\;B->Bb;B->\

![This is the output from cfg-to-lambert](https://github.com/kegross/cfg-to-lambert/blob/main/LambertGraphakbi.pdf)

The program will try to tell you what you may have missed if you mistype or don't follow the rules of a context-free grammar.
