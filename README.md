# Discord Music Bot "Understandek"
### Video Demo:  <https://youtu.be/ZxDVZb1gRaw> 


## Description
"Understandek" is a Discord Music Bot with many other features. At first (January 2022) Understandek was made for fun and due to the fact that most of the available music bots at that time were blocked from Discord. In September 2022 bot was refactorized a bit so that others can use it more easily. Bot was made in Python. I tried to wrote it as simple as possible. Video demo was recorded before refactorization, however it shows Understandek's main capabilities.

## File "colour.py"
In file "colour.py" there is one function called ```get_colour``` responsible for finding the most suitable Discord embed colour. From the YouTube thumbnail the color palettes are separated and the middle one is always chosen.

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/Embed.png?raw=true)

## File "search_link.py"
In file "search_link.py" there is one function called ```search_link``` that returns YouTube url from words typed by user.
To begin with, YouTube search engine works in such a way that the sum of the words you type in the search box is included in the constant: 
- ```https://www.youtube.com/results?search_query=<words from searchbox>```

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/search_link_snippet.png?raw=true)

To make ```search_link``` more universal ```unidecode``` function removes non-ASCII characters (for instance German umlauts).

The next step is searching through HTML of the following page for video ids. We can distinct them due to the fact that each YouTube video url has a regular expression with 11 characters unique identifier. Thus we are looking for:
- ```watch\?v=<unique 11 characters>``` expression.

For that example final YouTube url returned by function ```search_link``` for user's words "dua lipa levitating" is:
-  ```https://www.youtube.com/watch?v=TUVcZfQe-Kw&ab_channel=DuaLipa```

**Be aware that sometimes the first search result in HTML code may not be what you are looking for! I decided to leave it as it is (first video id instead of user spending time choosing link), but it can be edited easily.**

## File "requirements.txt"
File "requirements.txt" is a list with the libraries needed for the bot to work.

**You have to install [FFmpeg](https://ffmpeg.org/) as well!**

#
# File "understandek.py"
File "understandek.py" is the crux of my project.

 At the beginning there is the initialization of the bot with environment variables, prefix to cause commands and some intents to make it all work.
```python 
token = str(os.environ['token'])
bot_id = int(os.environ['bot_id'])
bot_prefix = ","
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True
client = commands.Bot(command_prefix=bot_prefix, intents=intents)
```
## Then there are 2 ```@client.event```:
```python 
@client.event 
async def on_ready():
```
- Function changes bot Discord status, when bot is online. 
#
```python
@client.event
async def on_message(message):
```
- Bot responds to keywords related to 'xD' emote.
#
## After those events there is ```@client.command()``` section and some support functions:
#
```python
@client.command()
async def join(ctx)
```
- Bot joins voice channel.
#
```python
@client.command()
async def dc(ctx):
```
- Bot disconnects from voice channel and says goodbye via ```tts```.
#
```python
list_of_songs = []
def add_to_queue(url):
```
- Function adds song's url to ```list_of_songs``` (global list of YouTube urls).
#
```python
embed_queue = discord.Embed(title="Queue  🎵 🎵 🎵", url="https://github.com/Resmakor", color=0x44a6c0)
def add_to_embed(video_title, url, duration):
```
- Function adds song to global embed (```embed_queue```) related to queue.
#
```python
@client.command()
async def queue(ctx):
```
- Function shows status of queue via sending ```embed_queue```.

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/queue_embed.png?raw=true)

#
```python
async def show_status(ctx, video_title, duration, id, colour_id):
```
- Function shows which song is being played and add reactions to some of them (```beloved``` and ```disgusting``` list)

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/bot_reaction_to_song.png?raw=true)

#
```python
ctx_queue = [] # list of saved context's
if_loop = False # variable that says whether the loop is on

FFMPEG_OPTIONS = {'before_options': '-ss 00:00:00.00 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} # FFmpeg options
previous_hours = previous_minutes = previous_seconds = 0 # used in get_ss_time function
```
#
```python
def play_queue():
```
- Function plays music in ```list_of_songs``` order. When list of songs is empty, playing is finished. Time.sleep is used to fixed bug with ```voice.is_playing()```, it used to return true value, when there was no music playing.
#
```python
@client.command()
async def play(ctx, url1 = "", url2 = "", url3 = "", url4 = "", url5 = "", url6 = ""):
```
Function ```play``` deals with:
- bot joining voice channel, 
- getting valid YouTube url, 
- downloading YouTube playlist, 
- adding song to queue, 
- updating ```queue_embed```, 
- sending ```queue_embed```, 
- initializing ```play_queue``` function.

Variables called ```url1```, ```url2```, ```url3```, ```url4```, ```url5```, ```url6``` are 6 words after command ```play```. For instance, let's execute ```,play young leosia rok tygrysa```:
```python
url1 = "young", 
url2 = "leosia", 
url3 = "rok", 
url4 = "tygrysa", 
url5 = ""
url6 = ""
```

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/play_command_whole.png?raw=true)


**I decided to do it this way so that the user would not enter too many words to search and for the sake of code readability**

#
```python
@client.command()
async def forward(ctx, seconds):
```
- Function rewinds the song by a given number of seconds. Support functions: ```show_time```, ```get_ss_time```.

```python
async def show_time(ctx, timer : str):
```
- Function shows time of a song already set.

```python
def get_ss_time(seconds, end):
```
- Function gets valid time (```FFMPEG``` type) after ```forward``` command in order to change ```FFMPEG OPTIONS```. For instance: "00:01:20.00".

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/forward_command.png?raw=true)


#
```python
@client.command()
async def pause(ctx):
```
```python
@client.command()
async def resume(ctx):
```
```python
@client.command()
async def skip(ctx):
```
- These functions in order: ```pause```, ```resume```, ```skip``` the music.

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/pause_resume_skip.png?raw=true)

#
```python
@client.command()
async def clear(ctx, amount):
```
- Bot clears text channel by deleting its own messages and messages with bot prefix.
- Bot searches through ```amount``` of messages behind.
    
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/clear_command.png?raw=true)

#
```python
@client.command()
async def loop(ctx):
```
- Function starts loop by changing ```if_loop``` value.
Loop makes it so that songs are no longer removed from the ```list_of_songs``` and ```ctx_queue```.

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/loop_command.png?raw=true)

#
```python
@client.command()
async def listen(ctx, member : discord.Member):
```
- Function send messages with some details about discord member who's listening to song on Spotify. Embed is not impressive, that command was fully made for fun.

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/listen_command_2.png?raw=true)

#
```python
@client.command()
async def cannon(ctx, member : discord.Member):
```
- Bot is moving specific user through all channels. Afterwards user is back on his previous voice channel. You can see how it works in demo on YouTube. You have to own ```cannon``` rank.
#
```python
@client.command()
async def coin(ctx):
```
- Function tosses a coin.
#
```python
@client.command()
async def help(ctx):
```
- Function shows available commands with description.
