"""Render a rotating feasible-score cube and deterministic offline archive."""

import math
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path(os.environ.get("Q572_FONT_DIR", "/System/Library/Fonts/Supplemental"))
BG, PANEL, TEXT, MUTED, GRID = "#15172d", "#20263f", "#f5f7ff", "#bdc9e6", "#4f6083"
OLD, NEW, MARK = "#b8b4ff", "#60ecc1", "#ffc281"
CUBE = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
EDGES = [(a,b) for i,a in enumerate(CUBE) for b in CUBE[i+1:]
         if sum(abs(x-y) for x,y in zip(a,b)) == 1]
STAGES = [
    ("Original labels", "Last label mean = 3/4", "Distance = 0"),
    ("Only the last labels change", "Last label mean = 7/8", "The old prediction stays fixed."),
    ("Repair on the boundary", "Nearest scores = (5/8, 3/8, 1)", "Distance = 1/12"),
]


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ("Arial Bold.ttf" if bold else "Arial.ttf")), size)


def scores(s, t):
    return .5+s/4, .5-s/4, .75+(t+s)/4


def project(point, angle):
    x,y,z = (2*q-1 for q in point)
    u,v = math.cos(angle), math.sin(angle)
    return round(355+144*(u*x-v*y)), round(347+70*(v*x+u*y)-98*z)


def render_frame(stage, angle):
    image = Image.new("RGB", (704,835), BG)
    d = ImageDraw.Draw(image)
    d.text((34,30), "Distance to multiaccuracy", font=font(47,True), fill=TEXT)
    d.text((36,94), "Two overlapping groups, three points", font=font(32), fill=MUTED)
    d.rounded_rectangle((30,151,674,583), radius=25, fill=PANEL)
    for first, second in EDGES:
        d.line((project(first,angle),project(second,angle)),fill=GRID,width=3)
    for point,name,delta in (
        ((1,0,0),"g1",(17,-17)), ((0,1,0),"g2",(-47,0)), ((0,0,1),"g3",(-48,-10))
    ):
        x,y = project(point,angle)
        d.text((x+delta[0],y+delta[1]),name,font=font(30,True),fill=MUTED)

    prediction = project(scores(1,0),angle)
    d.line((project(scores(-2,0),angle),prediction), fill=OLD,width=8)
    if stage:
        repair = project(scores(.5,.5),angle)
        d.line((project(scores(-2,.5),angle),repair), fill=NEW,width=8)
        if stage == 2:
            d.line((prediction,repair),fill=MARK,width=4)
        x,y = repair
        d.ellipse((x-10,y-10,x+10,y+10),fill=NEW,outline=BG,width=3)
    x,y = prediction
    d.polygon(((x,y-14),(x+14,y),(x,y+14),(x-14,y)),fill=MARK,outline=BG,width=2)
    legend = [(OLD,"Original feasible"),(MARK,"Fixed f")]
    if stage:
        legend = [(OLD,"Before"),(NEW,"After"),(MARK,"Fixed f")]
    at = 46
    for color, label in legend:
        d.rounded_rectangle((at,543,at+21,564),radius=4,fill=color)
        d.text((at+32,539),label,font=font(27,True),fill=TEXT)
        at += 125 + round(d.textlength(label,font=font(27,True)))
    title, first, second = STAGES[stage]
    d.text((34,606),title,font=font(44,True),fill=TEXT)
    d.line(((35,671),(670,671)),fill=GRID,width=2)
    d.text((36,693),first,font=font(33),fill=TEXT)
    d.text((36,745),second,font=font(35,True),fill=TEXT)
    return image.quantize(colors=48,method=Image.Quantize.MEDIANCUT)


def main():
    frames, delays = [], []
    for stage in range(3):
        for i in range(20):
            angle = .43 + .20 * math.sin(math.tau*i/20)
            frames.append(render_frame(stage,angle))
            delays.append(300 if i==0 else 160)
    frames[0].save(HERE/"score-repair.gif",save_all=True,append_images=frames[1:],
                   duration=delays,disposal=1,loop=0,optimize=True)
    item = ZipInfo("index.html",(1980,1,1,0,0,0))
    item.create_system = 3
    item.external_attr = 0o100644 << 16
    with ZipFile(HERE/"score-repair-explorer.zip","w") as z:
        z.writestr(item,(HERE/"index.html").read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__ == "__main__":
    main()
