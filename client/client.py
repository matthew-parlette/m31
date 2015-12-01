#!/usr/bin/python

import argparse
import logging
import os
import socket

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Process command line options.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('-H', '--host', default='localhost',
                        help='Hostname for server')
    parser.add_argument('-P', '--port', default=10344,
                        help='Port number for server')
    parser.add_argument('--version', action='version', version='0')
    args = parser.parse_args()

    # Setup logging options
    log_level = logging.DEBUG if args.debug else logging.INFO
    log = logging.getLogger(os.path.basename(__file__))
    log.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s'
        ':%(funcName)s(%(lineno)i):%(message)s')

    # Console Logging
    if args.debug:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        log.addHandler(ch)

    # File Logging
    fh = logging.FileHandler(os.path.basename(__file__) + '.log')
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    log.info("Initializing...")

    # Create Client and connect
    log.info("Connecting to {}:{}".format(
        str(args.host), str(args.port)))
    socket = socket.create_connection(
        (args.host, args.port))
    log.info("Connected to {}:{}".format(
        str(args.host), str(args.port)))

    fileobj = socket.makefile()

    """
    while True:
        command = menu.display()

        if command:
            # Send command
            log.info("Sending command to server: %s" % str(command))
            fileobj.write(json.dumps(command))
            fileobj.write("\n")
            fileobj.flush()

            # Receive state
            log.info("Receiving from server...")
            line = fileobj.readline()
            if not line:
                log.info("Server disconnected")
                break

            log.info("Loading state as json...")
            response = json.loads(line)
            log.info("State received from server: %s" % str(response))
            menu.state = response['state']
            menu.commands = response['commands']
        else:
            # User has quit
            log.info("Exiting game...")
            break
    """
    socket.close()
