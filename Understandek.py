import asyncio
import os
import random
import time
import datetime
import re
import validators

import discord
from discord import FFmpegOpusAudio, Spotify
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get 

from youtube_dl import YoutubeDL
from pytube import YouTube
from pytube import Playlist

import colour
import search_link


token = str(os.environ['token'])
bot_id = int(os.environ['bot_id'])
bot_prefix = ","

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True
client = commands.Bot(command_prefix=bot_prefix, intents=intents)

client.remove_command("help")

@client.event
async def on_ready():
    """Function changes bot status to: listening Young Leosia - Szklanki when bot is online"""
    print("Understandek is online")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Young Leosia - Szklanki"))

@client.event
async def on_message(message):
    """Bot responds to keywords related to 'xD' emote"""
    if message.author.bot == False and message.content != str(bot_prefix) and not validators.url(message.content):
        special_words = ['xd', 'xD', 'XD', 'Xd']
        for word in special_words:
            if word in message.content:
                if word == 'Xd':
                    await message.channel.send('Xd is not an emote!')
                else:
                    await message.channel.send(f'Haha {word}')
    await client.process_commands(message)

@client.command()
async def join(ctx):
    """Bot joins voice channel"""
    try:
        if not ctx.guild.voice_client in client.voice_clients:
                channel = ctx.author.voice.channel
                await channel.connect()
        else:
            await ctx.channel.send('I am in the voice channel!')
    except:
        await ctx.channel.send('You are not in the voice channel!')

@client.command()
async def dc(ctx):
    """Bot disconnects from voice channel"""
    if ctx.guild.voice_client in client.voice_clients:
        await ctx.send('See you soon!', tts=True, delete_after=4)
        await ctx.voice_client.disconnect()
    else:
        await ctx.channel.send('I am not in the voice channel!')


list_of_songs = []
def add_to_queue(url):
    """Function adds song to 'list_of_songs' (global list of YouTube urls)"""
    global list_of_songs
    list_of_songs.append(str(url))


embed_queue = discord.Embed(title="Queue  🎵 🎵 🎵", url="https://github.com/Resmakor", color=0x44a6c0)
def add_to_embed(video_title, url, duration):
    """Function adds song to global embed related to queue"""
    global embed_queue
    min_dur = datetime.timedelta(seconds=duration)
    value_to_be_given = f"Estimated time: {min_dur} " + url
    embed_queue.add_field(name=f"{video_title}", value=value_to_be_given, inline=False)


@client.command()
async def queue(ctx):
    """Function shows status of queue"""
    global embed_queue
    await ctx.channel.send(embed=embed_queue, delete_after=30)


async def show_status(ctx, video_title, duration, id, colour_id):
    """Function shows which song is being played and add reactions to some of them (beloved and disgusting)"""
    min_dur = datetime.timedelta(seconds=duration)
    quick_embed = discord.Embed(title=f"**{video_title}** 🎵", description=f'Song duration **{min_dur}**', color=colour_id)
    quick_embed.set_thumbnail(url=f"https://img.youtube.com/vi/{id}/0.jpg")
    await ctx.channel.send(embed=quick_embed)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=video_title))
    
    title_to_upper = video_title.upper()
    beloved = ['LEOSIA', 'SENTINO', 'POWW']
    disgusting = ['SZPAKU', 'CHIVAS']

    for word in beloved:
        if word in title_to_upper:
            await ctx.message.add_reaction("❤️")
            break

    for word in disgusting:
        if word in title_to_upper:
            await ctx.message.add_reaction("🥶")
            await ctx.message.add_reaction("🤮")
            await ctx.message.author.send("Reflect on yourself :)")
            break


async def show_time(ctx, timer : str):
    """Function shows time of a song already set"""
    await ctx.channel.send(f'Current time set to: **{timer}**', delete_after=10)


