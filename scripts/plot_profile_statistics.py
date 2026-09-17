"""Render descriptive profile charts and README tables from public statistics."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'stats/v0.2/dataset_statistics.json'
LABELS = {
    'natural_language_processing': 'Natural language processing',
    'artificial_intelligence_machine_learning': 'AI and machine learning',
    'external_side_effect': 'External side effect',
    'tool_benchmark': 'Tool benchmarks',
    'function_calling_dataset': 'Function-calling datasets',
    'framework_tool': 'Framework tools',
    'mcp': 'MCP', 'openapi': 'OpenAPI',
}


def label(key):
    return LABELS.get(key, key.replace('_', ' ').capitalize())


def ordered(counts):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


def table(title, counts, total):
    rows = [f'#### {title}', '', '| Category | Records | Share of main set |',
            '|---|---:|---:|']
    rows.extend(f'| `{key}` | {value:,} | {100 * value / total:.2f}% |'
                for key, value in ordered(counts))
    return '\n'.join(rows)


def source_table(stats):
    rows = ['| Source family | Records | Share |', '|---|---:|---:|']
    rows.extend(f'| {label(key)} | {value:,} | {100 * value / stats["records"]:.2f}% |'
                for key, value in ordered(stats['source_family']))
    return '\n'.join(rows)


def functional_tables(stats):
    n = stats['records']
    coverage = ['#### Evidence Availability', '', '| Dimension | Known labels | Unknown labels |',
                '|---|---:|---:|']
    for title, field in [('Domain', 'primary_domain'), ('Action mode', 'action_mode'),
                         ('Direct effect', 'effect_class'), ('Cardinality', 'cardinality')]:
        missing = stats[field + '_counts']['unknown']
        coverage.append(f'| {title} | {n - missing:,} ({100 * (n - missing) / n:.2f}%) | '
                        f'{missing:,} ({100 * missing / n:.2f}%) |')
    coverage.append('')
    coverage.append('A known label means the annotation is not `unknown`; it does not establish correctness.')
    return '\n\n'.join([
        '\n'.join(coverage),
        table('Supported Actions (Multi-label)', stats['supported_action_counts'], n),
        table('Direct Effects', stats['effect_class_counts'], n),
        table('Object Cardinality', stats['cardinality_counts'], n),
        table('Action Modes', stats['action_mode_counts'], n)])


def replace_block(text, name, content):
    start = f'<!-- {name}:start -->'
    end = f'<!-- {name}:end -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f'Missing or repeated README marker: {name}')
    before, tail = text.split(start)
    _, after = tail.split(end)
    return before + start + '\n' + content + '\n' + end + after


def draw(stats):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator, StrMethodFormatter

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.spines.left': False, 'axes.edgecolor': '#cbd0d4',
                         'axes.labelcolor': '#384047', 'text.color': '#242a2f',
                         'xtick.color': '#58636c', 'ytick.color': '#384047',
                         'svg.fonttype': 'none', 'savefig.facecolor': 'white'})
    n = stats['records']
    assets = ROOT / 'assets'
    assets.mkdir(exist_ok=True)

    def bars(ax, entries, color):
        ax.barh(range(len(entries)), [v for _, v in entries], height=.64,
                color=[('#90999f' if k == 'unknown' else color) for k, _ in entries])
        ax.set_yticks(range(len(entries)), [label(k) for k, _ in entries])
        ax.invert_yaxis()
        ax.tick_params(axis='y', length=0, pad=8)
        ax.xaxis.set_major_locator(MaxNLocator(4, integer=True))
        ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        ax.set_axisbelow(True)
        ax.grid(axis='x', color='#e6eaed', linewidth=.7)
        highest = max(v for _, v in entries)
        ax.set_xlim(0, highest * 1.55)
        annotations = []
        for i, (_, value) in enumerate(entries):
            annotations.append(ax.text(value + highest * .025, i,
                                      f'{value:,}  ({100 * value / n:.2f}%)',
                                      va='center', fontsize=9.5))
        ax.set_xlabel('Records', labelpad=8)
        return annotations

    def save(fig, annotations, name):
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        for annotation in annotations:
            bbox = annotation.get_window_extent(renderer)
            if not fig.bbox.contains(bbox.x0, bbox.y0) or not fig.bbox.contains(bbox.x1, bbox.y1):
                raise ValueError('Count annotation falls outside the figure')
        fig.savefig(assets / name, dpi=180, metadata={'Software': 'UTSR-ToolMeta'})
        plt.close(fig)

    domains = ordered({k: v for k, v in stats['primary_domain_counts'].items() if k != 'unknown'})
    top = domains[:12]
    rest = sum(v for _, v in domains[12:])
    other_key = f'other_{len(domains) - 12}_named_domains'
    LABELS[other_key] = f'Other {len(domains) - 12} named domains'
    entries = top + [(other_key, rest), ('unknown', stats['primary_domain_counts']['unknown'])]
    fig, ax = plt.subplots(figsize=(11.2, 6.7))
    fig.subplots_adjust(left=.29, right=.95, top=.83, bottom=.13)
    fig.text(.04, .95, 'Functional domains', fontsize=19, weight='bold')
    fig.text(.04, .90, f'Main set: {n:,} records | {len(domains)} named L1 domains + unknown', fontsize=11)
    annotations = bars(ax, entries, '#4d809e')
    fig.text(.04, .035, 'Top 12 named domains; remaining named domains aggregated. Counts describe labels, not accuracy.', fontsize=9)
    save(fig, annotations, 'functional_domains.png')

    fig, axes = plt.subplots(2, 2, figsize=(13.2, 10.3))
    fig.subplots_adjust(left=.16, right=.97, top=.86, bottom=.09, wspace=.62, hspace=.40)
    fig.text(.04, .965, 'Four dimensions of functional profiles', fontsize=20, weight='bold')
    fig.text(.04, .92, f'Main set: {n:,} records | counts and percentages of records', fontsize=11)
    plans = [
        ('a  Supported actions', 'supported_action_counts', '#4d809e'),
        ('b  Direct effects', 'effect_class_counts', '#4e8c79'),
        ('c  Object cardinality', 'cardinality_counts', '#9b774f'),
        ('d  Action modes', 'action_mode_counts', '#7786a4')]
    annotations = []
    for ax, (title, field, color) in zip(axes.flat, plans):
        ax.set_title(title, loc='left', fontsize=13, weight='bold', pad=14)
        annotations.extend(bars(ax, ordered(stats[field]), color))
    fig.text(.04, .025, 'Supported actions are multi-label and need not sum to 100%. Other panels partition records. No accuracy is inferred.', fontsize=9.5)
    save(fig, annotations, 'functional_dimensions.png')


def main():
    stats = json.loads(SOURCE.read_text(encoding='utf-8'))
    for field in ('source_family', 'primary_domain_counts', 'effect_class_counts',
                  'cardinality_counts', 'action_mode_counts'):
        if sum(stats[field].values()) != stats['records']:
            raise ValueError(f'Invalid count partition: {field}')
    draw(stats)
    readme = ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8')
    text = replace_block(text, 'source-statistics', source_table(stats))
    text = replace_block(text, 'functional-statistics', functional_tables(stats))
    readme.write_text(text, encoding='utf-8', newline='\n')
    print(f'Updated two charts and README tables from {stats["records"]:,} records.')


if __name__ == '__main__':
    main()
