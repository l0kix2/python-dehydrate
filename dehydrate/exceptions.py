# coding: utf-8


class DehydrationException(Exception):

    description = None

    def __init__(self, description=None, **kwargs):
        self.description = description or self.description

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.description
