# coding: utf-8

from dehydrate import Dehydrator


class Person(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def full_name(self):
        return ' '.join([
            self.first_name,
            self.last_name,
        ])


class PersonDehydrator(Dehydrator):
    def get_password(self, obj):
        return '*' * len(obj.password)

    def get_superhero_status(self, obj):
        return obj.login == 'iron_man'
