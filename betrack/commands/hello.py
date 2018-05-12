"""The hello command."""


from json import dumps

from .command import BetrackCommand


class Hello(BetrackCommand):
    """Say hello, world!"""

    def run(self):
        print('Hello, world!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
