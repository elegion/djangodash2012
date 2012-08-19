import random as sysrandom
import re
import string

from django.utils.importlib import import_module


PLACEHOLDER_REGEXP \
    = re.compile('\{(?P<resolver>[\w\d]+)(?P<params>(:[\w\d]+)*)\}', re.I)

RESOLVERS = {
    'random': 'fortuitus.feditor.resolvers.random',
}
RANDOM_SYMBOLS = {
    'd': string.digits,
    'l': string.ascii_lowercase,
    'L': string.ascii_uppercase,
}


def resolve_param(expr, context):
    """
    Resolves parameter expressions.

    Currently only random special form is supported.

    Example::

        {random:3:d}@touchin.ru ==> 345@touchin.ru
    """
    result = expr
    for ph in PLACEHOLDER_REGEXP.finditer(expr):
        placeholder = ph.group(0)
        resolver = RESOLVERS.get(ph.group('resolver'), None)
        params = ph.group('params').split(':')[1:]
        if not resolver:
            assert Exception('Wrong resolver')
        else:
            module = import_module('.'.join(resolver.split('.')[:-1]))
            fn = resolver.split('.')[-1]
            func = getattr(module, fn)
            result = result.replace(placeholder,
                                    func(placeholder, params, context))
    return result


def random(expr, params, context):
    """ Generates random expression. """
    length = 5
    symbols = 'dL'
    if len(params) > 0:
        length = int(params[0])
    if len(params) > 1:
        symbols = params[1]
    real_symbols = ''.join(RANDOM_SYMBOLS.get(s, s) for s in symbols)
    return ''.join(sysrandom.choice(real_symbols) for x in xrange(length))
