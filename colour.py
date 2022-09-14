from colorthief import ColorThief
from urllib.request import urlopen
from io import BytesIO
from discord import Color

def get_colour(id):
    """Function finds the most suitable embed colour from YouTube thumbnail"""
    url = f'https://img.youtube.com/vi/{id}/default.jpg'
    fd = urlopen(url)
    f = BytesIO(fd.read())
    color_thief = ColorThief(f)
    rgb = list(color_thief.get_palette(color_count=6))
    print(rgb)
    which_palette = int(len(rgb) / 2)
    colour = Color.from_rgb(rgb[which_palette][0], rgb[which_palette][1], rgb[which_palette][2])
    return colour
