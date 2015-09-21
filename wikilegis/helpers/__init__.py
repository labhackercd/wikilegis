from django.utils.decorators import available_attrs
from django.utils.six import wraps


def nocontext(helper):
    """Marks helpers as *context independent* so it won't receive the *context* argument.

    TODO: it would be cool if @nocontext helpers could be treated as regular Python functions,
    (called without the context) wouldn't, it?

    NOTE: At this point it doesn't really matter if you receive the context or not. But it will in the future,
    so avoid using it unless actually required.
    """
    @wraps(helper, assigned=available_attrs(helper))
    def _wrapped_helper(context, *args, **kwargs):
        del context
        return helper(*args, **kwargs)

    return _wrapped_helper
