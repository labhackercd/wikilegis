from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _


class Orderer(object):
    title = None

    def __init__(self, request, params):
        # This dictionary will eventually contain the request's query string
        # parameters actually used by this filter.
        self.used_parameters = {}
        if self.title is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify "
                "a 'title'." % self.__class__.__name__)

    def has_output(self):
        """
        Returns True if some choices would be output for this filter.
        """
        raise NotImplementedError('subclasses of ListFilter must provide a has_output() method')

    def choices(self):
        """
        Returns choices ready to be output in the template.
        """
        raise NotImplementedError('subclasses of ListFilter must provide a choices() method')

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset.
        """
        raise NotImplementedError('subclasses of ListFilter must provide a queryset() method')

    def expected_parameters(self):
        """
        Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        raise NotImplementedError('subclasses of ListFilter must provide an expected_parameters() method')


class SimpleOrderer(Orderer):
    # The parameter that should be used in the query string for that filter.
    parameter_name = None

    # If default is `None`, the "All" option will appear. Otherwise it'll not.
    default = None

    def __init__(self, request, params, default=None):
        super(SimpleOrderer, self).__init__(request, params)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify "
                "a 'parameter_name'." % self.__class__.__name__)
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value
        lookup_choices = self.lookups(request)
        if lookup_choices is None:
            lookup_choices = ()
        self.lookup_choices = list(lookup_choices)

        if default is None:
            default = self.default
        self.default = default

        # For now.
        self.params = params.copy()

    def has_output(self):
        return len(self.lookup_choices) > 0

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name, self.default)

    def lookups(self, request):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError(
            'The SimpleListFilter.lookups() method must be overridden to '
            'return a list of tuples (value, verbose value)')

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self):
        if self.default is None:
            yield {
                'selected': self.value() is None,
                'query_string': self.get_query_string({}, [self.parameter_name]),
                'display': _('None'),
            }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': self.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def get_query_string(self, new_params=None, remove=None):
        if new_params is None:
            new_params = {}
        if remove is None:
            remove = []
        p = self.params.copy()
        for r in remove:
            for k in list(p):
                if k.startswith(r):
                    del p[k]
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                p[k] = v
        return '?%s' % urlencode(sorted(p.items()))
