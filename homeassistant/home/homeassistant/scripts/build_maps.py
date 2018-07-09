"""
#!/usr/bin/env python3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Released by: Asphalter

Thanks to DustCloud project: https://raw.githubusercontent.com/dgiese/dustcloud
Thanks to CodeKing: https://github.com/dgiese/dustcloud/issues/22#issuecomment-367618008

"""
import argparse
import io
from PIL import Image, ImageDraw, ImageChops


def build_map(slam_log_data, map_image_data):
    map_image = Image.open(io.BytesIO(map_image_data))
    map_image = map_image.convert('RGBA')
    map_image = map_image.resize((map_image.size[0]*3, map_image.size[1]*3))

    # calculate center of the image
    center_x = map_image.size[0] / 2
    center_y = map_image.size[0] / 2

    map_image = map_image.rotate(-90)

    color_move = (238, 247, 255, 255)
    color_dot = (164, 0, 0, 255)
    color_ext_background = (82, 81, 82, 255)
    color_home_background = (35, 120, 198, 255)
    color_wall = (105, 208, 253, 255)
    color_white = (255, 255, 255, 255)
    color_grey = (125, 125, 125, 255)
    color_black = (0, 0, 0, 255)
    color_transparent = (0, 0, 0, 0)

    # prepare for drawing
    draw = ImageDraw.Draw(map_image, 'RGBA')

    # loop each line of slam log
    prev_pos = None
    for line in slam_log_data.split("\n"):
        # find positions
        if 'estimate' in line:
            d = line.split('estimate')[1].strip()

            # extract x & y
            y, x, z = map(float, d.split(' '))

            # set x & y by center of the image
            x = center_x + (x * 60)
            y = center_y + (y * 60)

            pos = (x, y)
            if prev_pos:
                draw.line([prev_pos, pos], color_move, 1)
            prev_pos = pos

    # draw current position
    def ellipsebb(x, y):
        return x-5, y-5, x+5, y+5
    draw.ellipse(ellipsebb(x, y), color_dot)

    map_image = map_image.rotate(90)

    # crop image
    bgcolor_image = Image.new('RGBA', map_image.size, color_grey)
    cropbox = ImageChops.subtract(map_image, bgcolor_image).getbbox()
    map_image = map_image.crop(cropbox)

    # and replace background with transparent pixels
    pixdata = map_image.load()
    for y in range(map_image.size[1]):
        for x in range(map_image.size[0]):
            # Image Background
            if pixdata[x, y] == color_grey:
               pixdata[x, y] = color_transparent
            # Home floor
            elif pixdata[x, y] == color_white:
                pixdata[x, y] = color_home_background
            # Home wall
            elif pixdata[x, y] == color_black:
                pixdata[x, y] = color_wall
            # Hide everything else (if you want sensors to be hidden uncomment this)
            #elif pixdata[x, y] not in [color_move, color_dot]:
            #    pixdata[x, y] = color_home_background

    temp = io.BytesIO()
    map_image.save(temp, format="png")

    return temp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
Process the runtime logs of the vacuum (SLAM_fprintf.log, navmap*.ppm from /var/run/shm)
and draw the path into the map. Outputs the map as a PNG image.
    """)

    parser.add_argument(
        "-slam",
        default="SLAM_fprintf.log",
        required=False)
    parser.add_argument(
        "-map",
        required=True)
    parser.add_argument(
        "-out",
        required=False)
    args = parser.parse_args()

    with open(args.slam) as slam_log:
        with open(args.map, 'rb') as mapfile:
            augmented_map = build_map(slam_log.read(), mapfile.read(), )

    out_path = args.out
    if not out_path:
        out_path = args.map[:-4] + ".png"
    if not out_path.endswith(".png"):
        out_path += ".png"

    with open(out_path, 'wb') as out:
        out.write(augmented_map.getvalue())
