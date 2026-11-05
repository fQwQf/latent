"""Exact interpolation points and 95% cluster-bootstrap CIs:
sec/X_suppl.tex tab:s10_e6_interp; native full-set unmasked L=4 / L=8
from tab E3-B2. No interpolated/synthetic measurements are introduced.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'source'))
from style import *
x=np.array([0,.2,.4,.6,.8,1,1.5,2])
full=[[0,.36,.89,1.67,2.61,3.58,5.62,6.75],[0,.34,.83,1.42,2.11,2.76,4.05,4.76]]
win=[[0,.36,.89,1.67,2.60,3.58,5.62,6.73],[0,.34,.82,1.41,2.09,2.75,4.01,4.72]]
lo=[[0,.27,.68,1.24,1.93,2.68,4.31,5.22],[0,.29,.70,1.21,1.79,2.34,3.45,4.03]]
hi=[[0,.46,1.12,2.10,3.27,4.5,7.01,8.3],[0,.4,.95,1.64,2.45,3.2,4.71,5.48]]
wlo=[[0,.28,.68,1.25,1.97,2.69,4.24,5.19],[0,.29,.69,1.19,1.77,2.31,3.38,3.98]]
whi=[[0,.45,1.11,2.12,3.28,4.48,7,8.24],[0,.4,.94,1.62,2.43,3.21,4.66,5.47]]
proto=[[0,.01,.01,.01,.02,.01,.02,.03],[0,0,0,0,.01,.01,.01,.01]]
nat=[[0,-.006,-.021,-.045,-.056,-.068,-.088,-.094],[0,.004,-.003,-.008,-.01,-.015,-.026,-.026]]
fig,axs=plt.subplots(1,2,figsize=(6.875, 1.65),sharey=True)
fig.subplots_adjust(left=.075,right=.985,bottom=.22,top=.78,wspace=.18)
for k,ax in enumerate(axs):
 clean(ax);ax.grid(axis='y',color=LIGHT,lw=.6);ax.axhline(0,color=GRAY,lw=.6);ax.axvline(1,color=GRAY,lw=.7,ls=':')
 ax.fill_between(x,lo[k],hi[k],color=TEAL,alpha=.13,lw=0)
 ax.plot(x,full[k],color=TEAL,marker='o',ms=3.8,lw=1.5,label='E6-A: full tape')
 ax.plot(x,win[k],color=BLUE,marker='s',ms=2.8,lw=1.3,ls='--',mfc='white',label='E6-A: matched 2 slots')
 ax.plot(x,proto[k],color=GRAY,marker='^',ms=2.8,lw=1,label='E6-B: shared prototype')
 ax.plot(x,nat[k],color=WARM,marker='v',ms=2.8,lw=1,label='Native: unmasked')
 ax.errorbar([1],[win[k][5]],yerr=[[win[k][5]-wlo[k][5]],[whi[k][5]-win[k][5]]],color=BLUE,capsize=3,lw=.8,zorder=0)
 ax.set_title(f'({"ab"[k]}) K = {2 if k==0 else 4} · {4 if k==0 else 8} slots',loc='left',weight='bold',pad=5)
 ax.set_ylim(-.4,8.7);ax.set_xlim(-.06,2.08);ax.set_xticks([0,.5,1,1.5,2]);ax.set_yticks([0,2,4,6,8]);ax.set_xlabel(r'Interpolation coefficient $\alpha$')
 ax.annotate(f'α = 1: +{full[k][5]:.2f} full\n         +{win[k][5]:.2f} window',xy=(1,full[k][5]),xytext=(1.14,1.3),fontsize=8,arrowprops={'arrowstyle':'-','lw':.7,'color':INK})
axs[0].set_ylabel(r'Log-odds shift $\delta M(\alpha)$')
fig.legend(*axs[0].get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.52,1.02),ncol=4,frameon=False,columnspacing=1.5,handlelength=2.2)
save(fig,'fig4_e6_logit_interpolation','logit-interpolation')
