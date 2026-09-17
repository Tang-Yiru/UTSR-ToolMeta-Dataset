# Data Quality

The public main set contains 7,593 valid declaration records. The inherited `high_confidence` subset reflects declaration-quality screening, not measured functional-profile accuracy or verified executable behavior.

All current records carry ten-field derived functional profiles. Rule-based pre-annotation and AI-assisted per-record semantic review were used. Labels are not human gold. Missing evidence remains unknown; sixteen known parsing-gap records retain abstaining profiles.

Record-level schemas validate data shape. They do not establish the correctness of every input schema, label, or backend binding. Use the version-local SHA-256 manifest to verify distribution integrity, and independently verify actual tools before execution.
