import operator
from operator import attrgetter, itemgetter

from core.functional import compose
from django.utils.importlib import import_module


def resolve_lhs(value, responses):
    """
    Resolves assertion's lhs.

    Format is approximately this::

        lhs := step_number.property_path
        step_number := (""|number)
        number := ("0"..."9")*
        property_path := ((("a"..."z")|"_")(("a"..."z")|"-"|"_")*["."])*

    Anyway, if you can't read this crap above (which is probably incorrect),
    here are some examples::

        .status_code       # current step, status code
        0.text.tweet.text  # response from step 0, tweet text

    """
    step_number, _, property_path = value.partition('.')
    step = -1 if step_number == '' else int(step_number)
    response = responses[step]
    prop_parts = property_path.split('.')
    ref = response
    for part in prop_parts:
        if isinstance(ref, dict):
            func = itemgetter
        elif isinstance(ref, list):
            func = compose(itemgetter, int)
        else:
            func = attrgetter
        ref = func(part)(ref)
    return ref


def resolve_rhs(value, responses):
    """
    Resolves assertion's rhs.

    Format is approximately this::

        rhs := (lhs|value)
        value := <anything without any dot characters>

    See also: :func resolve_lhs:.
    """
    if not isinstance(value, basestring) or '.' not in value:
        return value
    else:
        return resolve_lhs(value, responses)


def resolve_operator(value):
    """
    Returns operator class from operator string.

    Might be full path, i.e. `my.awesome.module.myoperator` or simply
    `operator`.  In the latter case it is imported from standard `operator`
    module.

    Writing your own operators is dead simple: just create a function that
    takes two arguments and returns a boolean.

    """
    mdl, _, func = value.rpartition('.')
    module = operator if not mdl else import_module(mdl)
    return getattr(module, func)
