"""
Copyright 2015 Ben Lopatin
"""
__version__ = '0.1.0a'

import sys
from magwitch import commands


command_dict = {
    'requires': commands.requires,
    'required_by': commands.required_by,
}


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if not len(args):
        sys.exit("You must specify a command")
    cmd_name = args[0]
    cmd_args = args[1:]

    try:
        command = command_dict[cmd_name](cmd_args)
    except KeyError:
        sys.exit("No such command %s" % cmd_name)

    return command(cmd_args)


if __name__ == '__main__':
    main(sys.argv[1:])
