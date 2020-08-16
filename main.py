import numpy as np
from collections import Counter, defaultdict
import math
import nltk
from nltk.tree import Tree
from symbol import Symbol, Nonterminal, Terminal
from rule import Rule
from grammar import PCFG
from cky import cky
from treebuilder import build_tree, make_nltk_tree

def main():
    # TODO: implement Penn Treebank support

    # Read in the grammar
    istream = open('data/groucho-grammar-1.txt')
    grammar = PCFG(read_grammar_rules(istream))
    print("The grammar:\n", grammar, "\n")

    # Turn the sentence into a list
    sentence = "I shot an elephant in my pajamas".split()

    num_words = len(sentence)
    num_nonterminals = len(grammar.nonterminals)

    # Make a nonterminal2index and a index2nonterminal dictionary
    n2i = defaultdict(lambda: len(n2i))
    i2n = dict()
    for A in grammar.nonterminals:
        i2n[n2i[A]] = A

    # Stop defaultdict behavior of n2i
    n2i = dict(n2i)

    # A numpy array zeros
    score = np.zeros((num_nonterminals,
                      num_words + 1,
                      num_words + 1))

    # A numpy array that can store arbitrary data (we set dtype to object)
    back = np.zeros((num_nonterminals,
                     num_words + 1,
                     num_words + 1), dtype=object)

    # Run CKY
    score, back = cky(sentence, grammar, n2i)

    derivation = build_tree(back, sentence, 0, len(sentence), Nonterminal('S'), n2i)

    tree = make_nltk_tree(derivation)
    tree.pretty_print()


def read_grammar_rules(istream):
    """Reads grammar rules formatted as 'LHS ||| RHS ||| PROB'."""
    for line in istream:
        line = line.strip()
        if not line:
            continue
        fields = line.split('|||')
        if len(fields) != 3:
            raise ValueError('I expected 3 fields: %s', fields)
        lhs = fields[0].strip()

        if lhs[0] == '[':
            lhs = Nonterminal(lhs[1:-1])
        else:
            lhs = Terminal(lhs)
        rhs = fields[1].strip().split()
        new_rhs = []
        for r in rhs:
            if r[0] == '[':
                r = Nonterminal(r[1:-1])
            else:
                r = Terminal(r)
            new_rhs.append(r)

        prob = float(fields[2].strip())
        yield Rule(lhs, new_rhs, prob)
