from EcflowDAO import EcflowDAO
import unittest

from ecflow_state_parser import EcflowStateParser


class TestEcflowDAO(unittest.TestCase):

    dao = EcflowDAO()
    output = dao.fetch_ecflow_stats()
    parser = EcflowStateParser()
    parser.parse_ecflow_state(output)


