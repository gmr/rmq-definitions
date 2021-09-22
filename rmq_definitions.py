"""
rmq-definitions
===============

Deterministicly sort and format RabbitMQ definition backups

"""
import argparse
import json
import sys

import requests


def dict_list_key(item):
    """Provide the value to sort the dictionary item on.

    :param dict item: The item to sort
    :rtype: mixed

    """
    if 'vhost' in item and 'name' in item:
        return item['vhost'], item['name']
    elif 'user' in item and 'vhost' in item:
        return item['user'], item['vhost']
    elif 'vhost' in item and 'source' in item and 'destination' in item:
        return item['vhost'], item['source'], item['destination']
    for key in {'name', 'user'}:
        if key in item:
            return item[key]
    return item


def get_definitions(args):
    """Make the HTTP Request to RabbitMQ to retrieve the RabbitMQ definitions.

    :param argparse.namespace args: CLI argument values
    :rtype: dict
    :raises: RequestException

    """
    try:
        response = requests.get(
            '{}/api/definitions'.format(args.url.rstrip('/')),
            auth=(args.username, args.password))
    except requests.RequestException as error:
        raise RequestException(error.__class__.__name__)
    if not response.ok:
        error = response.json()
        raise RequestException(error.get('reason', error.get('error')))
    return response.json()


def nested_sort(value):
    """Perform a recursive sort on the provided item.

    :param mixed item: The item to sort
    :rtype: mixed
    :raises: ValueError

    """
    if isinstance(value, dict):
        return {k: nested_sort(v) for k, v in value.items()}
    elif isinstance(value, list):
        if all([isinstance(i, dict) for i in value]):
            return sorted(value, key=dict_list_key)
        raise ValueError('Unexpected list with mismatched data types')
    return value


def parse_cli_arguments(cli_args=None):  # pragma: nocover
    """Return the parsed CLI arguments for the application invocation.

    :param list cli_args: CLI args to parse instead of from command line
    :rtype: argparse.namespace

    """
    parser = argparse.ArgumentParser(
        'rmq-sorted-definitions',
        description='Deterministicly sort and format RabbitMQ definition '
                    'backups')
    parser.add_argument(
        '--url', default='http://localhost:15672',
        help='The RabbitMQ Management API base URL. Default: %(default)s')
    parser.add_argument(
        '-u', '--username', default='guest',
        help='The RabbitMQ Management API username. Default: %(default)s')
    parser.add_argument(
        '-p', '--password', default='guest',
        help='The RabbitMQ Management API password. Default: %(default)s')
    parser.add_argument(
        '-f', '--from-file', type=argparse.FileType('r'),
        help='Read definitions from a file instead of the Management API')
    parser.add_argument(
        'file', default=sys.stdout, type=argparse.FileType('w'), nargs='?',
        metavar='DESTINATION',
        help='Location to write the definitions to. Default: STDOUT')
    return parser.parse_args(cli_args)


def write_definitions(handle, definitions):
    """Write the sorted definitions

    :param file handle: The open file handle
    :param dict definitions: The parsed definitions from RabbitMQ

    """
    value = json.dumps(
        nested_sort(definitions), sort_keys=True, indent=2)
    handle.write('{}\n'.format(value))


def main():
    """Application Entrypoint"""
    args = parse_cli_arguments()

    try:
        if args.from_file:
            definitions = json.load(args.from_file)
        else:
            definitions = get_definitions(args)
    except (RequestException, ValueError) as error:
        sys.stderr.write('ERROR: {}\n'.format(error))
        sys.exit(1)

    with args.file as handle:
        write_definitions(handle, definitions)


class RequestException(Exception):
    """Raised when we can not download the definitions from RabbitMQ"""


if __name__ == '__main__':  # pragma: nocover
    main()
