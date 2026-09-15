"""Generate the hero SVG: simplified world map with routes converging on Johannesburg."""
LAND = {
 "na": [(-168,66),(-158,71),(-135,70),(-118,73),(-100,74),(-86,70),(-78,64),(-64,60),(-56,52),(-66,45),(-70,42),(-75,36),(-80,31),(-81,25),(-84,30),(-90,29),(-97,27),(-97,21),(-90,17),(-84,11),(-79,8),(-83,9),(-88,14),(-94,17),(-105,21),(-110,25),(-115,31),(-121,35),(-124,42),(-124,48),(-132,55),(-142,60),(-152,60),(-163,58),(-166,62)],
 "sa": [(-79,8),(-72,12),(-62,11),(-52,5),(-50,0),(-45,-2),(-35,-6),(-38,-13),(-40,-20),(-48,-26),(-53,-33),(-58,-38),(-63,-41),(-65,-46),(-68,-52),(-70,-55),(-74,-50),(-75,-42),(-72,-33),(-70,-20),(-76,-14),(-80,-6),(-80,0),(-78,4)],
 "eu": [(-9,43),(-9,37),(-6,36),(0,38),(3,42),(8,44),(12,44),(16,40),(18,40),(19,42),(23,37),(26,40),(28,41),(30,45),(35,45),(40,47),(48,42),(50,46),(45,52),(40,60),(35,65),(30,70),(25,71),(18,69),(12,65),(5,62),(5,58),(10,57),(12,55),(8,54),(4,52),(0,50),(-2,48),(-5,48),(-2,44)],
 "uk": [(-5,50),(1,51),(2,53),(-1,56),(-2,58),(-5,58),(-6,55),(-3,54),(-5,52)],
 "af": [(-17,15),(-17,21),(-13,27),(-9,32),(-6,35),(0,36),(10,37),(11,34),(20,32),(25,32),(32,31),(35,28),(38,22),(43,12),(51,11),(48,4),(42,-2),(40,-10),(35,-20),(33,-26),(32,-29),(28,-33),(20,-35),(17,-30),(12,-18),(12,-5),(9,1),(9,4),(4,6),(-2,5),(-8,4),(-13,8),(-17,12)],
 "mg": [(44,-25),(49,-13),(50,-16),(48,-25)],
 "as": [(28,41),(35,37),(35,32),(40,30),(48,30),(56,25),(59,23),(62,25),(66,25),(68,23),(72,20),(73,14),(77,8),(80,13),(80,16),(87,22),(91,22),(95,16),(98,10),(103,2),(104,10),(109,12),(107,20),(112,22),(118,25),(121,30),(122,36),(118,39),(122,40),(127,38),(130,42),(135,44),(140,52),(142,60),(150,60),(158,55),(162,60),(180,66),(180,71),(160,70),(140,73),(120,73),(100,77),(75,72),(65,70),(55,68),(45,66),(40,60),(45,52),(50,46),(48,42),(40,47),(35,45),(30,45)],
 "jp": [(130,31),(134,34),(140,36),(141,40),(142,44),(145,44),(141,41),(137,37),(133,33)],
 "au": [(114,-22),(117,-35),(125,-33),(132,-32),(138,-35),(140,-38),(147,-39),(150,-37),(153,-28),(150,-22),(146,-15),(142,-11),(136,-12),(131,-12),(126,-14),(122,-18)],
 "gl": [(-45,60),(-42,64),(-30,68),(-20,72),(-20,78),(-35,82),(-60,82),(-70,78),(-60,72),(-55,66)],
 "id": [(95,5),(100,0),(106,-6),(114,-8),(120,-9),(118,-2),(112,-4),(105,-5),(103,0)],
}

LON0, LAT0, S = -128, 74, 2.1   # crop: lon -128..148, lat -44..74 → ~580 x 248
def P(lon, lat): return (round((lon-LON0)*S,1), round((LAT0-lat)*S,1))

ORIGINS = [("United States", -98, 39, "start"), ("Europe", 10, 50, "middle"), ("India", 78, 22, "middle"), ("China", 105, 35, "middle")]
TARGET = ("South Africa", 28, -26)

def arc(a, b, lift, gap=24):
    (x1,y1),(x2,y2) = a,b
    cx, cy = (x1+x2)/2, min(y1,y2) - lift
    # trim the end: back off along the tangent from control point to target
    dx, dy = x2-cx, y2-cy; L=(dx*dx+dy*dy)**.5
    ex, ey = x2-dx/L*gap, y2-dy/L*gap
    return f"M{x1} {y1} Q{cx:.0f} {cy:.0f} {ex:.1f} {ey:.1f}"

def build():
    out = ['<svg class="route" viewBox="0 0 580 250" role="img" aria-label="Routes from the United States, Europe, India and China converging on South Africa">']
    out.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#8fd0cc"/></marker></defs>')
    out.append('<g fill="rgba(255,255,255,.13)" stroke="rgba(255,255,255,.22)" stroke-width=".8" stroke-linejoin="round">')
    for k, pts in LAND.items():
        out.append('<path d="M' + " L".join(f"{x} {y}" for x,y in map(lambda p: P(*p), pts)) + ' Z"/>')
    out.append('</g>')
    tx, ty = P(TARGET[1], TARGET[2])
    out.append('<g fill="none" stroke="#8fd0cc" stroke-width="2" stroke-dasharray="5 6" stroke-linecap="round" marker-end="url(#ah)">')
    lifts = {"United States": 90, "Europe": 40, "India": 45, "China": 70}
    for name, lon, lat, _ in ORIGINS:
        out.append(f'<path d="{arc(P(lon,lat),(tx,ty),lifts[name])}"/>')
    out.append('</g>')
    for name, lon, lat, anchor in ORIGINS:
        x, y = P(lon, lat)
        out.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff"/><circle cx="{x}" cy="{y}" r="10" fill="#fff" opacity=".18"/>')
        dx = 0 if anchor=="middle" else -6
        ly = y+22 if name=="United States" else y-13
        out.append(f'<text x="{x+dx}" y="{ly}" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="#dfe6ee" text-anchor="{anchor}">{name}</text>')
    out.append(f'<circle cx="{tx}" cy="{ty}" r="7" fill="#8fd0cc"/><circle cx="{tx}" cy="{ty}" r="15" fill="#8fd0cc" opacity=".22"/>')
    out.append(f'<text x="{tx}" y="{ty+26}" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">{TARGET[0]}</text>')
    out.append('</svg>')
    return "\n        ".join(out)

if __name__ == "__main__":
    import re, pathlib
    p = pathlib.Path(__file__).parent / "pages" / "index.html"
    h = p.read_text()
    h = re.sub(r'<svg class="route".*?</svg>', build(), h, flags=re.S)
    p.write_text(h)
    print("map injected")
