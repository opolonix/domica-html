import sys
import unittest


sys.path.insert(0, "src")

import domica_html


class PublicApiTests(unittest.TestCase):
    def test_all_names_are_exported(self):
        missing = [name for name in domica_html.__all__ if not hasattr(domica_html, name)]
        self.assertEqual(missing, [])

    def test_star_import_uses_public_api(self):
        namespace = {}
        exec("from domica_html import *", namespace)

        for name in domica_html.__all__:
            self.assertIn(name, namespace)

    def test_expected_html_tags_are_available(self):
        for name in ("header", "footer", "table", "img", "hr", "style_item"):
            self.assertTrue(hasattr(domica_html, name), name)


if __name__ == "__main__":
    unittest.main()
