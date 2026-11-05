"""Export the canonical draw.io document; preserve all manual edits to it.
Requires the drawio desktop CLI and PyMuPDF. Exports native vector SVG/PDF,
plus a PNG preview. The PDF contains no raster-image objects.
"""
from pathlib import Path
import subprocess
import pymupdf as f
ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'figs/fig1_teaser_overview.drawio'
BUILD=ROOT/'ccfa-workfiles/figures/method-overview/build'
BUILD.mkdir(parents=True,exist_ok=True)
base=['drawio','--export','--theme','light','--timeout','60']
subprocess.run(base+['--format','svg','--embed-diagram','--embed-svg-fonts','false','--output',str(BUILD/'preview.svg'),str(SOURCE)],check=True)
raw=BUILD/'vector-export.pdf'
subprocess.run(base+['--format','pdf','--crop','--output',str(raw),str(SOURCE)],check=True)
src=f.open(raw)
assert len(src)==1 and not src[0].get_images(), 'Expected a single fully vector page.'
out=f.open();page=out.new_page(width=495,height=495*src[0].rect.height/src[0].rect.width)
page.show_pdf_page(page.rect,src,0)
out.save(ROOT/'figs/fig1_teaser_overview.pdf',garbage=4,deflate=True)
page.get_pixmap(matrix=f.Matrix(4,4),alpha=False).save(BUILD/'preview.png')
raw.unlink()
print('Exported vector PDF/SVG and PNG preview from',SOURCE)
