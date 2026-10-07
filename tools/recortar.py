"""Recorta una figura de cómic (contorno oscuro) de su fondo de papel claro y la
guarda como PNG con transparencia (también vacía los huecos cerrados, como el de una R).

    pip install numpy scipy pillow
    python3 tools/recortar.py dibujo.jpg recorte.png

Después se puede pasar a WebP para la web, p. ej. con:
    python3 -c "from PIL import Image; Image.open('recorte.png').save('assets/x.webp', quality=86)"
"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi

def recortar(src, holes_min=300, tol=30, tight_tol=14, ring_dark=120, region=None, keep_largest=False):
    im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
    if region: im = im[region[1]:region[3], region[0]:region[2]]
    H, W, _ = im.shape
    border = np.concatenate([im[:6].reshape(-1,3), im[-6:].reshape(-1,3), im[:, :6].reshape(-1,3), im[:, -6:].reshape(-1,3)])
    bg = np.median(border, 0)
    d = np.sqrt(((im - bg) ** 2).sum(2))
    L = im.mean(2)
    cand = d < tol
    lab, n = ndi.label(cand)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])); edge = edge[edge > 0]
    outside = np.isin(lab, edge)
    holes = np.zeros_like(outside)
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        if sl is None or i in edge: continue
        sub = lab[sl] == i
        if sub.sum() < holes_min: continue
        dd = d[sl][sub]
        if (dd < tight_tol).mean() < 0.9 or dd.std() > 6: continue   # fondo liso, no una tela clara sombreada
        y0, x0 = max(0, sl[0].start - 5), max(0, sl[1].start - 5)
        s2 = lab[y0:sl[0].stop + 5, x0:sl[1].stop + 5] == i
        ring = ndi.binary_dilation(s2, iterations=4) & ~s2
        if L[y0:sl[0].stop + 5, x0:sl[1].stop + 5][ring].mean() < ring_dark:
            holes[y0:sl[0].stop + 5, x0:sl[1].stop + 5] |= s2
    fg = ~ndi.binary_opening(outside | holes, iterations=1)
    if keep_largest:
        lab2, n2 = ndi.label(fg)
        if n2 > 1:
            sizes = ndi.sum(fg, lab2, range(1, n2 + 1)); fg = lab2 == (np.argmax(sizes) + 1)
            fg = ndi.binary_fill_holes(fg) & ~holes
    # franja del borde: 2 px hacia fuera y solo 1 hacia dentro (los brillos junto al contorno no se pierden)
    band = ndi.binary_dilation(fg, iterations=2) & ~ndi.binary_erosion(fg, iterations=1)
    Lbg = bg.mean(); Ldark = 40.0
    alpha = fg.astype(np.float32)
    alpha[band] = np.clip((Lbg - L[band]) / (Lbg - Ldark) * 1.15, 0, 1)
    rgb = im.copy(); m = band & (alpha > 0.02)
    k = np.clip(alpha[m], 0.08, 1)[:, None]
    rgb[m] = np.clip((im[m] - bg * (1 - k)) / k, 0, 255)
    img = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), 'RGBA')
    return img, bg

if __name__ == '__main__':
    img, bg = recortar(sys.argv[1])
    img.save(sys.argv[2]); print(sys.argv[2], img.size, 'fondo', bg, 'bbox', img.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
