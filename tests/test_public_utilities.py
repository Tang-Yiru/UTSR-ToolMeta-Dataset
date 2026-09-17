import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


S = load_module('summarize_dataset')
V = load_module('verify_release')


class PublicUtilitiesTests(unittest.TestCase):
    def test_structured_intent_statistics(self):
        row = {'source_meta': {'source_family': 'mcp'}, 'function_profile': {
            'primary_domain': 'developer_tools', 'primary_subdomain': None,
            'primary_action': None, 'supported_actions': ['create', 'delete'],
            'action_mode': 'multi', 'effect_class': 'mixed', 'cardinality': 'unknown',
            'task_intent': {'actions': ['create', 'delete'], 'object': 'file',
                            'qualifiers': [], 'canonical_text': None}}}
        summary = S.summarize([row, row])
        self.assertEqual(summary['task_intent_unique'], 1)
        self.assertEqual(summary['primary_action_counts'], {'__null__': 2})
        self.assertEqual(summary['supported_action_counts'], {'create': 2, 'delete': 2})
        self.assertEqual(summary['primary_domain_counts'], {'developer_tools': 2})

    def test_release_manifest(self):
        self.assertEqual(V.verify(ROOT / 'releases/v0.2'), 7)

    def test_manifest_rejects_missing_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'MANIFEST.sha256').write_text('# empty\n', encoding='utf-8')
            (root / 'unlisted.json').write_text('{}', encoding='utf-8')
            with self.assertRaises(ValueError):
                V.verify(root)

    def test_manifest_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'MANIFEST.sha256').write_text('0' * 64 + '  1  ../outside\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                V.verify(root)

    def test_full_statistics_match(self):
        release = ROOT / 'releases/v0.2'
        summary = S.summarize(list(S.iter_jsonl(release / 'data/utsr_records.release_valid.jsonl')))
        expected = json.loads((release / 'statistics.json').read_text(encoding='utf-8'))
        for key, value in expected.items():
            self.assertEqual(summary[key], value, key)

    def test_schema_and_privacy_projection(self):
        from jsonschema import Draft202012Validator
        release = ROOT / 'releases/v0.2'
        schema = json.loads((release / 'schema/utsr_record.schema.json').read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        rows = list(S.iter_jsonl(release / 'data/utsr_records.core_balanced.jsonl'))
        self.assertEqual(len(rows), 2000)
        for row in rows:
            validator.validate(row)
            self.assertEqual(set(row['provenance']), {'raw_descriptor_ref'})
            self.assertNotIn('field_origin_map', row['utsr']['source'])
            self.assertEqual(len(row['function_profile']), 10)


if __name__ == '__main__':
    unittest.main()
