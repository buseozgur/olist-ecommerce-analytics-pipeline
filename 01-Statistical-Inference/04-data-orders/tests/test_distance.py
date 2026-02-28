from nbresult import ChallengeResultTestCase
import pytest

@pytest.mark.optional
class TestDistance(ChallengeResultTestCase):
    def test_distance(self):
        self.assertGreater(self.result.mean, 580)
        self.assertLess(self.result.mean, 620)
