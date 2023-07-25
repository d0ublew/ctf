#!/usr/bin/env python3

# type: ignore

import exiftool
from PIL import Image

image = Image.new("RGBA", (690, 420), (255, 255, 255, 0))

image.putpixel((412, 309), (52, 146, 235, 123))
image.putpixel((12, 209), (42, 16, 125, 231))
image.putpixel((264, 143), (122, 136, 25, 213))

out = "out.png"
image.save(out)

with exiftool.ExifToolHelper() as et:
    metadata = {
        "PNG:Description": "jctf{not_the_flag}",
        "PNG:Title": "kool_pic",
        "PNG:Author": "anon",
    }
    et.set_tags(out, metadata)
