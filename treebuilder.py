import nltk
from collections import Counter, defaultdict
from nltk.tree import Tree
from rule import Rule
from symbol import Symbol


class Span(Symbol):
    """
    A Span indicates that symbol was recognized between begin and end.

    Example:
        Span(Terminal('the'), 0, 1)
            This means: we found 'the' in the sentence between 0 and 1
        Span(Nonterminal('NP'), 4, 8) represents NP:4-8
            This means: we found an NP that covers the part of the sentence between 4 and 8

    Thus, Span holds a Terminal or a Nonterminal and wraps it between two integers.
    This makes it possible to distinguish between two instances of the same rule in the derrivation.
    Example:
        We can find that the rule NP -> Det N is use twice in the parse derrivation. But that in the first
        case it spans "an elephant" and in the second case it spans "my pajamas". We want to distinguis these.
        So: "an elephant" is covered by [NP]:2-4 -> [Det]:2-3 [N]:3-4
            "my pajamas" is covered by [NP]:5-7 -> [Det]:5-6 [N]:6-7

    Internally, we represent spans with tuples of the kind (symbol, start, end).
    """

    def __init__(self, symbol, start, end):
        assert isinstance(symbol, Symbol), 'A span takes an instance of Symbol, got %s' % type(symbol)
        self._symbol = symbol
        self._start = start
        self._end = end

    def is_terminal(self):
        # a span delegates this to an underlying symbol
        return self._symbol.is_terminal()

    def root(self):
        # Spans are hierarchical symbols, thus we delegate
        return self._symbol.root()

    def obj(self):
        """The underlying python tuple (Symbol, start, end)"""
        return (self._symbol, self._start, self._end)

    def translate(self, target):
        return Span(self._symbol.translate(target), self._start, self._end)

    def __str__(self):
        """Prints Symbol with span if Symbol is Nonterminal else without (purely aesthetic distinction)"""
        if self.is_terminal():
            return "%s" % (self._symbol)
        else:
            return "%s:%s-%s" % (self._symbol, self._start, self._end)

    def __repr__(self):
        return 'Span(%r, %r, %r)' % (self._symbol, self._start, self._end)

    def __hash__(self):
        return hash((self._symbol, self._start, self._end))

    def __eq__(self, other):
        return type(self) == type(
            other) and self._symbol == other._symbol and self._start == other._start and self._end == other._end

    def __ne__(self, other):
        return not (self == other)


def build_tree(back, sentence, start, end, root, n2i):
    """
    It returns a list called derivation which hols the rules that.

    :param back: a backpointer chart of shape [num_nonterminals, num_words+1, num_words+1]
    :param sentence: a list of words
    :param root: the root symbol of the tree: Nonterminal('S')
    :param n2i: the dictionary mapping from Nonterminals to indices
    :return derivation: a derivation: a list of Rules with Span symbols that generate the Viterbi tree.
    """
    derivation = []
    num_words = len(sentence)

    # base case
    if (num_words == 1):
        word = sentence[0]
        derivation.append(Rule(Span(root, start, end), [Span(Terminal(word), start, end)], prob=None))

    else:  # recursion
        span, lhs_symbol, rhs_symbol = back[n2i[root], start, end]

        derivation.append(
            Rule(Span(root, start, end), [Span(lhs_symbol, start, span), Span(rhs_symbol, span, end)], prob=None))

        # recursion on left hand side symbol
        derivation.extend(build_tree(back, sentence[0:span - start], start, span, lhs_symbol, n2i))
        # recustion on right hand side symbol
        derivation.extend(build_tree(back, sentence[span - start:num_words], span, end, rhs_symbol, n2i))

    return derivation

def make_nltk_tree(derivation):
    """
    Return a NLTK Tree object based on the derivation
    (list or tuple of Rules)
    """
    d = defaultdict(None, ((r.lhs, r.rhs) for r in derivation))

    def make_tree(lhs):
        return Tree(str(lhs), (str(child) if child not in d else make_tree(child) for child in d[lhs]))

    return make_tree(derivation[0].lhs)

