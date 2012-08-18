class BaseOperator(object):
    """
    BaseClass for assertion operators.

    Subclass it and implement :meth run: when creating new operators.

    See :class Eq: for example.
    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def run(self):
        raise NotImplementedError


class Eq(BaseOperator):
    """
    Equality operator. Tests that lhs == rhs.
    """
    def run(self):
        return self.lhs == self.rhs
