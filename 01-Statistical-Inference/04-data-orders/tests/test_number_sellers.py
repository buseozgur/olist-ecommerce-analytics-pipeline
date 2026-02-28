from nbresult import ChallengeResultTestCase


class TestNumberSellers(ChallengeResultTestCase):
    def test_number_seller(self):
        self.assertEqual(self.result.shape, (98666,2))

    def test_column_names(self):
        expected_columns = sorted(['order_id', 'number_of_sellers'])
        self.assertListEqual(sorted(self.result.columns), expected_columns)
