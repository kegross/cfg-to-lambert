"""
An attempt at creating a program that takes in a context free rewrite grammar and creates a Lambert graph from the
inputted context free grammar.
A Lambert graph is also known as a Strongly Directed Hypergraph, and can be described as a directed
hypergraph where the edges are ordered. This order comes from zero-indexed numbers listed within the
tails of a hyperedge.
Some liberties and shortcuts have been taken, but some may be undone, and some are necessary to allow this project to
run.

@author Kiera Gross
email: kiera.gross@stonybrook.edu
"""
import graphviz as gv
import tempfile


"""
LambertGraph Class
Creates an instance of a lambert graph with all the necessary information to create an image

nodes: the nodes in the graph 
--> stored as a list
edges: the hyperedges of the graph
--> stored as a dictionary
    --> keys are numbers: zero to k-1 where k is the number of edges
    --> values are lists of tails, use lists to preserve order (don't need something else to track order)
edge_des: the "destination" or head of the hyperedge in question
--> stored as a dictionary
    --> keys are numbers: zero to k-1 where k is the number of edges
    --> values are lists of strings, each string being the name of a node
"""

class LambertGraph:
    def __init__(self, nodes, edges, edge_des):
        self.nodes = nodes  # nodes are the nodes/vertices of the graph
        self.edges = edges  # edges are the hyperedges, a dict of lists key: edge number, values: list of tail edges
        self.edge_des = edge_des  # head of the edge & the root node in the DFTBA

    def __str__(self):  # tostring, mainly for debugging
        return "nodes: " + str(self.nodes) + '\n' + "edges: " + str(self.edges) + '\n' + "edge destination:" + \
               str(self.edge_des)


"""
Checks if a given CFG is actually context free and well-formatted
input: the input the user has given that is allegedly a CFG
returns string: empty string if CFG, comment about format or context free-ness if not
"""

def checkCFG(user_input):
    user_input = str(user_input)
    issues = []
    rules = user_input.split(";")  # split the input into a list of rules
    for rule in rules:
        split_rule = rule.split("->")  # need the first and second part of each rule
        if len(split_rule) != 2:  # there should only be a left and right side to the ->
            if 1 not in issues:
                issues += [1]
        if len(split_rule[0]) != 1:  # the left side should be one symbol
            if 2 not in issues:
                issues += [2]
        if split_rule[0].islower():  # the left side should be a nonterminal symbol
            if 3 not in issues:
                issues += [3]
        if not split_rule[0].isalpha():  # the left side should be alphabetical-only
            if 4 not in issues:
                issues += [4]
        if len(split_rule) > 1:
            if not split_rule[1].isalpha():  # the right side should also be alphabetical-only (given it exists)
                if 4 not in issues:
                    issues += [4]
    if issues == []:
        return ""
    else:
        errors = ""
        for issue in issues:
            if issue == 1:
                errors += "You have incorrectly used '->' in at least one rule. "
            if issue == 2:
                errors += "For a context free grammar, the left side of the rule must be one letter long. "
            if issue == 3:
                errors += "For a context free grammar, the left side of the rule must be a nonterminal symbol. "
            if issue == 4:
                errors += "You may only use alphabetical characters for this program. "
    return errors + "You may type 'help' for help, 'quit' for quit, or try again now: "


"""
Turns a verified context free grammar into a lambert graph
input: the verified CFG
output: an instance of a LambertGraph which matches the CFG
"""

