"""
betrack

Usage:
  betrack hello
  betrack -h | --help
  betrack --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  betrack hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/gvalentini85/betrack-cli/issues
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import betrack.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(betrack.commands, k) and v:
            module = getattr(betrack.commands, k)
            betrack.commands = getmembers(module, isclass)
            command = [command[1] for command in betrack.commands if command[0] != 'BetrackCommand'][0]
            command = command(options)
            command.run()
