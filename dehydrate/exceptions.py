# coding: utf-8


class DehydrationException(Exception):

    # if description is static string
    description = None

    # if description is depends on params, use kwargs names in
    # `description_tpl`, values will be provided automatically.
    description_tpl = None

    def __init__(self, description=None, **kwargs):
        """
        Only one positional argument allowed: `description`. Other will be set
        as attributes.
        """
        self.description = description or self.description

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        if self.description:
            return self.description
        else:
            return self.format_description()

    def format_description(self):
        tpl = self.description_tpl.replace('{', '{self.')
        return tpl.format(self=self)

    def __unicode__(self):
        return unicode(str(self))

    def __repr__(self):
        return str(self)


class HandlerNotFound(DehydrationException):

    description_tpl = 'No handler for spec type `{spec_type}`'


class UnknownSpecFormat(DehydrationException):

    description_tpl = 'Unknown or invalid spec format. {spec}'


class TargetResolvingError(DehydrationException):

    description_tpl = """Can't resolve target {target}. It didn't match any of
object attributes names [{object_attributes_string}] or object methods
[{object_methods_string}] and get_{target} method was not found among
dehydrator getters [{dehydrator_getters_string}]."""

    @property
    def object_attributes_string(self):
        return ', '.join(
            attr for attr in dir(self.obj)
            if not callable(getattr(self.obj, attr))
            and not attr.startswith('__')
        )

    @property
    def object_methods_string(self):
        return ', '.join(
            attr for attr in dir(self.obj)
            if callable(getattr(self.obj, attr))
            and not attr.startswith('__')
        )

    @property
    def dehydrator_getters_string(self):
        return ' ,'.join(
            attr for attr in dir(self.dehydrator)
            if attr.startswith('get_') and
            callable(getattr(self.dehydrator, attr))
        )
