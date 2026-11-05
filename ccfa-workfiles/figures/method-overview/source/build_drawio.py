"""Native draw.io mechanism figure: cached routes, all-layer swaps, isolated readout.
Authoritative output: figs/fig1_teaser_overview.drawio. Export it with
export_drawio.py to preserve manual edits. This constructor resets its geometry.
3D is restricted to exploded KV-layer sheets and across-layer selection frames.
Computation operators and slot windows are flat. All editable text is black.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import math, zlib, base64
from urllib.parse import quote
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[4]
W,H=1800,1155
mx=E.Element('mxfile',host='Electron',version='31.5.2')
d=E.SubElement(mx,'diagram',id='causal-routing',name='Cached routes, across-layer swaps, and isolated readout')
m=E.SubElement(d,'mxGraphModel',dx=str(W),dy=str(H),grid='1',gridSize='10',guides='1',tooltips='1',connect='1',arrows='1',page='1',pageScale='1',pageWidth=str(W),pageHeight=str(H),background='#FFFFFF',shadow='0')
r=E.SubElement(m,'root');E.SubElement(r,'mxCell',id='0');E.SubElement(r,'mxCell',id='1',parent='0')
BLACK='#000000';TEAL='#277C83';BLUE='#3B6687';CORAL='#DD866E';GRAY='#A7ABB1'
def cell(id,value,style,x,y,w,h,parent='1'):
 c=E.SubElement(r,'mxCell',id=id,value=value,style=style,vertex='1',parent=parent)
 E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
 return id
def group(id,x,y,w,h,parent='1'):
 return cell(id,'','group;connectable=1;recursiveResize=1;',x,y,w,h,parent)
def text(id,value,x,y,w,h,size=31,bold=False,align='center',parent='1'):
 return cell(id,value,f'text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;fontColor=#000000;fontFamily=Liberation Sans;fontSize={size};fontStyle={int(bold)};align={align};verticalAlign=middle;spacing=0;overflow=visible;',x,y,w,h,parent)
@lru_cache(None)
def rounded_stencil(w,h,skew,radius):
 # Rounded quadrilateral via exact quadratic Bezier tangencies, unlike the
 # stock parallelogram's clipped corner treatment. Native editable stencil.
 poly=[(skew,0),(w,0),(w-skew,h),(0,h)]
 tangent=[]
 for i,(x,y) in enumerate(poly):
  prev=poly[(i-1)%4];nxt=poly[(i+1)%4]
  def towards(p):
   dx,dy=p[0]-x,p[1]-y;length=math.hypot(dx,dy);dist=min(radius,length*.42)
   return (x+dx/length*dist,y+dy/length*dist)
  tangent.append((towards(prev),towards(nxt)))
 s=E.Element('shape',name='Rounded shallow plane',w=str(w),h=str(h),aspect='variable',strokewidth='inherit')
 bg=E.SubElement(s,'background');path=E.SubElement(bg,'path')
 def ptag(tag,**kwargs):E.SubElement(path,tag,{k:f'{v:.4f}' for k,v in kwargs.items()})
 ptag('move',x=tangent[0][0][0],y=tangent[0][0][1])
 for i in range(4):
  if i:ptag('line',x=tangent[i][0][0],y=tangent[i][0][1])
  ptag('quad',x1=poly[i][0],y1=poly[i][1],x2=tangent[i][1][0],y2=tangent[i][1][1])
 E.SubElement(path,'close');fg=E.SubElement(s,'foreground');E.SubElement(fg,'fillstroke')
 xml=E.tostring(s,encoding='unicode');comp=zlib.compressobj(level=9,wbits=-15)
 data=comp.compress(quote(xml,safe="~()*!.'-").encode())+comp.flush()
 return base64.b64encode(data).decode()
def plane(id,x,y,w,h,skew,rad,fill,gradient=None,opacity=100,stroke='none',sw=.7,parent='1'):
 st=f'shape=stencil({rounded_stencil(w,h,skew,rad)});fillColor={fill};strokeColor={stroke};strokeWidth={sw};opacity={opacity};connectable=0;'
 if gradient:st+=f'gradientColor={gradient};gradientDirection=south;'
 return cell(id,'',st,x,y,w,h,parent)
def edge(id,src,tgt,color=BLUE,points=None,source=None,target=None,exit=None,entry=None,arrow=True,dashed=False,width=3,parent='1'):
 st=f'edgeStyle=none;rounded=1;arcSize=15;html=1;fontColor=#000000;strokeColor={color};strokeWidth={width};endArrow={"block" if arrow else "none"};endFill=1;endSize=8;'
 if dashed:st+='dashed=1;dashPattern=4 4;'
 if exit:st+=f'exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;exitPerimeter=0;'
 if entry:st+=f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;entryPerimeter=0;'
 attrs=dict(id=id,value='',style=st,edge='1',parent=parent)
 if source:attrs['source']=source
 if target:attrs['target']=target
 c=E.SubElement(r,'mxCell',attrs);g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
 if src:E.SubElement(g,'mxPoint',x=str(src[0]),y=str(src[1]),attrib={'as':'sourcePoint'})
 if tgt:E.SubElement(g,'mxPoint',x=str(tgt[0]),y=str(tgt[1]),attrib={'as':'targetPoint'})
 if points:
  a=E.SubElement(g,'Array',attrib={'as':'points'})
  for x,y in points:E.SubElement(a,'mxPoint',x=str(x),y=str(y))
 return id
def cross(id,x,y,s=20):
 edge(id+'-a',(x-s,y-s),(x+s,y+s),CORAL,arrow=False,width=4)
 edge(id+'-b',(x-s,y+s),(x+s,y-s),CORAL,arrow=False,width=4)

def box(id,x,y,w,h,fill='#F6F8F9',stroke='#B7C4CA',radius=10,parent='1'):
 return cell(id,'',f'rounded=1;arcSize={radius};fillColor={fill};strokeColor={stroke};strokeWidth=1.6;',x,y,w,h,parent)

def scope_frame(id,x,y,w,face_h,depth,height,color):
 # A selection column intersects the same cache partition at every layer.
 a=(x,y+face_h);b=(x+w,y+face_h);c=(x+w+depth,y);d=(x+depth,y)
 aa=(a[0],a[1]+height);bb=(b[0],b[1]+height);cc=(c[0],c[1]+height)
 for i,(u,v) in enumerate([(a,b),(b,c),(c,d),(d,a),(a,aa),(b,bb),(c,cc),(aa,bb),(bb,cc)]):
  edge(f'{id}-{i}',u,v,color,arrow=False,dashed=True,width=2.2)

cell('canvas','','fillColor=#FFFFFF;strokeColor=none;locked=1;connectable=0;',0,0,W,H)
text('panel-a','(a) Decode masking leaves cached routes',24,16,850,48,size=34,bold=True,align='left')
text('panel-b','(b) Test the full cache depth (E6-C)',930,16,850,48,size=34,bold=True,align='left')
edge('top-panel-divider',(898,82),(898,582),'#D3DADD',arrow=False,width=1.3)

# (a) A flat information-flow diagram. Both nonvisual cache partitions are
# explicitly image-conditioned; a zero flip rate cannot remove either edge.
text('image-input-label','Image V<sub>T</sub>',35,203,180,42,size=31)
group('image-token-grid',55,252,132,104)
for row in range(3):
 for col in range(3):
  box(f'visual-token-{row}-{col}',col*45,row*35,40,30,'#D7EAE5','#A2C6BC',radius=8,parent='image-token-grid')
edge('visual-information-hub',(188,302),(247,302),TEAL,arrow=False,width=3)
edge('direct-visual-read',(215,302),(777,274),GRAY,[(215,111),(777,111)],width=2.7)
text('decode-mask-label','Direct visual read: masked',340,65,405,38,size=29)
cross('decode-mask',748,111,14)
box('prompt-cache-node',355,165,260,104,'#FFF1E9','#DBAA96',radius=0)
text('prompt-cache-node-label','Prompt / markers',366,174,238,38,size=30)
text('prompt-cache-node-symbol','KV<sub>Q,M</sub>',366,218,238,36,size=31)
box('latent-cache-node',355,360,260,104,'#EEF4F9','#9DB6CA',radius=0)
text('latent-cache-node-label','Latent positions',366,369,238,38,size=30)
text('latent-cache-node-symbol','KV<sub>H</sub>',366,413,238,36,size=31)
edge('image-conditions-prompt',(247,302),(347,217),CORAL,[(260,302),(260,217)],width=3)
edge('image-conditions-latent',(247,302),(347,412),BLUE,[(260,302),(260,412)],width=3)
box('masked-readout',710,282,155,106,'#F6F8F9','#B8C4CA')
text('masked-readout-label','Readout',717,292,141,38,size=30)
text('masked-readout-setting','m<sub>vis</sub> = 0',714,338,147,36,size=29)
edge('prompt-read-route',(615,217),(702,313),CORAL,[(661,217),(661,313)],width=3.3)
text('relay-label','relay',625,171,78,34,size=27)
edge('latent-read-route',(615,412),(702,353),BLUE,[(661,412),(661,353)],width=3)
text('cache-conditioning-takeaway','Both caches can contain visual information.<br>Swaps test their effect on the answer.',48,502,800,76,size=29)

# (b) The only 3D construction: exploded layer sheets with aligned partitions.
# Layers 1, 2, and 28 are shown, and the omitted layers are explicit. A wireframe
# column means a swap through all layers, not a new tensor or simultaneous arms.
text('prompt-partition-label','Prompt / markers',1003,116,360,40,size=31)
text('latent-partition-label','Latent positions',1354,116,365,40,size=31)
text('cache-layout-note','Swap donor KV across all layers',1047,166,650,36,size=28)
for layer,yy in [(1,415),(2,350),(28,230)]:
 group(f'cache-layer-{layer}',1010,yy,720,72)
 plane(f'cache-layer-{layer}-edge',0,5,720,64,44,7,'#D1DADF','#E3E9EC',parent=f'cache-layer-{layer}')
 plane(f'cache-layer-{layer}-sheet',0,0,720,64,44,7,'#F8FAFB','#EDF2F4',stroke='#D3DCE0',sw=.8,parent=f'cache-layer-{layer}')
 plane(f'cache-layer-{layer}-prompt',15,4,330,56,40,5,'#FFE6D7','#EFBBA2',stroke='#FFFFFF',sw=.8,parent=f'cache-layer-{layer}')
 plane(f'cache-layer-{layer}-latent',360,4,330,56,40,5,'#DFEAF3','#B7CCDD',stroke='#FFFFFF',sw=.8,parent=f'cache-layer-{layer}')
text('prompt-partition-symbol','KV<sub>Q,M</sub>',1105,241,180,38,size=31)
text('latent-partition-symbol','KV<sub>H</sub>',1450,241,180,38,size=31)
scope_frame('all-layer-prompt-scope',1019,225,302,69,40,190,CORAL)
scope_frame('all-layer-latent-scope',1364,225,302,69,40,190,BLUE)
edge('layer-axis',(982,486),(982,275),'#88969F',width=1.5)
text('layer-axis-label','Layer ℓ',919,214,94,42,size=28)
for val,yy in [('28',294),('2',414),('1',479)]:
 edge('layer-tick-'+val,(976,yy),(990,yy),'#88969F',arrow=False,width=1.5)
 text('layer-label-'+val,val,928,yy-18,42,36,size=29)
text('layer-ellipsis','⋮',936,331,30,45,size=34)
# An ellipsis inside each selected column connects the omitted layer range.
text('prompt-layer-ellipsis','⋮',1163,307,35,39,size=31)
text('latent-layer-ellipsis','⋮',1509,307,35,39,size=31)
text('prompt-swap-result','C3a/b: 96.88–100%',1005,514,365,42,size=31,bold=True)
text('latent-swap-result','C2: 0.00%',1370,514,345,42,size=31,bold=True)
text('swap-result-unit','Eligible flips · separate donor swaps',1003,562,710,36,size=28)

edge('main-divider',(24,619),(1776,619),'#CFD7DC',arrow=False,width=1.4)
text('panel-c','(c) Transfer latent inputs into a fresh readout (E6-A)',24,641,1700,48,size=35,bold=True,align='left')
text('phase-a-label','Phase A',65,712,505,42,size=32,bold=True)
text('phase-b-label','Phase B',1430,712,290,42,size=32,bold=True)

# (c) Computations are flat operators, distinct from the layer-wise KV sheets.
# Both the no-grad rollout and parallel replay receive the image/prompt inputs.
text('phase-a-inputs','V<sub>T</sub>, Q, M<sub>start</sub>',70,768,500,38,size=31)
edge('phase-a-input-bus',(320,810),(160,842),TEAL,[(320,825),(160,825)],width=2.5)
edge('phase-a-replay-input',(320,825),(453,842),TEAL,[(453,825)],width=2.5)
box('raw-rollout',60,850,200,104,'#F5F8F7','#AEC8C0')
text('raw-rollout-label','AR rollout',67,860,186,39,size=31)
text('raw-rollout-gradient','no grad',67,908,186,34,size=28)
box('parallel-replay',335,850,235,104,'#F5F8F7','#AEC8C0')
text('parallel-replay-label','Parallel<br>replay',348,867,209,68,size=32)
edge('raw-to-replay',(260,902),(327,902),TEAL,width=2.8)
text('raw-tape-label','H<sub>raw</sub>',264,860,66,32,size=27)
edge('replay-emission',(570,902),(680,902),TEAL,width=3)
text('replay-emission-label','H<sub>diff</sub>',577,849,108,36,size=29)
edge('discard-a-cache',(453,960),(453,991),GRAY,arrow=False,width=2)
cross('discard-a-cache-cross',453,979,13)
text('discard-a-cache-label','Discard all Phase-A KV',125,1004,490,40,size=29)

# H is a flat sequence of exactly eight editable slots, in four labeled pairs.
# A two-slot evaluation window is aligned in the same coordinate system.
group('recipient-tape',700,871,408,65)
colors=[('#DCEFE9','#A3C9BC'),('#FBE2D6','#D6977C'),('#E1EBF4','#9BB6CB'),('#E5EEDB','#A4BB8D')]
for k,(fill,stroke) in enumerate(colors):
 for j in range(2):
  box(f'step-{k+1}-slot-{j+1}',k*108+j*45,0,39,65,fill,stroke,radius=5,parent='recipient-tape')
 center=700+k*108+42
 edge(f'window-{k+1}-bracket',(center-42,944),(center+42,944),BLACK,[(center-42,953),(center+42,953)],arrow=False,width=1.4)
 text(f'window-{k+1}-index',str(k+1),center-20,961,40,34,size=29)
text('window-step-label','Step',625,959,68,36,size=28)
cell('selected-two-slot-window','','rounded=1;arcSize=5;fillColor=none;strokeColor=#BB6E51;strokeWidth=2;dashed=1;dashPattern=4 4;',800,863,100,81)
text('donor-window-label','Eval: donor window m',697,712,440,42,size=29)
for j in range(2):
 xx=808+j*45
 box(f'donor-slot-{j+1}',xx,771,39,60,'#FBE2D6','#D6977C',radius=5)
 edge(f'donor-interpolation-{j+1}',(xx+19.5,839),(xx+19.5,862),CORAL,width=2.3)
text('interpolation-alpha','α',905,824,40,38,size=31)
text('tape-label','H<sub>diff</sub>: 2 slots per step (K = 4)',660,1010,540,40,size=30)
text('interpolation-formula','H<sub>m</sub>(α) = (1 − α)H<sub>m</sub> + αH′<sub>m</sub>',626,1064,620,42,size=30)
text('unchanged-window-note','Other windows stay fixed',690,1110,500,36,size=28)

# Only the latent input is carried across phases. New text/marker caches may
# depend on this input; the diagram does not assert their independence from H.
edge('fresh-cache-boundary',(1290,778),(1290,1127),GRAY,arrow=False,dashed=True,width=2)
text('fresh-cache-label','Fresh cache',1298,779,213,40,size=29)
edge('latent-only-transfer',(1118,902),(1422,902),TEAL,width=3)
text('latent-only-label','H only',1123,852,150,38,size=30)
box('fresh-text-readout',1430,850,290,104,'#F5F8F9','#AFC3CD')
text('fresh-text-readout-label','Text readout',1444,860,262,38,size=31)
text('fresh-text-recompute','recompute all layers',1444,907,262,34,size=27)
edge('question-markers-input',(1575,1008),(1575,962),BLUE,width=2.6)
text('question-markers-label','Q + markers',1410,1016,330,40,size=30)
edge('answer-output',(1720,902),(1750,902),BLUE,width=3)
text('answer-label','Y',1755,878,37,44,size=32)
text('training-note','Training: H<sub>diff</sub> is not detached<br>Answer-loss gradients reach replay',1315,1074,462,68,size=27)

E.indent(mx,space='  ')
path=ROOT/'figs/fig1_teaser_overview.drawio'
E.ElementTree(mx).write(path,encoding='utf-8',xml_declaration=True)
print(path)
