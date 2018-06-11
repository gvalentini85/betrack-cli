#------------------------------------------------------------------------------#
# Copyright 2018 Gabriele Valentini. All rights reserved. Use of this source   #
# code is governed by a MIT license that can be found in the LICENSE file.     #
#------------------------------------------------------------------------------#

"""
betrack

Usage:
  betrack -h | --help
  betrack --version
  betrack track-particles -c <file> | --configuration=<file>
  betrack annotate-video

Options:
  -h --help                            Show help screen.
  --version                            Show betrack version.
  -c <file> --configuration=<file>     Specify a yml configuration file.

Examples:
  betrack track-particles

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/gvalentini85/betrack-cli/issues
"""


from sys     import exit
from inspect import getmembers, isclass
from docopt  import docopt

from . import __cli__ as CLI
from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import betrack.commands
    options = docopt(__doc__, version=CLI + ' ' + VERSION)
    bcommands = ['TrackParticles', 'AnnotateVideo']

    for (k, v) in options.items():
        if hasattr(betrack.commands, k.replace('-', '')) and v:
            module = getattr(betrack.commands, k.replace('-', ''))
            betrack.commands = getmembers(module, isclass)
            command = [command[1] for command in betrack.commands if command[0] in bcommands][0]
            command = command(options)
            errcode = command.run()
            exit(errcode)