def CFGtoLambert(cfg):
    cfg = str(cfg)
    rules = cfg.split(";")
    # need the characters chosen by the user, so create a set (no duplicates) of only the alphabetical characters
    chars = cfg.replace("->","")
    chars = chars.replace(";","")
    chars = "".join(set(chars))
    index = 0  # associate rules with a number so they can be tied to edges, and have the edges accessible by number
    rndict = {}
    for rule in rules:
        rndict[rule] = index
        index += 1
    # now set up the structures for the instance of LambertGraph
    nodes = []
    edges = {}
    edge_des = {}
    for char in chars:
        nodes += ["q_" + char]
        # if the character is a terminal, it needs an edge coming from no nodes with itself as the weight
        if char.islower():
            edges[index] = []  # continue using index so it doesn't mess up the dictionaries
            edge_des[index] = char
            index += 1
    for rule in rules:
        parts = rule.split("->")
        left = parts[0]
        right = parts[1]
        edges[rndict[rule]] = []
        edge_des[rndict[rule]] = left
        for char in right:
            edges[rndict[rule]] += ["q_" + char]
    return LambertGraph(nodes, edges, edge_des)


"""
Creates the visual for the Lambert graph using graphviz
input: the Lambert Graph instance
output: a graphviz graph that can be displayed as a pdf
"""

def createLambertVisual(lambertgraph):
    graph = gv.Digraph('LambertGraph')
    # graph the start node first
    graph.attr('node',shape='doublecircle')
    graph.node("q_" + lambertgraph.edge_des[0])
    # graph the edge nodes
    graph.attr('node', shape='circle')
    for key in lambertgraph.edges:
        if lambertgraph.edges[key] == []:  # arrow in from "nowhere"
            graph.attr('node', shape='plain')  # this is how it's made to look like it's not from a node
            graph.node(lambertgraph.edge_des[key])
            graph.attr('node', shape='circle')
            graph.edge(lambertgraph.edge_des[key],"q_" + lambertgraph.edge_des[key])
        elif len(lambertgraph.edges[key]) == 1:  # simple case, just a regular edge
            graph.edge(lambertgraph.edges[key][0], "q_" + lambertgraph.edge_des[key], label=lambertgraph.edge_des[key])
        else:  # hyperedge time, this is where "fake nodes" come in
            index = 0
            graph.attr('node', shape='plain')  # create nodes for each hyperedge
            graph.node("e" + str(key))         # make them plain so they don't distract from "real nodes"
            graph.attr('node', shape='circle')
            for tail in lambertgraph.edges[key]:  # send each tail to the fake node
                graph.edge(tail, "e" + str(key), label=str(index))  # the label is the order
                index += 1
            graph.edge("e" + str(key), "q_" + lambertgraph.edge_des[key], label=lambertgraph.edge_des[key])
    return graph  # ^^^ go from the fake edge to the real destination with the correct label


"""
The main function:
    - Gives examples for use if "help" is entered
    - Accepts the input for CFG
    - Uses the checkCFG function to make sure the input is context free (and formatted correctly)
    --> If it is not a CFG: concludes program with message to user
    --> If is a CFG, runs CFGtoLambert function to create Lambert struct
    - Displays Lambert Graph to user, then ends
"""

def main():
    help_or_cfg = input("Please enter your context free rewrite grammar or type 'help' for information about this "
                        "program: ")
    help_or_cfg = str(help_or_cfg)
    while checkCFG(help_or_cfg) != "":
        if help_or_cfg.lower() == "quit" or help_or_cfg.lower() == 'q':
            print("Goodbye!")
            exit(0)
        if help_or_cfg.lower() == "help" or help_or_cfg.lower() == 'h':
            help_or_cfg = input(
                "A context free rewrite grammar contains rules of the form A->B where A is a nonterminal "
                "symbol, and B is a string containing any number of nonterminal and terminal symbols. This "
                "program uses uppercase letters for nonterminal symbols and lowercase letters for the "
                "alphabet. Please enter the rules with '->' for the arrows, with semicolons inbetween each "
                "rule. For example: 'S->aSb;S->ab' is a^nb^n. It will be assumed that your first rule starts with "
                "your start symbol. You may also type 'quit' to quit: ")
        else:
            help_or_cfg = input(checkCFG(help_or_cfg))
    lambert_graph = CFGtoLambert(help_or_cfg)
    visual = createLambertVisual(lambert_graph)
    visual.render(tempfile.mktemp('.gv'), view=True)


main()
