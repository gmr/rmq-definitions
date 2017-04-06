import argparse
import json
import tempfile
import unittest
import uuid

import mock
import requests_mock

import rmq_definitions


class DictListKeyTestCase(unittest.TestCase):

    def test_invalid_key(self):
        value = {'foo': 'bar'}
        result = rmq_definitions.dict_list_key(value)
        self.assertDictEqual(result, value)

    def test_valid_key(self):
        expectation = 'bar'
        result = rmq_definitions.dict_list_key({'name': expectation})
        self.assertEqual(result, expectation)


class NestedSortTestCase(unittest.TestCase):

    def test_unexpected_list_of_values(self):
        with self.assertRaises(ValueError):
            rmq_definitions.nested_sort([{'bar': 'baz'}, [123, 456]])



class GetDefinitionsTestCase(unittest.TestCase):

    def test_method_returns_dict(self):
        expectation = {'fake': 'data', 'value': str(uuid.uuid4())}
        with requests_mock.mock() as request:
            request.register_uri(
                'GET', 'http://localhost:15672/api/definitions',
                status_code=200, text=json.dumps(expectation))

            args = rmq_definitions.parse_cli_arguments([])
            response = rmq_definitions.get_definitions(args)
            self.assertDictEqual(response, expectation)


    def test_connection_error_raises_request_exception(self):
        args = rmq_definitions.parse_cli_arguments(
            ['--url', 'http://255.255.255.255:15672'])
        with self.assertRaises(rmq_definitions.RequestException):
            rmq_definitions.get_definitions(args)

    def test_error_response_raises_request_exception(self):
        with requests_mock.mock() as request:
            request.register_uri(
                'GET', 'http://localhost:15672/api/definitions',
                status_code=400, text='{"error": "test error"}')

            args = rmq_definitions.parse_cli_arguments([])
            with self.assertRaises(rmq_definitions.RequestException):
                rmq_definitions.get_definitions(args)


class JSONValueTestCase(unittest.TestCase):

    @staticmethod
    def read_expectation():
        with open('test-data/expectation.json', 'r') as handle:
            return '{}\n'.format(
                json.dumps(json.load(handle), sort_keys=True, indent=2))


class OutputTestCase(JSONValueTestCase):

    def test_output_expectations(self):
        expectation = self.read_expectation()
        with open('test-data/from-rmq.json', 'r') as handle:
            definitions = json.load(handle)

        with tempfile.TemporaryFile(mode='w+') as test_file:
            rmq_definitions.write_definitions(test_file, definitions)
            test_file.seek(0)
            self.assertEqual(test_file.read(), expectation)


class MainTestCase(JSONValueTestCase):

    def test_from_file_specified(self):
        expectation = self.read_expectation()
        with tempfile.NamedTemporaryFile(mode='w+') as test_file:
            args = rmq_definitions.parse_cli_arguments(
                ['-f', 'test-data/from-rmq.json', test_file.name])
            with mock.patch('rmq_definitions.parse_cli_arguments') as cliargs:
                cliargs.return_value = args
                rmq_definitions.main()
            test_file.seek(0)
            self.assertEqual(test_file.read(), expectation)

    def test_from_rabbitmq(self):
        expectation = self.read_expectation()
        with open('test-data/from-rmq.json', 'r') as handle:
            definitions = handle.read()
        with requests_mock.mock() as request:
            request.register_uri(
                'GET', 'http://localhost:15672/api/definitions',
                status_code=200, text=definitions)
            with tempfile.NamedTemporaryFile(mode='w+') as test_file:
                args = rmq_definitions.parse_cli_arguments([test_file.name])
                with mock.patch(
                        'rmq_definitions.parse_cli_arguments') as cliargs:
                    cliargs.return_value = args
                    rmq_definitions.main()
                test_file.seek(0)
                self.assertEqual(test_file.read(), expectation)

    def test_from_rabbitmq_with_error(self):
        args = rmq_definitions.parse_cli_arguments([])
        with mock.patch('rmq_definitions.parse_cli_arguments') as cliargs:
            cliargs.return_value = args
            error_string = 'error {}'.format(str(uuid.uuid4()))
            with requests_mock.mock() as request:
                request.register_uri(
                    'GET', 'http://localhost:15672/api/definitions',
                    status_code=400, text=json.dumps({'error': error_string}))

                with mock.patch('sys.stderr') as stderr:
                    with self.assertRaises(SystemExit) as system_exit:
                        rmq_definitions.main()
                        self.assertEqual(system_exit.args[0], 1)
                    stderr.assert_has_calls([
                        mock.call.write('ERROR: {}\n'.format(error_string))
                    ])
