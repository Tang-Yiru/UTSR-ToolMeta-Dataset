import importlib.util
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('plot_profile_statistics', ROOT / 'scripts/plot_profile_statistics.py')
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)


class ReadmeStatisticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stats = json.loads((ROOT / 'stats/v0.2/dataset_statistics.json').read_text(encoding='utf-8'))
        cls.readme = (ROOT / 'README.md').read_text(encoding='utf-8')

    def test_single_documentation_entry(self):
        paths = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.md') if '.git' not in p.parts]
        self.assertEqual(paths, ['README.md'])
        self.assertTrue((ROOT / 'LICENSE').is_file())
        self.assertTrue((ROOT / 'CITATION.cff').is_file())

    def test_readme_tables_match_actual_statistics(self):
        self.assertIn(P.source_table(self.stats), self.readme)
        self.assertIn(P.functional_tables(self.stats), self.readme)

    def test_partitions_and_multilabel_denominator(self):
        self.assertEqual(self.stats['records'], 7593)
        for field in ('source_family', 'primary_domain_counts', 'action_mode_counts',
                      'effect_class_counts', 'cardinality_counts'):
            self.assertEqual(sum(self.stats[field].values()), 7593)
        self.assertGreater(sum(self.stats['supported_action_counts'].values()), 7593)
        self.assertIn('multi-label', self.readme)
        self.assertIn('not accuracy estimates', self.readme)

    def test_png_exports_are_present_and_large_enough(self):
        for name in ('functional_domains.png', 'functional_dimensions.png'):
            image = (ROOT / 'assets' / name).read_bytes()
            self.assertEqual(image[:8], b'\x89PNG\r\n\x1a\n')
            width, height = struct.unpack('>II', image[16:24])
            self.assertGreaterEqual(width, 1600)
            self.assertGreaterEqual(height, 1000)

    def test_notice_and_license_content_preserved(self):
        for text in ('No blanket license', 'unknown license metadata',
                     'upstream endorsement', 'corrections or removals',
                     'AI participation is declared here at dataset level', 'not human gold'):
            self.assertIn(text.lower(), self.readme.lower())

    def test_generated_readme_block_is_idempotent(self):
        text = P.replace_block(self.readme, 'functional-statistics', P.functional_tables(self.stats))
        self.assertEqual(text, self.readme)
        with self.assertRaises(ValueError):
            P.replace_block('no markers', 'missing', 'content')


if __name__ == '__main__':
    unittest.main()
