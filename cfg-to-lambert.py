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
import copy

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
        if len(split_rule) > 1:  # we can only check the "right side" if it exists
            if not split_rule[1].isalpha():  # the right side should also be alphabetical-only
                if split_rule[1] != "\\":    # or it could be lambda (\), the empty string
                    if 4 not in issues:
                        issues += [4]
    emptys = []
    starts = ""
    for rule in rules:
        split_rule = rule.split("->")
        starts += split_rule[0]
        if len(split_rule) > 1:
            if split_rule[1] == "\\":
                emptys += [split_rule[0]]
    for empty in emptys:
        if starts.count(empty) < 2:
            if 5 not in issues:
                issues += [5]
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
                errors += "You may only use alphabetical characters for this program. If you use the empty string, it " \
                          "must be used on its own on the right side of a rule. "
            if issue == 5:
                errors += "You must have a definition other than the empty string for each nonterminal symbol. "
    return errors + "You may type 'help' for help, 'quit' for quit, or try again now: "


"""
A helper function to generate all binary numbers of a given length
Input: the length, the binary string so far, and the current index
Output: the binary sequence (in list form)
"""
nums = []  # global variable unfortunately necessary in this case :/
def helperGenBins(n,num,index):
    global nums
    if index == n:
        nums += [num]
    else:  # Current spot is either zero or one
        temp = copy.copy(num)  # turns out python does weird stuff and you need to make a copy *insert eyeroll emoji*
        temp[index] = 0
        helperGenBins(n, temp, index + 1)
        temp1 = copy.copy(num)  # if this copy and the other weren't made, all lists were zeros or ones
        temp1[index] = 1
        helperGenBins(n, temp1, index + 1)


"""
A recursive helper function which deals with languages that have terminal -> empty string rules
Input: the rules (without terminal -> empty string rules), the nonterminals that lead to empty strings, the size of the
rule set previous to the last additions (if there were any
Output: rules with all combinations of "empty nonterms" removed in all combinations
"""
def helperDealWithEmptyString(rules, nonterms, prev_len):
    if len(rules) == prev_len or len(nonterms) == 0:  # if there are no empty nonterms left or if the rules haven't been
        return rules                                    # changed, end and return
    else:
        nonterm = nonterms[0]
        prev_len = len(rules)  # update the length of the rules before changing the rules (potentially)
        for rule in rules:
            right = rule.split("->")[1]
            num_nonterms = right.count(nonterm)  # count the number of instances of the empty nonterminal
            if num_nonterms > 0:
                subseq = right.replace(nonterm,"")
                if subseq == "":
                    if rule.split("->")[0] not in nonterms:  # if the right side is only empty nonterminals, the left
                        nonterms += rule.split("->")[0]      # side is also an empty nonterminal
                zeros = []
                for i in range(num_nonterms):  # create a filled list of the correct length
                    zeros += [0]
                helperGenBins(num_nonterms, zeros, 0)  # generate all binary numbers of length n where n is the count
                for combo in nums:                       # of nonterminals in the right side
                    pot_rule = ""
                    for char in right:
                        if char == nonterm:  # for each nonterminal, it could be empty string or itself, the binary
                            if combo[0] == 0:  # numbers give all possible combinations (0 = empty, 1 = itself)
                                pot_rule += ""
                                combo = combo[1:]  # get rid of the first digit in the binary number, that was used
                            else:
                                pot_rule += char
                                combo = combo[1:]
                        else:
                            pot_rule += char  # other characters stay the same, so just add them back on
                    if pot_rule != "" and pot_rule != rule.split("->")[0]:  # the rule cannot be empty or just A->A
                        formed_rule = rule.split("->")[0] + "->" + pot_rule  # form the rule
                        if formed_rule not in rules:  # if the rule doesn't already exist, add it
                            rules += [formed_rule]
        nonterms = nonterms[1:]  # remove the nonterminal that was dealt with
        return helperDealWithEmptyString(rules, nonterms, prev_len)


"""
Turns a verified context free grammar into a lambert graph
input: the verified CFG
output: an instance of a LambertGraph which matches the CFG
"""

def CFGtoLambert(cfg):
    cfg = str(cfg)
    rules_withlam = cfg.split(";")  # We must do a couple steps to deal with the nonterminal to empty string rules
    empty_nonterms = []
    rules = []
    for rule in rules_withlam:  # We first track the "empty rules" or rules leading to an empty string
        split_rule = rule.split("->")
        if split_rule[1] == "\\":  # if the rule goes to empty string, we track the nonterminal
            empty_nonterms += [split_rule[0]]
        else:
            rules += [rule]  # otherwise the rule is added to our set of rules
    # now we need to add all possibilities of rules with the "empty nonterms" removed in any combination
    rules = copy.deepcopy(helperDealWithEmptyString(rules, empty_nonterms, 0))  # again, needed a copy for some reason
    chars = cfg.replace("->","")  # next steps are getting the set of characters chosen by the user
    chars = chars.replace(";","")
    chars = chars.replace("\\", "")
    chars = "".join(set(chars))  # this is simply a string of all alphabetical characters used in the rules
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
                "rule. For example: 'S->aSb;S->ab' is a^nb^n. It will be assumed that your first rule starts with your "
                "start symbol. Please use \'\ \' to represent the empty string. You may also type 'quit' to quit: ")
        else:
            help_or_cfg = input(checkCFG(help_or_cfg))
    lambert_graph = CFGtoLambert(help_or_cfg)
    visual = createLambertVisual(lambert_graph)
    visual.render(tempfile.mktemp('.gv'), view=True)


main()