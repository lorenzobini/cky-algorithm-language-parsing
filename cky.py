import numpy as np
from symbol import Terminal

def cky(sentence, grammar, n2i):
    """
    The CKY algorithm.

    Follow the pseudocode from the slides (or J&M).

    :param sentence: a list of words
    :param grammar: an instance of the class PCFG
    :param n2i: a dictionary mapping from Nonterminals to indices
    :return score: the filled in scores chart
    :return back: the filled in backpointers chart
    """
    num_words = len(sentence)
    num_nonterminals = len(grammar.nonterminals)

    # A numpy array to store the scores of intermediate parses
    score = np.zeros((num_nonterminals,
                      num_words + 1,
                      num_words + 1))

    # A numpy array to store the backpointers
    back = np.zeros((num_nonterminals,
                     num_words + 1,
                     num_words + 1), dtype=object)

    for j in range(0, num_words):
        word = sentence[j]
        for nt in grammar.nonterminals:
            rules = grammar.get(nt)
            for rule in rules:
                if rule.rhs[0] == Terminal(word):
                    score[n2i[nt], j, j + 1] = rule.prob

    for r in range(2, num_words + 1):
        for i in range(0, num_words - r + 1):
            for nt in grammar.nonterminals:
                j = i + r
                rules = grammar.get(nt)
                for k in range(i + 1, j):
                    for p in grammar.nonterminals:
                        for q in grammar.nonterminals:
                            for rule in rules:
                                if ([p][0] == rule.rhs[0]) and ([q][0] == rule.rhs[1]):
                                    if (rule.prob * score[n2i[p], i, k] * score[n2i[q], k, j] != 0 and
                                            rule.prob * score[n2i[p], i, k] * score[n2i[q], k, j] > score[
                                                n2i[nt], i, j]):
                                        back[n2i[nt], i, j] = (k, p, q)
                                        score[n2i[nt], i, j] = rule.prob * score[n2i[p], i, k] * score[n2i[q], k, j]

    return score, back
