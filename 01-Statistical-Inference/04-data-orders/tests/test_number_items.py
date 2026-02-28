from nbresult import ChallengeResultTestCase


class TestNumberItems(ChallengeResultTestCase):
    def test_number_items(self):
        self.assertEqual(self.result.shape, (98666, 2))

    def test_column_names(self):
        expected_columns = sorted(['order_id', 'number_of_items'])
        self.assertListEqual(sorted(self.result.columns), expected_columns)
