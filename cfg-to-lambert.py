"""
An attempt at creating a program that takes in a context free rewrite grammar and
creates a Lambert graph from the inputted context free grammar.
A Lambert graph is also known as a Strongly Directed Hypergraph, and can be described as a directed
hypergraph where the edges are ordered. This order comes from zero-indexed numbers listed within the
tails of a hyperedge.

@author Kiera Gross
email: kiera.gross@stonybrook.edu
"""

# This is the struct to be used for creating a lambert graph so all the necessary information to display it is stored
class LambertGraph:
    def __init__(self, nodes, edges, edge_weight, rules):
        self.nodes = nodes  # nodes are the nodes/vertices of the graph
        self.edges = edges  # edges are the hyperedges, a dict of lists key: edge number, values: list of tail edges
        self.edge_weight = edge_weight  # head of the edge & the root node in the DFTBA
        self.rules = rules  # the original rewrite grammar rules, here for preservation

    def __str__(self):  # tostring, mainly for debugging
        return "nodes: " + str(self.nodes) + '\n' + "edges: " + str(self.edges) + '\n' + "edge weight: " + \
               str(self.edge_weight)


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
        split_rule = rule.split("->")  # we need the first and second part of each rule
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
    rules.sort()
    # we need the characters chosen by the user, so we create a set (no duplicates) of only the alphabetical characters
    chars = cfg.replace("->","")
    chars = chars.replace(";","")
    chars = "".join(set(chars))
    index = 0  # we associate rules with a number so we can tie them to edges, and have the edges accessible by number
    rndict = {}
    nrdict = {}
    for rule in rules:
        rndict[rule] = index
        nrdict[index] = rule
        index += 1
    # now we set up the structures for our instance of LambertGraph
    nodes = []
    edges = {}
    edge_weight = {}
    for char in chars:
        nodes += ["q_" + char]
        # if the character is a terminal, it needs an edge coming from no nodes with itself as the weight
        if char.islower():
            edges[index] = []  # we continue using index so we don't mess up our dictionaries
            edge_weight[index] = [char]
            index += 1
    for rule in rules:
        parts = rule.split("->")
        left = parts[0]
        right = parts[1]
        edges[rndict[rule]] = []
        edge_weight[rndict[rule]] = left
        for char in right:
            edges[rndict[rule]] += ["q_" + char]
    return LambertGraph(nodes, edges, edge_weight, nrdict)



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
                "rule. For example: 'S->aSb;S->ab' is a^nb^n. You may also type 'quit' to quit: ")
        else:
            help_or_cfg = input(checkCFG(help_or_cfg))
    lambert_graph = CFGtoLambert(help_or_cfg)
    print(str(lambert_graph))
    # TODO: Convert lambert class to image


main()
