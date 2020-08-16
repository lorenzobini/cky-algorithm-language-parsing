class Symbol:
    """
    A symbol in a grammar.
    This class will be used as parent class for Terminal, Nonterminal.
    This way both will be a type of Symbol.
    """

    def __init__(self):
        pass


class Terminal(Symbol):
    """
    Terminal symbols are words in a vocabulary

    E.g. 'I', 'ate', 'salad', 'the'
    """

    def __init__(self, symbol: str):
        assert type(symbol) is str, 'A Terminal takes a python string, got %s' % type(symbol)
        self._symbol = symbol

    def is_terminal(self):
        return True

    def is_nonterminal(self):
        return False

    def __str__(self):
        return "'%s'" % self._symbol

    def __repr__(self):
        return 'Terminal(%r)' % self._symbol

    def __hash__(self):
        return hash(self._symbol)

    def __len__(self):
        """The length of the underlying python string"""
        return len(self._symbol)

    def __eq__(self, other):
        return type(self) == type(other) and self._symbol == other._symbol

    def __ne__(self, other):
        return not (self == other)

    @property
    def obj(self):
        """Returns the underlying python string"""
        return self._symbol


class Nonterminal(Symbol):
    """
    Nonterminal symbols are the grammatical classes in a grammar.

    E.g. S, NP, VP, N, Det, etc.
    """

    def __init__(self, symbol: str):
        assert type(symbol) is str, 'A Nonterminal takes a python string, got %s' % type(symbol)
        self._symbol = symbol

    def is_terminal(self):
        return False

    def is_nonterminal(self):
        return True

    def __str__(self):
        return "[%s]" % self._symbol

    def __repr__(self):
        return 'Nonterminal(%r)' % self._symbol

    def __hash__(self):
        return hash(self._symbol)

    def __len__(self):
        """The length of the underlying python string"""
        return len(self._symbol)

    def __eq__(self, other):
        return type(self) == type(other) and self._symbol == other._symbol

    def __ne__(self, other):
        return not (self == other)

    @property
    def obj(self):
        """Returns the underlying python string"""
        return self._symbol
