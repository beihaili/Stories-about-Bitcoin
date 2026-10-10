import re
import unittest

from scripts import build_zh


class ChineseSummaryTests(unittest.TestCase):
    def test_summary_contains_all_39_chapters(self):
        chapters = build_zh.find_chapters()
        summary = build_zh.build_summary(chapters)
        summary_links = re.findall(r"^\* \[[^]]+\]\(([^)]+\.md)\)$", summary, re.MULTILINE)
        chapter_links = [link for link in summary_links if link != "INTRO.md"]

        self.assertEqual(len(chapters), 39)
        self.assertEqual(len(chapter_links), 39)
        self.assertEqual({path.name for _, _, path in chapters}, set(chapter_links))


class WebsiteMetadataTests(unittest.TestCase):
    def test_public_metadata_uses_current_book_scope(self):
        expected_by_file = {
            "new-website/src/components/home/Hero.jsx": ("39", "9", "1976-2025"),
            "new-website/src/App.jsx": ("39", "1976-2025"),
            "new-website/index.html": ("39", "9", "1976-2025"),
            "new-website/public/manifest.json": ("39", "9", "1976-2025"),
            "new-website/public/og-image.svg": ("39", "9", "1976-2025"),
            "new-website/README.md": ("39", "9", "1976-2025"),
        }

        for relative_path, expected_values in expected_by_file.items():
            with self.subTest(path=relative_path):
                content = (build_zh.REPO_ROOT / relative_path).read_text(encoding="utf-8")
                for expected in expected_values:
                    self.assertIn(expected, content)


if __name__ == "__main__":
    unittest.main()
