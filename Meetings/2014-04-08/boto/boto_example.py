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

    parser.parse_args()


if __name__ == "__main__":
    main()



