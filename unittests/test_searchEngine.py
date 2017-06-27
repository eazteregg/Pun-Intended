from unittest import TestCase
from SearchEngine import SearchEngine


class TestSearchEngine(TestCase):

    def setUp(self):
        self.se = SearchEngine(1000, 'word2vec.glove.6B.300d.txt', 'sum', forcebin=True)

    def test_execute_query_Summation(self):

        self.se.combine = 'sum'
        self.assertEqual(self.se.execute_query('lose', 'alcohol', False, False),
                         [('booze', 29), ('laws', 234), ('lows', 584), ('dues', 627), ("law's", 772)])
        self.assertEqual(self.se.execute_query('summarize', 'warrior', False, False),
                         [("samurai's", 2), ('samurais', 2), ('summarize', 100000000), ('warriors', 100000000),
                          ('dragon', 100000002)])

    def test_execute_query_Multiplication(self):
        self.se.combine = 'prod'
        self.assertEqual(self.se.execute_query('lose', 'alcohol', False, False),
                         [('booze', 228), ('laws', 7683), ('dues', 12768), ("law's", 27968), ('lows', 41328)])
        self.assertEqual(self.se.execute_query('summarize', 'warrior', False, False),
                         [('samurais', 2), ("samurai's", 4), ('summarize', 100000000), ('warriors', 100000000),
                          ('dragon', 100000002)])

    def tearDown(self):
        pass
