from unittest import TestCase
from SearchEngine import SearchEngine


class TestSearchEngine(TestCase):

    def setUp(self):
        self.se = SearchEngine(1000, 'word2vec.glove.6B.300d.txt', 'sum', forcebin=True)

    def test_execute_query_Summation(self):

        self.se.combine = 'sum'
        self.assertEqual(self.se.execute_query('lose', 'alcohol', False, False),
                         [('booze', 23), ('laws', 228), ('lows', 578), ('dues', 621), ("law's", 766)])
        self.assertEqual(self.se.execute_query('summarize', 'warrior', False, False),
                         [("samurai's", 1), ('samurais', 1), ('warriors', 100000000), ('somers', 100000002),
                          ('dragon', 100000002)])

    def test_execute_query_Multiplication(self):
        self.se.combine = 'prod'
        self.assertEqual(self.se.execute_query('lose', 'alcohol', False, False),
                         [('booze', 114), ('laws', 6501), ('dues', 9120), ("law's", 23552), ('lows', 38304)])
        self.assertEqual(self.se.execute_query('summarize', 'warrior', False, False),
                         [('samurais', 1), ("samurai's", 2), ('warriors', 100000000), ('somers', 100000002),
                          ('dragon', 100000002)])

    def tearDown(self):
        pass
