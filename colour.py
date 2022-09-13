from colorthief import ColorThief
from urllib.request import urlopen
import io
import discord

def get_colour(id):
    url = f'https://img.youtube.com/vi/{id}/default.jpg'
    fd = urlopen(url)
    f = io.BytesIO(fd.read())
    color_thief = ColorThief(f)
    rgb = list(color_thief.get_palette(color_count=6))
    print(rgb)
    which_palette = int(len(rgb) / 2)
    colour =  discord.Color.from_rgb(rgb[which_palette][0], rgb[which_palette][1], rgb[which_palette][2])
    return colour
