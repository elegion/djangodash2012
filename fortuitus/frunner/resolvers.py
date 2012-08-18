from operator import attrgetter, itemgetter
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
        func = itemgetter if isinstance(ref, dict) else attrgetter
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

    Might be full class path, i.e. `my.awesome.module.MyOperator` or simply
    `MyOperator`.  In the latter case it is imported from `frunner.operators`
    module.

    """
    mdl, _, cls = value.rpartition('.')
    mdl = 'fortuitus.frunner.operators' if not mdl else mdl
    module = import_module(mdl)
    return getattr(module, cls)
