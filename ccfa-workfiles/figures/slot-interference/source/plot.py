"""E3-C: exact values and paired CIs from sec/5_experiments.tex, tab:e3c.
All eight arms shown. Paired contrasts are reported CIs, not differences of CIs.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'source'))
from style import *
from matplotlib.colors import LinearSegmentedColormap
D=np.array([[76,73.67,30.67,35],[76.33,73.33,31.33,34.33],[64,63,18,21],[56.33,57,19,24.33],[77,73.33,32.67,36.33],[76.33,72.33,33.33,36.33],[64.33,62.67,19,21],[56.33,57,19.67,25.33]])
rows=['NoLatent','Marker-only','Native, L = 4','Native, L = 8','Zero-Slot, L = 4','Zero-Slot, L = 8','Zero-Marker, L = 4','Zero-Marker, L = 8']
fig=plt.figure(figsize=(3.28,4.05))
fig.text(.02,.974,'(a) Eight-arm chain accuracy (%)',weight='bold',size=10)
ax=fig.add_axes([.36,.49,.62,.40]); cmap=LinearSegmentedColormap.from_list('teal',['#F3F6F6','#B8D9D1',TEAL])
ax.imshow(D,vmin=0,vmax=100,cmap=cmap,aspect='auto')
ax.set_xticks(range(4),['K=2\nInd.','K=2\nSer.','K=4\nInd.','K=4\nSer.']); ax.xaxis.tick_top(); ax.tick_params(length=0,pad=4)
ax.set_yticks(range(8),rows)
for i in range(8):
 for j in range(4): ax.text(j,i,f'{D[i,j]:.1f}',ha='center',va='center',size=8,color=INK,weight='bold' if i in [4,5] else 'normal')
for y in [.5,1.5,3.5,5.5]: ax.axhline(y,color='white',lw=2)
ax.axvline(1.5,color='white',lw=3)
for s in ax.spines.values():s.set_visible(False)
fig.text(.02,.433,'(b) Paired effects with 95% CIs (pp)',weight='bold',size=10)
ax=fig.add_axes([.31,.15,.65,.235]); clean(ax)
xs=np.array([.33,-.33,.67,-.67]); lo=np.array([0,-2,-.67,-2]); hi=np.array([1,1.33,2,.67])
z=np.array([13,10.33,14.67,15.33]); zl=np.array([6.67,4,8.67,10]); zh=np.array([19.33,16.67,20.67,20.67]); ys=np.arange(4)[::-1]
ax.errorbar(xs,ys+.12,xerr=[xs-lo,hi-xs],fmt='s',ms=3.5,lw=1,color=GRAY,capsize=2,label='Marker-only − NoLatent')
ax.errorbar(z,ys-.12,xerr=[z-zl,zh-z],fmt='o',ms=4,lw=1.3,color=TEAL,capsize=2,label='Zero-Slot − Native (L=4)')
ax.axvline(0,lw=.8,color=INK,ls=':');ax.set_yticks(ys,['K=2 Ind.','K=2 Ser.','K=4 Ind.','K=4 Ser.']);ax.set_xlim(-3,24);ax.set_ylim(-.5,3.5);ax.set_xticks([0,10,20]);ax.spines['left'].set_visible(False)
ax.legend(loc='upper center',bbox_to_anchor=(.40,-.29),frameon=False,ncol=1,handlelength=1.4,labelspacing=.2,borderpad=0)
save(fig,'fig2_e3c_slot_interference','slot-interference')
