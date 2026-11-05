"""Exact values from sec/5_experiments.tex, tab:e6c and tab:e6_acc.
Dot matrix: position-eligible K=2, position-eligible K=4, full K=4.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'source'))
from style import *
from matplotlib.colors import LinearSegmentedColormap
fig=plt.figure(figsize=(3.28,3.65))
fig.text(.02,.973,'(a) Cache swaps: target flip rate (%)',weight='bold',size=10)
ax=fig.add_axes([.27,.57,.69,.28]);clean(ax)
series=[[0,0,100,100],[0,0,96.88,96.88],[0,0,40.23,39.19]]
for vals,offset,color,mark in zip(series,[.18,0,-.18],[BLUE,WARM,GRAY],['o','s','^']):
 ax.scatter(vals,np.arange(4)[::-1]+offset,c=color,marker=mark,s=18,zorder=3)
ax.set_yticks(range(4),['C3b: all text KV','C3a: prompt KV','C2: latent KV','C1: slot inputs']);ax.set_xlim(-4,109);ax.set_ylim(-.5,3.5);ax.set_xticks([0,50,100]);ax.spines['left'].set_visible(False)
from matplotlib.lines import Line2D
for xx, yy, label, color, marker in [(.28,.898,'K=2 eligible',BLUE,'o'),(.65,.898,'K=4 eligible',WARM,'s'),(.28,.862,'K=4 full set',GRAY,'^')]:
 fig.add_artist(Line2D([xx+.012],[yy+.008],transform=fig.transFigure,marker=marker,ms=3.5,color=color,linestyle='none'))
 fig.text(xx+.038,yy,label,size=8,color=INK)
fig.text(.02,.47,'(b) Strict Phase-B chain accuracy (%)',weight='bold',size=10)
D=np.array([[2.33,1.33,0,0],[9.67,9.67,3.33,4.67],[18.33,15,6.33,6.67],[82,83.33,72.67,75.67]])
ax=fig.add_axes([.27,.12,.69,.26]);cmap=LinearSegmentedColormap.from_list('teal',['#F3F6F6','#B8D9D1',TEAL]);ax.imshow(D,vmin=0,vmax=100,cmap=cmap,aspect='auto')
ax.set_yticks(range(4),['Native†','E5†','E6-B','E6-A']);ax.set_xticks(range(4),['K=2\nSer.','K=2\nInd.','K=4\nSer.','K=4\nInd.']);ax.xaxis.tick_top();ax.tick_params(length=0,pad=3)
for i in range(4):
 for j in range(4):ax.text(j,i,f'{D[i,j]:.1f}',va='center',ha='center',size=9,color=INK,weight='bold' if i==3 else 'normal')
ax.axhline(2.5,color='white',lw=3);ax.axvline(1.5,color='white',lw=3)
for s in ax.spines.values():s.set_visible(False)
fig.text(.27,.055,'† Untrained on the Phase-B interface.',size=8,color=GRAY)
save(fig,'fig3_e6c_double_dissociation','cache-dissociation')
