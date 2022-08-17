import unittest

import extractor
import sample_data


class TestExtractor(unittest.TestCase):

    # this isn't a good test.
    # it depends on an external system AND doesn't really prove anything.
    # if it turns out to be flaky, I'll remove it again
    def test_full(self):
        extractor.extract_info.__wrapped__(sample_data.vm_base + sample_data.vm_code_working)
