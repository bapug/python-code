#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse


def main():
    """
    Example of using the argparse module

    https://docs.python.org/2.7/library/argparse.html
    """

    usage = """
    %(prog)s [options]

    This command does awesome stuff.
    It includes a lot of parameters also, which are described below.
    When using this command, make sure you have "Project X" checked-out
    and you are in the top level directory.

"""

    parser = argparse.ArgumentParser(
        description="Example Argument Parser",
        usage=usage,
        epilog="We sure hope you enjoy our new command!"
    )

    parser.add_argument(
        'required_arg',
        action= 'store', # This is defaulted
        help="Enter the required arg."
    )

    parser.add_argument(
        '-a','--arg',
        help="Add a single value to the 'arg' arg."
    )

    parser.add_argument(
        '-l', '--list',
        nargs='*',
        help="Here you can specify a bunch of stuff."
    )

    parser.add_argument(
        '-v','--verbose',
        action='store_true',
        help="set this to turn on the verbose level."
    )

    args = parser.parse_args()

    if args.verbose:

        print("Requried arg: {0}".format(args.required_arg))

        if args.arg:
            print("A single 'arg' was passed as: {0}".format(args.arg))

        if args.list:
            print("A list of args was passed as \n\t{0}".format("\n\t".join(args.list)))

    else:
        print("Use verbose mode if you want to see results.")

    print("\n\nAnd, now do something with these arguments!!")


if __name__ == "__main__":
    main()



