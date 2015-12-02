#!/usr/bin/python

import argparse
import logging
import os
import json
from gevent.server import StreamServer
from module import Module


def json_repr(obj):
    """Represent instance of a class as JSON.
    Arguments:
    obj -- any object
    Return:
    String that reprent JSON-encoded object.
    """
    def serialize(obj):
        """Recursively walk object's hierarchy."""
        if isinstance(obj, (bool, int, long, float, basestring)):
            return obj
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                obj[key] = serialize(obj[key])
            return obj
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        elif hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        else:
            return repr(obj)  # Don't know how to handle, convert to string
    return json.dumps(serialize(obj))


def handle(socket, address):
    log.info("Connection received from {}".format(str(address)))
    log.info("Creating ServerGameAdapter...")
    log.debug("Creating fileobj")
    fileobj = socket.makefile()

    while True:
        # Listen for commands
        log.debug("Waiting for commands...")
        line = fileobj.readline()
        if not line:
            log.info("Client disconnected...")
            # game.save()
            break
        # Process line as a command
        command_dict = json.loads(line)
        log.debug("Command from client: '%s'" % str(command_dict))
        if len(command_dict.keys()) is 1:
            command = command_dict.keys()[0]
            method = getattr(game, str(command), None)
            if method:
                log.info("Command is '%s'" % str(command))
                method(command_dict[command])
            else:
                log.error("Command '{}' not found in ServerGameAdapter".format(
                    str(command)))
        else:
            log.error("Command dictionary from client includes multiple keys")

        # Respond to command
        state, commands = game.state()
        data = {'state': state, 'commands': commands}
        fileobj.write(json.dumps(data))
        fileobj.write("\n")
        fileobj.flush()

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Manage a m31 server.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--bigbang', action='store_true',
                        help='Delete everything before starting')
    parser.add_argument('-H', '--host', default='0.0.0.0',
                        help='Address the server should listen on.')
    parser.add_argument('-P', '--port', default=10344,
                        help='Port to use for server.')
    parser.add_argument('--version', action='version', version='0')
    args = parser.parse_args()

    # Setup logging options
    log_level = logging.DEBUG if args.debug else logging.INFO
    log = logging.getLogger(os.path.basename(__file__))
    log.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s:'
        '%(funcName)s(%(lineno)i):%(message)s')

    # Console Logging
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # File Logging
    fh = logging.FileHandler(os.path.basename(__file__) + '.log')
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # Load modules
    log.info("Importing modules...")
    from modules import *
    log.info("Loading modules...")
    modules = [m(log) for m in Module.modules]

    server = StreamServer((args.host, args.port), handle)
    log.info("Server initialized on {}:{}, listening...".format(
        str(args.host), str(args.port)))
    server.serve_forever()
