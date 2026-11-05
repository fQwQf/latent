"""Reference-faithful native draw.io construction (not a bitmap trace).
Authoritative output: figs/fig1_teaser_overview.drawio. Export it with
export_drawio.py to preserve manual edits. This constructor resets its geometry.
Custom rounded paths, thin sidewalls, highlights and layered vector shadows are
native stencil objects, grouped by scientific object; all live text is black.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import math, zlib, base64
from urllib.parse import quote
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[4]
W,H=1800,920
mx=E.Element('mxfile',host='Electron',version='31.5.2')
d=E.SubElement(mx,'diagram',id='causal-routing',name='Causal routing and strict isolation')
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
def shadow(id,x,y,w,h,skew,rad,parent):
 # Smooth-looking soft contact shadow using translucent vector paths, with no
 # SVG blur filter and therefore no rasterization on PDF export.
 for k in range(24,0,-1):
  spread=k*1.1
  plane(f'{id}-{k}',x-spread,y+5-spread*.35,w+2*spread,h+spread*.6,skew,rad+spread,'#8C9DA3',opacity=1,parent=parent)
def chip(id,x,y,w,h,skew,rad,top,bottom,side,parent='1',depth=5,shade=True):
 group(id,x,y,w,h+depth+4,parent)
 if shade:shadow(id+'-shadow',0,depth+3,w,h,skew,rad,id)
 plane(id+'-side',0,depth,w,h,skew,rad,side,bottom,parent=id)
 plane(id+'-face',0,0,w,h,skew,rad,top,bottom,stroke='#F6FFFC',sw=.35,parent=id)
 return id
def stack(id,x,y,w,face_h,skew,rad,colors,layers=3,step=18,label='',size=31):
 top,bottom,side=colors;total=face_h+(layers-1)*step+7
 group(id,x,y,w,total)
 shadow(id+'-ambient',0,(layers-1)*step+10,w,face_h,skew,rad,id)
 for k in reversed(range(layers)):
  yy=k*step
  # Narrow bottom face and a hairline highlight preserve the reference's
  # thin translucent layer appearance without dark outlines.
  plane(f'{id}-layer-{k}-edge',0,yy+5,w,face_h,skew,rad,side,bottom,parent=id)
  plane(f'{id}-layer-{k}',0,yy,w,face_h,skew,rad,top,bottom,stroke='#FAFFFD',sw=.4,parent=id)
 if label:text(id+'-label',label,skew*.35,face_h*.12,w-skew*.7,face_h*.76,size=size,parent=id)
 return id

def edge(id,src,tgt,color=BLUE,points=None,source=None,target=None,exit=None,entry=None,arrow=True,dashed=False,width=3):
 st=f'edgeStyle=none;rounded=1;arcSize=15;html=1;fontColor=#000000;strokeColor={color};strokeWidth={width};endArrow={"block" if arrow else "none"};endFill=1;endSize=8;'
 if dashed:st+='dashed=1;dashPattern=4 4;'
 if exit:st+=f'exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;exitPerimeter=0;'
 if entry:st+=f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;entryPerimeter=0;'
 attrs=dict(id=id,value='',style=st,edge='1',parent='1')
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
cell('canvas','','fillColor=#FFFFFF;strokeColor=none;locked=1;connectable=0;',0,0,W,H)
text('panel-a','(a) Single-pass: prefill relay',20,13,1040,48,size=36,bold=True,align='left')
# Reference proportions: left 4x4 chip plane; separate cache sheets, decoder.
group('visual-tokens',90,185,320,190)
for row in range(4):
 for col in range(4):
  chip(f'visual-{row}-{col}',66-22*row+62*col,row*37,60,28,10,10,'#C1ECE5','#9BDDD1','#72BFB2',parent='visual-tokens',depth=5)
text('visual-label','Visual tokens',-3,160,330,42,parent='visual-tokens')
stack('prompt-cache',724,177,466,60,50,20,('#FFEAE2','#F4CDC0','#E5AF9C'),label='Prompt / marker KV')
stack('latent-cache',676,310,462,60,50,20,('#E5EDF4','#BACEDC','#8DAABE'),label='Latent KV')
stack('answer-decoder',1335,195,414,132,60,23,('#ECF8F5','#CCEAE3','#95CFC4'),layers=2,step=12,label='Answer decoder',size=32)
# Explicit connected ports retain the graph when grouped modules are moved.
edge('direct-image-path',None,None,GRAY,[(303,116),(1542,116)],source='visual-tokens',target='answer-decoder',exit=(.666,0),entry=(.5,0))
text('decode-mask-label','Decode-time mask',744,60,430,43,size=31)
cross('decode-mask-cross',943,116,20)
edge('visual-to-relay',None,None,CORAL,source='visual-tokens',target='prompt-cache',exit=(1,.21),entry=(.035,.46))
text('relay-label','Prefill relay',470,170,250,40,size=31,bold=True)
edge('relay-to-answer',None,None,CORAL,source='prompt-cache',target='answer-decoder',exit=(.975,.46),entry=(.1,.197))
edge('visual-to-latent',None,None,BLUE,[(475,282),(475,348)],source='visual-tokens',target='latent-cache',exit=(1,.51),entry=(.04,.36))
edge('latent-to-answer',None,None,BLUE,source='latent-cache',target='answer-decoder',exit=(.975,.36),entry=(.025,.98))
edge('panel-divider',(20,445),(1780,445),'#D2D6DA',arrow=False,width=1.5)
text('panel-b','(b) Two-phase: isolated readout',20,463,1180,47,size=36,bold=True,align='left')
text('phase-a-label','Phase A',36,539,240,43,size=32,bold=True,align='left')
text('phase-b-label','Phase B',1282,539,230,43,size=32,bold=True,align='left')
text('image-question-label','Image + question',20,634,245,40,size=30,align='left')
stack('parallel-emission',272,605,300,83,30,17,('#E6F5F1','#C2E7DE','#94CBBD'),layers=2,step=10,label='Parallel replay',size=31)
edge('context-to-replay',(205,670),None,BLUE,target='parallel-emission',entry=(.01,.65))
text('phase-a-detail','After no-grad rollout',254,738,340,38,size=28)
# No extra oversized algorithm inset: full rollout/replay and gradient details
# remain in the figure caption; the tape identity is explicit in the graphic.
group('differentiable-tape',611,625,444,53)
colors=[('#C1ECE3','#99D6C8','#7DBAAB'),('#FFE3D6','#F4BBA5','#DB9F87'),('#DDEAF4','#B2CADF','#91AEC7'),('#E0EDD8','#BCD4AB','#9EBB88')]
for k,colorset in enumerate(colors):
 for j in range(2):
  chip(f'step-{k+1}-slot-{j+1}',k*111+j*50,0,48,31,10,9,*colorset,parent='differentiable-tape',depth=5)
 center=611+k*111+49
 edge(f'window-{k+1}-bracket',(center-46,675),(center+46,675),BLACK,[(center-46,684),(center+46,684)],arrow=False,width=1.5)
 text(f'step-{k+1}-index',str(k+1),center-20,690,40,34,size=29)
 cell(f'step-{k+1}-target','',f'rounded=1;arcSize=20;fillColor={colorset[1]};gradientColor={colorset[0]};gradientDirection=north;strokeColor=none;',center-17,799,34,34)
 edge(f'step-{k+1}-supervision',(center,791),(center,736),GRAY,dashed=True,width=2.2)
text('tape-label','H<sub>diff</sub>: 2 slots per step',606,558,453,46,size=31)
edge('emission-to-tape',None,None,BLUE,source='parallel-emission',target='differentiable-tape',exit=(.99,.43),entry=(0,.43))
edge('target-bracket',(611,849),(1043,849),'#788289',[(611,858),(1043,858)],arrow=False,width=1.4)
text('supervision-label','Step-wise ROI / color supervision (train)',559,868,545,38,size=28)
edge('isolation-boundary',(1078,537),(1078,873),GRAY,dashed=True,arrow=False,width=2)
text('fresh-cache-label','Fresh cache',1090,548,200,41,size=29,align='left')
stack('text-decoder',1293,605,309,83,30,17,('#E6F5F1','#C2E7DE','#94CBBD'),layers=2,step=10,label='Text decoder',size=31)
edge('tape-only-transfer',None,None,BLUE,source='differentiable-tape',target='text-decoder',exit=(1,.43),entry=(.005,.43))
text('no-detach-label','No detach',1098,607,178,34,size=28)
text('question-label','Question',1123,708,195,38,size=30)
edge('question-to-decoder',(1258,752),None,BLUE,[(1388,752)],target='text-decoder',entry=(.307,1))
text('answers-label','Answers',1669,636,130,40,size=31)
edge('decoder-to-answers',None,(1663,656),BLUE,source='text-decoder',exit=(.99,.51))
stack('excluded-a-cache',1111,786,148,27,17,7,('#F2F4F5','#DDE1E5','#BDC5CD'),layers=3,step=12)
cross('excluded-a-cache-cross',1182,815,22)
text('excluded-cache-label','No image /<br>Phase-A cache',1089,851,218,67,size=28)
E.indent(mx,space='  ')
path=ROOT/'figs/fig1_teaser_overview.drawio';E.ElementTree(mx).write(path,encoding='utf-8',xml_declaration=True)
print(path)
