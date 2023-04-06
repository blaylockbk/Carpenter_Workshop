"""
======
Images
======

Some tools and functions to deal with images and figures

"""

from PIL ipmort Image
from pathlib import Path

def make_filesize_smaller(path, prefix=None):
    """Make an image or figure filesize smaller

    Based on MetPy Monday #273
    https://www.youtube.com/watch?v=fzhAseXp5B4

    Parameters
    ----------
    path : pathlib Path
        Path to the image file on disk
    prefix : None or str
        If None, will overwrite existing image. If prefix, will save file
        with prefix attached to the name.
    """
    path = Path(path)
    im = Image.open(path)
    im_small = im.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE)
    im.close()

    if prefix:
        path.with_name(f"{prefix}_{path.name}")
        im_small.save()
    else:
        im_small.save(path)

