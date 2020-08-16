from collections import defaultdict


class PCFG(object):
    """
    Constructs a PCFG.
    A PCFG stores a list of rules that can be accessed in various ways.

    :param rules: an optional list of rules to initialize the grammar with
    """

    def __init__(self, rules=[]):
        self._rules = []
        self._rules_by_lhs = defaultdict(list)
        self._terminals = set()
        self._nonterminals = set()
        for rule in rules:
            self.add(rule)

    def add(self, rule):
        """Adds a rule to the grammar"""
        if not rule in self._rules:
            self._rules.append(rule)
            self._rules_by_lhs[rule.lhs].append(rule)
            self._nonterminals.add(rule.lhs)
            for s in rule.rhs:
                if s.is_terminal():
                    self._terminals.add(s)
                else:
                    self._nonterminals.add(s)

    def update(self, rules):
        """Add a list of rules to the grammar"""
        for rule in rules:
            self.add(rule)

    @property
    def nonterminals(self):
        """The list of nonterminal symbols in the grammar"""
        return self._nonterminals

    @property
    def terminals(self):
        """The list of terminal symbols in the grammar"""
        return self._terminals

    @property
    def rules(self):
        """The list of rules in the grammar"""
        return self._rules

    @property
    def binary_rules(self):
        """The list of binary rules in the grammar"""
        return [rule for rule in self._rules if rule.is_binary()]

    @property
    def unary_rules(self):
        """The list of unary rules in the grammar"""
        return [rule for rule in self._rules if rule.is_unary()]

    def __len__(self):
        return len(self._rules)

    def __getitem__(self, lhs):
        return self._rules_by_lhs.get(lhs, frozenset())

    def get(self, lhs, default=frozenset()):
        """The list of rules whose LHS is the given symbol lhs"""
        return self._rules_by_lhs.get(lhs, frozenset())

    def __iter__(self):
        """Iterator over rules (in arbitrary order)"""
        return iter(self._rules)

    def iteritems(self):
        """Iterator over pairs of the kind (LHS, rules rewriting LHS)"""
        return self._rules_by_lhs.items()

    def __str__(self):
        """Prints the grammar line by line"""
        lines = []
        for lhs, rules in self.iteritems():
            for rule in rules:
                lines.append(str(rule))
        return '\n'.join(lines)
