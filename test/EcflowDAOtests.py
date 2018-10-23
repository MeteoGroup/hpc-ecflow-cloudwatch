from EcflowDAO import EcflowDAO
import unittest


class TestEcflowDAO(unittest.TestCase):

    dao = EcflowDAO()
    output = dao.fetch_ecflow_stats()
    print(output)

