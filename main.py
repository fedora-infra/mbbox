#!/usr/bin/env python3
import argparse
import logging

import mbox.ca
import mbox.state


def parse_args():
    parser = argparse.ArgumentParser(description="Modular Builder in a Box")
    parser.add_argument("config_file", default="./mbox.yml",
                        help="Configuration file path")
    parser.add_argument("--debug", action='store_true', default=False,
                        help='Enable debugging')
    parser.add_argument("--force-update", action='append', default=[],
                        help="Force this component to be updated")
    # TODO
    return parser.parse_known_args()


def main():
    args, extra = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")

    logger.debug("Initializing objects")
    state = mbox.state.State(
        config_file=args.config_file,
        print_oc_output=args.debug,
    )

    logger.debug("Running OC test")
    state.oc_test()

    if len(extra) > 0 and extra[0] == 'koji':
        out = state.client.run_koji_command(*extra[1:])
        print("Retcode: %s" % out.returncode)
        print("Stdout: %s" % out.stdout)
        print("Stderr: %s" % out.stderr)
        return

    state.build_all()
    state.ensure_all(
        forced=args.force_update,
    )


if __name__ == '__main__':
    main()
