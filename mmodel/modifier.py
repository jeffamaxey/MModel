from functools import wraps
import inspect
from mmodel.utility import parse_input


def loop_modifier(func, parameter: str):
    """Loop - iterates one given parameter

    :param list parameter: target parameter to loop
    """

    @wraps(func)
    def loop_wrapped(**kwargs):

        loop_values = kwargs.pop(parameter)
        return [func(**kwargs, **{parameter: value}) for value in loop_values]

    return loop_wrapped


def zip_loop_modifier(func, parameters: list):
    """Pairwise loop - iterates the values from loop

    :param list parameters: list of the parameter to loop
        only one parameter is allowed. If string of parameters are
        provided, the parameters should be delimited by ", ".
    """

    @wraps(func)
    def loop_wrapped(**kwargs):

        loop_values = [kwargs.pop(param) for param in parameters]

        result = []
        for value in zip(*loop_values):  # unzip the values

            loop_value_dict = dict(zip(parameters, value))
            rv = func(**kwargs, **loop_value_dict)
            result.append(rv)

        return result

    return loop_wrapped


def signature_modifier(func, parameters):
    """Replace node object signature

    :param list parameters: signature parameters to replace the original
        signature. The parameters are assumed to be "POSITIONAL_OR_KEYWORD", and no
        default values are allowed. The signature will replace the original signature
        in order.

    .. Note::

        The modifier does not work with functions that have positional only
        input parameters. When the signature_parameter length is smaller than the
        list of original signatures, there are two cases:
        1. The additional parameters have a default value - they do not show up
        in the signature, but the default values are applied to function
        2. The additional parameters do not have a default value - error is thrown
        for missing input

        ``mmodel`` allows the first case scenario, no checking is performed.

    """
    sig = inspect.Signature([inspect.Parameter(var, 1) for var in parameters])

    old_parameters = list(inspect.signature(func).parameters.keys())

    if len(parameters) > len(old_parameters):
        raise Exception(
            "The number of signature modifier parameters "
            "exceeds that of function's parameters"
        )

    # once unzipped to return iterators, the original variable returns none
    param_pair = list(zip(old_parameters, parameters))

    @wraps(func)
    def wrapped(**kwargs):
        # replace keys
        replace_kwargs = {old: kwargs[new] for old, new in param_pair}
        return func(**replace_kwargs)

    wrapped.__signature__ = sig
    return wrapped


def signature_binding_modifier(func):
    """Add parameter binding and checking for function

    The additional wrapper is unnecessary, but to keep a consistent
    modifier syntax. The modifier can be used on wrapped functions
    that do not have a parameter binding step (ones that only allow
    keyword arguments).

    The parse_input method binds the input args and kwargs and fills
    default values automatically. The resulting function behaves the
    same as a python function.
    """

    sig = inspect.signature(func)

    @wraps(func)
    def wrapped(*args, **kwargs):

        parsed_kwargs = parse_input(sig, *args, **kwargs)

        return func(**parsed_kwargs)

    return wrapped
