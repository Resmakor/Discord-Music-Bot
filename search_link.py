from urllib.request import urlopen
from unidecode import unidecode
from re import findall


def link(user_words):
    """Function returns YouTube url for first video id found in HTML code"""
    user_words = unidecode(user_words).replace(" ", "+")
    html = urlopen("https://www.youtube.com/results?search_query=" + str(user_words))
    video_ids = findall(r"watch\?v=(\S{11})", html.read().decode())
    return str("https://www.youtube.com/watch?v=" + str(video_ids[0]))

