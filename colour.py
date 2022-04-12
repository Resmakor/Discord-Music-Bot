from webbrowser import get
from colorthief import ColorThief
import sys
import io
import discord

def get_colour(id):
    url = f'https://img.youtube.com/vi/{id}/default.jpg'
    if sys.version_info < (3, 0):
        from urllib2 import urlopen
    else:
        from urllib.request import urlopen
    fd = urlopen(url)
    f = io.BytesIO(fd.read())
    color_thief = ColorThief(f)
    rgb = list(color_thief.get_palette(color_count=6))
    print(rgb)
    
    which_palette = int(len(rgb) / 2)
    colour =  discord.Color.from_rgb(rgb[which_palette][0], rgb[which_palette][1], rgb[which_palette][2])
    return colour

