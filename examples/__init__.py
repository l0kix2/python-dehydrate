# coding: utf-8

from dehydrate import Dehydrator


class PersonDehydrator(Dehydrator):
    def get_password(self, obj):
        return '*' * len(obj.password)

    def get_superhero_status(self, obj):
        return obj.login == 'iron_man'
