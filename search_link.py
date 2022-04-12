import urllib.request

import re


def polish_signs(url):
    while 'ą' in url or 'Ą' in url:
        url = url.replace('ą', 'a')
        url = url.replace('Ą', 'A')
    while 'ę' in url or 'Ę' in url:
        url = url.replace('ę', 'e')
        url = url.replace('Ę', 'E')
    while 'ć' in url or 'Ć' in url:
        url = url.replace('ć', 'c')
        url = url.replace('Ć', 'C')
    while 'ż' in url or 'Ż' in url:
        url = url.replace('ż', 'z')
        url = url.replace('Ż', 'Z')
    while 'ż' in url or 'Ź' in url:
        url = url.replace('ź', 'z')
        url = url.replace('Ź', 'Z')
    while 'ł' in url or 'Ł' in url:
        url = url.replace('ł', 'l')
        url = url.replace('Ł', 'L')
    while 'ó' in url or 'Ó' in url:
        url = url.replace('ó', 'o')
        url = url.replace('Ó', 'O')
    while 'ś' in url or 'Ś' in url:
        url = url.replace('ś', 's')
        url = url.replace('Ś', 'S')
    return url

def link(url):
    url = polish_signs(url)
    url = url.replace(" ", "+")

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + str(url))

    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    return str("https://www.youtube.com/watch?v=" + str(video_ids[0]))