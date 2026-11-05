"""Shared paper figure style. Data stay in each figure's source.
Typeface: Nimbus Roman (Times-compatible); Times New Roman unavailable locally.
Layout adapts CCFA heatmap_matrix's directly labelled matrix grammar.
"""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
for f in Path('/usr/share/fonts/opentype/urw-base35').glob('NimbusRoman-*.otf'):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','mathtext.fontset':'stix','axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.6,'axes.edgecolor':'#9AA6AC','text.color':'#000000','axes.labelcolor':'#000000','xtick.color':'#000000','ytick.color':'#000000'})
INK='#000000'; TEAL='#168579'; WARM='#C7694B'; BLUE='#32658A'; GRAY='#8D999E'; LIGHT='#E9EFF0'
def clean(ax):
    ax.set_axisbelow(True); ax.grid(axis='x',color=LIGHT,lw=.6); ax.tick_params(length=2.5,pad=3)
def save(fig, name, task):
    from matplotlib.text import Text
    for artist in fig.findobj(match=Text):
        artist.set_color('#000000')
    fig.savefig(ROOT/'figs'/f'{name}.pdf',facecolor='white')
    fig.savefig(ROOT/'figs'/f'{name}.svg',facecolor='white')
    fig.savefig(ROOT/'ccfa-workfiles/figures'/task/'build/preview.png',dpi=240,facecolor='white')
    plt.close(fig)