ctx_queue = []
if_loop = False
FFMPEG_OPTIONS = {'before_options': '-ss 00:00:00.00 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
previous_hours = previous_minutes = previous_seconds = 0

def play_queue():
    """Function plays music in 'queue' order. When list of songs is empty playing is finished."""
    """Time.sleep is used to fixed bug with voice.is_playing(), it was sending true value when there was no music playing"""

    global FFMPEG_OPTIONS, ctx_queue, list_of_songs, started_time, previous_hours, previous_minutes, previous_seconds
    print(list_of_songs)

    if len(list_of_songs) > 0:
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(list_of_songs[0], download=False)
                video_title = info.get('title', None)
                global duration
                duration = info['duration']

        ctx = ctx_queue[0]
        time.sleep(0.2)
        voice = get(client.voice_clients, guild=ctx.guild)
        global if_loop
        started_time = 0
        URL = info['formats'][0]['url']
        ids = re.findall(r"watch\?v=(\S{11})", list_of_songs[0])
        id = ids[0]
        colour_id = colour.get_colour(id)
        voice.play(FFmpegOpusAudio(URL, **FFMPEG_OPTIONS), after = lambda e: play_queue())
        
        timer = FFMPEG_OPTIONS['before_options']
        timer = timer[4:15]
  
        global current_url, current_ctx
        current_url = list_of_songs[0]
        current_ctx = ctx
              
        time.sleep(1.5)
        started_time = time.time()
              
        if voice.is_playing():
          if '00:00:00.00' == timer:
              client.loop.create_task(show_status(ctx, video_title, duration, id, colour_id))
              previous_seconds = previous_minutes = previous_hours = 0
          else: 
              client.loop.create_task(show_time(ctx, timer))
          if if_loop == False:
              del list_of_songs[0]
              del ctx_queue[0]
              global embed_queue
              embed_queue.remove_field(0)       
            
    else:
        FFMPEG_OPTIONS = {'before_options': '-ss 00:00:00.00 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}      

@client.command()
async def play(ctx, url1 = "", url2 = "", url3 = "", url4 = "", url5 = "", url6 = ""):
    """Function deals with bot joining voice channel, getting valid YouTube url,"""
    """downloading YouTube playlist, adding song to queue, updating queue_embed, sending queue_embed and initializing song queue"""
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    global ctx_queue, embed_queue, list_of_songs
    
    url = url1 + url2 + url3 + url4 + url5 + url6
    print(url)

    if not ctx.guild.voice_client in client.voice_clients:
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            await ctx.channel.send("You are not in a voice channel!")
            return

    if validators.url(url) != 1:
        url = search_link.link(url)

    if (validators.url(url) == 1) and 'list=' in url:
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        for x in playlist.video_urls:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(x, download = False)
                video_title = info.get('title', None)
                add_to_queue(x)
                add_to_embed(video_title, x, info['duration'])
                ctx_queue.append(ctx)
    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', None)
                add_to_queue(url)
                add_to_embed(video_title, url, info['duration'])
                time.sleep(0.2)
        ctx_queue.append(ctx)

    voice = get(client.voice_clients, guild=ctx.guild)
    if (len(list_of_songs) > 1 or (voice.is_playing() or voice.is_paused())):
        await ctx.channel.send(embed=embed_queue, delete_after=8)

    play_queue()
    

@client.command()
async def pause(ctx):
    """Function pauses music"""
    time.sleep(0.1)
    voice = get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.pause()
            await ctx.channel.send('Song **paused** ⏸️')
        else:
            await ctx.channel.send('Nothing is playing right now!')
    except:
        await ctx.channel.send('Nothing is playing right now!')

def get_ss_time(seconds, end):
    """Function gets valid time after forward command (to change FFMPEG OPTIONS)"""
    """For instance: 00:01:20.00"""
    seconds = abs(seconds)
    print(duration)
    h = int(duration / 3600)
    m = int((duration / 60) % 60)
    s = duration % 60

    ss_music_whole_time = str(datetime.time(h, m, s)) + ".00"

    global started_time
    global previous_hours, previous_minutes, previous_seconds

    current_hours = int(round(end - started_time) / 3600)
    current_minutes = int(round(end - started_time) / 60)
    current_seconds = round(end - started_time) % 60

    new_hours = previous_hours + int(seconds / 3600) + current_hours
    new_minutes = previous_minutes + int(seconds / 60) + current_minutes
    new_seconds = previous_seconds + (seconds % 60) + current_seconds

    print("Time passed: ", current_hours, current_minutes, current_seconds)
    print("New time: ", new_hours, new_minutes, new_seconds)

    if new_seconds >= 60:
        new_minutes += int(new_seconds / 60)
        new_seconds = (new_seconds % 60)
        if new_minutes >= 60:
            new_hours += int(new_minutes / 60)
            new_minutes = new_minutes % 60

    elif new_minutes >= 60:
        new_hours += int(new_minutes / 60)
        new_minutes = new_minutes % 60

    ss_time = str(datetime.time(new_hours, new_minutes, new_seconds)) + ".00"
    print(ss_time)
    print(ss_music_whole_time)

    if ss_music_whole_time > ss_time:
        previous_hours = new_hours
        previous_minutes = new_minutes
        previous_seconds = new_seconds
        return ss_time
    else:
        return 0

@client.command()
async def forward(ctx, seconds):
    """Function rewinds the song by a given number of seconds"""
    try:
        seconds = int(seconds)
    except:
         await ctx.channel.send(f"Argument '{seconds}' is not a valid argument!")
         return
    time.sleep(0.1)   
    voice = get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing() and ctx.guild.voice_client in client.voice_clients:
            end = time.time()
            ss_time = get_ss_time(seconds, end)
            global list_of_songs, ctx_queue, if_loop, current_url, current_ctx, FFMPEG_OPTIONS
            if if_loop == False and ss_time != 0:
                list_of_songs.insert(0, current_url)
                ctx_queue.insert(0, current_ctx)
                FFMPEG_OPTIONS = {'before_options': f'-ss {ss_time} -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            time.sleep(0.5)
            voice.stop()
        else:
            await ctx.channel.send("Nothing is playing right now!")
    except:
        await ctx.channel.send("Nothing is playing right now!")

@client.command()
async def resume(ctx):
    """Function resumes song"""
    time.sleep(0.1)
    voice = get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_paused() and ctx.guild.voice_client in client.voice_clients:
            await ctx.channel.send('Song **resumed** ⏯️')
            voice.resume()
        else:
            await ctx.channel.send('Nothing is paused right now!')
    except:
        await ctx.channel.send('Nothing is paused right now!')

@client.command()
async def skip(ctx):
    """Function skips song"""
    time.sleep(0.5)
    voice = get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing() or voice.is_paused() and ctx.guild.voice_client in client.voice_clients:
            global FFMPEG_OPTIONS
            await ctx.channel.send('Song **skipped** ⏹️')
            voice.stop()
            FFMPEG_OPTIONS = {'before_options': '-ss 00:00:00.00 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        else:
            await ctx.channel.send('Nothing is playing right now!')
    except:
        await ctx.channel.send('Nothing is playing right now!')
        

@client.command()
async def clear(ctx, amount):
    """Bot clears text channel by deleting its own messages and messages with bot prefix"""
    try:
        amount = abs(int(amount))
    except:
         await ctx.channel.send(f"Argument '{amount}' is not a valid argument!")
         return
    deleted_messages = await ctx.channel.purge(limit=amount, check=lambda x: bot_prefix in x.content or bot_id == x.author.id)
    how_many = len(deleted_messages)
    await ctx.send(f"**{how_many}** messages have been deleted! ♻️", delete_after=10)

@client.command()
async def loop(ctx):
    """Function starts loop"""
    """Loop makes it so that songs are no longer removed from the 'list_of_songs' and 'ctx_queue'"""
    global if_loop
    if if_loop == False:
        if_loop = True
        await ctx.send("Loop **enabled** 🔁")
    else:
        if_loop = False
        await ctx.send("Loop **disabled** ❌")
        voice = get(client.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing and len(list_of_songs) > 0:
                    del list_of_songs[0]
                    del ctx_queue[0]
                    global embed_queue
                    embed_queue.remove_field(0)
        except:
            return
            
@client.command()
async def listen(ctx, member : discord.Member):
    """Function send messages with some details about discord member who's listening to song on Spotify"""
    try:
        sname = member.activity.title
        sartists = member.activity.artists
        album = member.activity.album
        palbum = member.activity.album_cover_url
        duration = member.activity.duration
        quick_embed = discord.Embed(title=f"{member} listens now {sname} from {album}, there are: {sartists}", description=f'Song duration **{duration}**', colour=0xeb1e1e)
        quick_embed.set_thumbnail(url=palbum)
        await ctx.channel.send(embed=quick_embed)
    except:
        await ctx.channel.send(f"Member {member} does not listen anything!")

@client.command()
async def cannon(ctx, member : discord.Member):
    """Bot is moving specific user through all channels. Afterwards user is back on his previous channel"""
    try:
        cannon = discord.utils.find(lambda r: r.name == 'cannon', ctx.message.guild.roles)
    except:
        await ctx.channel.send('Could not find role cannon on the server!')
        return
    if cannon in ctx.author.roles:
        current_channel_id = member.voice.channel.id
        voice_channels = ctx.guild.voice_channels
        voice_channels_ids = [channel.id for channel in voice_channels]
        if voice_channels_ids[-1] != current_channel_id:
            voice_channels_ids.append(current_channel_id)
        for channel_id in voice_channels_ids:
            channel = client.get_channel(channel_id)
            await member.move_to(channel)
        gif_embed = discord.Embed(title="KABOOM!")
        gif_embed.set_image(url="https://i.giphy.com/media/76zpU8jlNo5EHoEpjb/giphy.webp")
        await ctx.channel.send(f'{member.mention} has been blown up!', embed=gif_embed)
    else:
        await ctx.channel.send('You do not have sufficient permissions!')

@client.command()
async def coin(ctx):
    """Function tosses a coin"""
    to_be_drawn = ('Heads', 'Tails')
    await ctx.channel.send(random.choice(to_be_drawn))

@client.command()
async def help(ctx):
    """Function shows available comments with description"""
    embed = discord.Embed(title="Commands", url="https://github.com/Resmakor", description="powered by Resmakor", color=0xeb1e1e)
    embed.add_field(name=f"{bot_prefix}play <song name>", value="Bot turns the music on and joins voice channel. If something is being played, song is added to queue", inline=False)
    embed.add_field(name=f"{bot_prefix}pause", value="Bot pauses song", inline=False)
    embed.add_field(name=f"{bot_prefix}resume", value ="Bot resumes song", inline=False)
    embed.add_field(name=f"{bot_prefix}skip", value="Bot skips song", inline=False)
    embed.add_field(name=f"{bot_prefix}queue", value="Bot shows queue status", inline=False)
    embed.add_field(name=f"{bot_prefix}loop", value="Bot loops next song till someone uses 'loop' command again!", inline=False)
    embed.add_field(name=f"{bot_prefix}forward <value>", value="Bot rewinds the song by the 'value' seconds", inline=False)
    embed.add_field(name=f"{bot_prefix}join", value="Bot joins voice channel", inline=False)
    embed.add_field(name=f"{bot_prefix}dc", value="Bot leaves voice channel", inline=False)
    embed.add_field(name=f"{bot_prefix}coin", value="Bot toss a coin", inline=False)
    embed.add_field(name=f"{bot_prefix}cannon <discordmember>", value="User is being thrown to some specific channels", inline=False)
    embed.add_field(name=f"{bot_prefix}clear <value>", value="Bot deletes messages with commands and its own back <value> messages", inline=False)
    embed.add_field(name=f"{bot_prefix}listen <discordmember>", value="Bot sends what someone is listening to on Spotify", inline=False)
    await ctx.send(embed=embed, delete_after=30)

client.run(token)
