"""\
PySplendor: Splendor board game in command line interface
This file parses command line arguments and passes them to CmdUtil
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from cmdutil import CmdUtil
VERSION = "PySplendor 1.0"

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="PySplendor",
        description="Splendor board game in command line interface",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('human', metavar='human', type=int, nargs='?', choices=range(5), default=1,
                        help='Type number of human players [between 0-4]')
    parser.add_argument('ai', metavar='ai', type=int, nargs='?', choices=range(5), default=1,
                        help='Type number of AI players [between 0-4]')
    parser.add_argument('score', metavar='score', type=int, nargs='?', choices=[15, 21], default=15,
                        help='Type the win score [either 15 or 21]')
    parser.add_argument('--sleep', type=float, default=0.2,
                        help='Enter AI sleep parameter in range [0.0, 0.5]')
    args = parser.parse_args()

    if not 2 <= args.human + args.ai <= 4:
        parser.error("Total player number should be between 2 and 4")

    if not 0 <= args.sleep <= 0.5:
        parser.error("Sleep duration should be between 0 and 0.5 second")

    # Pass arguments to CmdUtil and start the command line loop
    app = CmdUtil(args.human, args.ai, args.score, args.sleep)
    app.cmdloop()
