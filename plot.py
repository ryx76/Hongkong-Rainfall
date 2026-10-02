# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib==3.10.8"]
# ///

import csv
from datetime import date
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
HERE = Path(__file__).resolve().parent
DATA = HERE / 'data' / 'daily_HKO_RF_2025.csv'
OUT = HERE / 'out' / 'rainfall-2025-weekly.png'

def read_daily_data():
    rows = []
    with DATA.open(encoding='utf-8-sig', newline='') as f:
        for r in csv.reader(f):
            if len(r) != 5 or not r[0].isdigit():
                continue
            y, m, d, v, q = r
            if q != 'C' or v == '***':
                raise ValueError(f'Unavailable or incomplete record: {r}')
            rows.append((date(int(y), int(m), int(d)), 0.0 if v == 'Trace' else float(v)))
    expected = [date.fromordinal(date(2025, 1, 1).toordinal() + i) for i in range(365)]
    if [d for d, v in rows] != expected:
        raise ValueError('Expected all 365 dates of 2025 in chronological order.')
    return rows

def main():
    rows = read_daily_data()
    weeks = [rows[i:i + 7] for i in range(0, len(rows), 7)]
    means = [sum((v for d, v in w)) / len(w) for w in weeks]
    x = list(range(1, len(weeks) + 1))
    peak = means.index(max(means))
    print('Weeks:', len(weeks), 'last week days:', len(weeks[-1]), 'highest:', peak + 1, means[peak], weeks[peak][0][0], weeks[peak][-1][0])
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
    fig, ax = plt.subplots(figsize=(18, 8.5), facecolor='white')
    fig.subplots_adjust(left=0.065, right=0.982, bottom=(0.245 * 7.8 + 0.7) / 8.5, top=(0.79 * 7.8 + 0.7) / 8.5)
    blue = '#397DB2'
    orange = '#EA8B28'
    red = '#D84B4B'
    ax.bar(x, means, width=0.68, color=[red if i == peak else blue for i in range(len(weeks))], zorder=2)
    ax.plot(x, means, color=orange, linewidth=1.8, marker='o', markersize=3.7, zorder=3)
    for i, v in zip(x, means):
        ax.annotate(f'{v:.1f}', (i, v), xytext=(0, 7), textcoords='offset points', ha='center', va='bottom', fontsize=8.5, color='#303B48', zorder=4)
    ax.set_xlim(0.25, 53.75)
    ax.set_ylim(0, max(means) * 1.19)
    ax.set_xticks(x, [f'W{i}' for i in x], rotation=90, fontsize=9)
    ax.set_xlabel('Week of 2025', labelpad=47, color='#455261')
    ax.set_ylabel('Average daily rainfall (mm/day)', labelpad=13, color='#455261')
    ax.grid(axis='y', color='#E3E8ED', linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    for s in ['left', 'bottom']:
        ax.spines[s].set_color('#BEC8D1')
    ax.tick_params(axis='both', length=0, pad=7, labelcolor='#455261')
    fig.text(0.065, (0.935 * 7.8 + 0.7) / 8.5, '2025 rainfall at the Hong Kong Observatory', fontsize=23, weight='bold', color='#24384A')
    fig.text(0.065, (0.889 * 7.8 + 0.7) / 8.5, 'Weekly average daily rainfall · 365 daily records grouped into 53 weeks', fontsize=13, color='#667585')
    ax.legend(handles=[Patch(color=blue, label='Weekly daily average'), Line2D([0], [0], color=orange, marker='o', label='Same averages connected'), Patch(color=red, label='Highest weekly average')], loc='lower left', bbox_to_anchor=(0, 1.025), ncol=3, frameon=False, fontsize=10.5, borderaxespad=0)
    fig.text(0.065, 0.095 * 7.8 / 8.5, 'Week 1 = Jan 1–7; each following week spans 7 days. Week 53 = Dec 31 only (1 day).', fontsize=10, color='#667585')
    fig.text(0.065, 0.062 * 7.8 / 8.5, 'Each value = rainfall total ÷ days in that week. Labels rounded to 1 decimal; Trace (<0.05 mm) plotted as 0.', fontsize=10, color='#667585')
    fig.text(0.065, 0.029 * 7.8 / 8.5, 'Source: Hong Kong Observatory · daily_HKO_RF_2025.csv · Observatory station data', fontsize=10, color='#667585')
    timeline = fig.add_axes([0.065, (0.245 * 7.8 + 0.7 - 0.65) / 8.5, 0.917, 0.025])
    timeline.set_xlim(ax.get_xlim())
    timeline.set_ylim(0, 1)
    timeline.axis('off')
    bounds = [0.5 + (date(2025, m, 1) - date(2025, 1, 1)).days / 7 for m in range(1, 13)] + [53.5]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i, label in enumerate(months):
        left, right = bounds[i:i + 2]
        timeline.plot([left, right], [0.65, 0.65], color='#91A3B3', linewidth=1.2, clip_on=False)
        timeline.text((left + right) / 2, -0.12, label, ha='center', va='top', fontsize=10, color='#455261', clip_on=False)
    for boundary in bounds:
        timeline.plot([boundary, boundary], [0.35, 0.95], color='#91A3B3', linewidth=1.2, clip_on=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=180, facecolor='white')
    plt.close(fig)
    print(f'Saved {OUT}')
if __name__ == '__main__':
    main()
