import discord
import os
from discord.ext import commands,tasks
import requests
import json
from keep_alive import keep_alive
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.voice_client import VoiceClient
import youtube_dl
from random import choice
from random import choice
import wolframalpha
from tkinter import *
from tkinter import ttk
import urllib.parse
from urllib.request import urlopen
import xmltodict
from urllib import request
import urllib.request
import re
import codecs
from youtubesearchpython import VideosSearch
import translators as ts
import asyncio
from vs import counter_hero
client = commands.Bot(command_prefix="?",help_command=None)

app_id = os.getenv("app_id")

youtube_dl.utils.bug_reports_message = lambda: ''
#format ต้องระบุเพราะโมดูล youtube_dl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}
#from FFmpegPCMAudio module ระบุเพื่อหาเพลง จ้า
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=True, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

status = ['Jamming out to music!', 'Eating!', 'Sleeping!']
n = 1
queue = []

@client.event
async def on_guild_join(guild):
  with open("queue.json","r") as f:
    queue = json.load(f)
  queue[guild.id] = []
  with open("queue.json","w") as f:
    json.dump(queue,f,indent=4)


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'ยินดีต้อนรับ {member.mention}!  พร้อมที่จะสรรเสริญเต้ยเเล้วหรือยัง? พิมพ์ ?command เพื่อโชว์คำสั่ง')
        
@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**ปิงง!** ค่า Latency: {round(client.latency * 1000)}ms')


@client.command(name='credit', help='This command returns the credits')
async def credits(ctx):
    await ctx.send('สร้างโดย `กูนัท`')
    await ctx.send('API Dota2:https://docs.stratz.com/index.html')
    await ctx.send('Discord Doc:https://discordpy.readthedocs.io/en/stable/index.html')
    await ctx.send("wolframalpha Doc:https://products.wolframalpha.com/api/")

@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("มึงไม่ได้อยู่ใน Voice channel ไอเอ๋อ")
        return
    
    else:
        channel = ctx.message.author.voice.channel
        await ctx.send("**เ ต้ ย** อยากสัมผัสคุณที่ **{}**".format(channel))

    await channel.connect()

@client.command(name='q', help='This command adds a song to the queue')
async def queue_(ctx,*, url:str):
  voice = get(client.voice_clients, guild=ctx.guild)
  global queue
  global n
  if ctx.message.author.voice and len(queue) == 0 and voice.is_playing() == False:
    txt = url
    x = txt.startswith("http")
    if x == True:
      name = url
      videosSearch = VideosSearch(name, limit = 1)
      res =  videosSearch.result()
      q = res["result"]
      aim = q[0]
      title = aim["title"]
      link = aim["link"]
      pic = aim["thumbnails"][0]["url"]
      duration = aim["duration"]
      server = ctx.message.guild
      voice_channel = server.voice_client
      queue.append(link)
      async with ctx.typing():
        #loop=client.loop
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('เออเหรอ: %s' % e) if e else None)
      author = ctx.message.author
      pfp = author.avatar_url
      embed = discord.Embed(
        colour = discord.Colour.orange()
      )
      song = [
        ["เพลง",f'`{title}`',True],
        ["ระยะเวลา",duration,True],
        ["link",link,False],
      ]
      embed.set_author(name=author, icon_url=pfp)
      for i in range(len(song)):
        if i == 0:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
          embed.set_image(url=pic)
        else:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
      await ctx.send(embed=embed)
      await ctx.send('**เต้ยกำลังร้องเพลง:** {}'.format(player.title))
      del(queue[0])
    else:
      name = url.replace(" ","+")
      videosSearch = VideosSearch(name, limit = 1)
      res =  videosSearch.result()
      q = res["result"]
      aim = q[0]
      title = aim["title"]
      link = aim["link"]
      pic = aim["thumbnails"][0]["url"]
      duration = aim["duration"]
      server = ctx.message.guild
      voice_channel = server.voice_client
      queue.append(link)
      async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('เออเหรอ: %s' % e) if e else None)
      author = ctx.message.author
      pfp = author.avatar_url
      embed = discord.Embed(
        colour = discord.Colour.orange()
      )
      song = [
        ["เพลง",f'`{title}`',True],
        ["ระยะเวลา",duration,True],
        ["link",link,False],
      ]
      embed.set_author(name=author, icon_url=pfp)
      for i in range(len(song)):
        if i == 0:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
          embed.set_image(url=pic)
        else:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
      await ctx.send(embed=embed)
      await ctx.send('**เต้ยกำลังร้องเพลง:** {}'.format(player.title))
      del(queue[0])
  elif voice.is_playing() == True:
    txt = url
    x = txt.startswith("http")
    if x == True:
      name = url
      videosSearch = VideosSearch(name, limit = 2)
      res =  videosSearch.result()
      q = res["result"]
      aim = q[0]
      title = aim["title"]
      link = aim["link"]
      duration = aim["duration"]
      pic = aim["thumbnails"][0]["url"]
      queue.append(link)
      author = ctx.message.author
      pfp = author.avatar_url
      embed = discord.Embed(
        colour = discord.Colour.orange()
      )
      song = [
        ["เพลง",f'`{title}`',False],
        ["ระยะเวลา",duration,True],
        ["link",link,False],
        ["คิวลำดับที่",len(queue),True],
        ["หมายเหตุ","ถ้าคิวไว้เเล้ว เพลงต่อๆไปให้สั่ง ?p ทุกครั้งเพื่อเล่น เพราะไม่รู้ทำไงให้มันเล่นต่อเอง จะข้ามเพลงก็ ?skip",False]
      ]
      embed.set_author(name=author,icon_url=pfp)
      for i in range(len(song)):
        if i == 0:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
          embed.set_image(url=pic)
        else:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
      await ctx.send(embed=embed)
      await ctx.send(f'`{url}` เเอดเข้าคิว!')
      n+=1
    else: 
      name = url.replace(" ","+")
      videosSearch = VideosSearch(name, limit = 2)
      res =  videosSearch.result()
      q = res["result"]
      aim = q[0]
      title = aim["title"]
      link = aim["link"]
      duration = aim["duration"]
      pic = aim["thumbnails"][0]["url"]
      queue.append(link)
      author = ctx.message.author
      pfp = author.avatar_url
      embed = discord.Embed(
        colour = discord.Colour.orange()
      )
      song = [
        ["เพลง",f'`{title}`',False],
        ["ระยะเวลา",duration,True],
        ["link",link,False],
        ["คิวลำดับที่",len(queue),True],
        ["หมายเหตุ","ถ้าคิวไว้เเล้ว เพลงต่อๆไปให้สั่ง ?p ทุกครั้งเพื่อเล่น เพราะไม่รู้ทำไงให้มันเล่นต่อเอง จะข้ามเพลงก็ ?skip",False]
      ]
      embed.set_author(name=author,icon_url=pfp)
      for i in range(len(song)):
        if i == 0:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
          embed.set_image(url=pic)
        else:
          embed.add_field(name=song[i][0],value=song[i][1],inline=song[i][2])
      await ctx.send(embed=embed)
      await ctx.send(f'`{url}` เเอดเข้าคิว!')
      n+=1


@client.command(name='remove', help='This command removes an item from the list')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number-1)])
        await ctx.send(f'คิวตอนนี้ : `{queue}!`')
    
    except:
        await ctx.send('คิวมึงไม่ **empty** ก็ **out of range** อะ')
        
@client.command(name='p', help='This command plays songs')
async def play(ctx):
    global queue
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('เออเหรอ: %s' % e) if e else None)
    await ctx.send('**เต้ยกำลังร้องเพลง:** {}'.format(player.title))
    del(queue[0])

@client.command(name='skip', help='Skip song')
async def skip(ctx):
  global queue
  try:
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()
    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('เออเหรอ: %s' % e) if e else None)
        await ctx.send('**เต้ยกำลังร้องเพลง:** {}'.format(player.title))
    del(queue[0])
  except:
    await ctx.send("หมดเพลงละ มึงจะให้กูร้องยังไง")

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command(name='view', help='This command shows the queue')
async def view(ctx):
    global queue
    name_song_lis = []
    for i in queue:
      videosSearch = VideosSearch(i, limit = 1)
      res =  videosSearch.result()
      q = res["result"]
      aim = q[0]
      name = aim["title"]
      name_song_lis.append(name)
    await ctx.send(f'คิวตอนนี้คือ `{name_song_lis}!`')

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

#----------------------------------------------------------
def player_country(ids:float):
  r = requests.get("https://api.stratz.com/api/v1/player/{}".format(ids))
  player = r.text
  dict_player = json.loads(player)
  steam_account = dict_player['steamAccount']
  for i in steam_account:
    if i == 'smurfFlag':
        check_smurf = steam_account['smurfFlag']
        if check_smurf > 0:
            chr = "เสมิฟไอเหี้ย พวกมึงโดนเเน่ !!!!"
        else:
            chr = "ไอเหี้ยนี่ไม่ใช่เสมิฟ (อาจจะ)"
        break
    else:
        chr = "ข้อมูลไม่ครบ"
  return chr




def bot_name():
  return "กู เ ต้ ย"

def where_u_from(ids:float):
  r = requests.get("https://api.stratz.com/api/v1/player/{}".format(ids))
  player = r.text
  dict_player = json.loads(player)
  steam_account = dict_player['steamAccount']
  for i in steam_account:
    if i == 'countryCode':
        check_place = steam_account['countryCode']
        chr = check_place
        break
    else:
        chr = "ไม่ปรากฎข้อมูลไอหำ"
  return chr

 #----------------------------------------------------------
@client.event
async def on_ready():
  activity = discord.Game(name="กำลังพัฒนาตัวเอง")
  await client.change_presence(status=discord.Status.online, activity=activity)
  print('กูเข้ามาเเล้วนะ {0.user}'.format(client))

@client.command()
async def trans(ctx,msg:str):
  chr = ts.google(msg,to_language="th")
  await ctx.send("{0} เเปลว่า {1} นะจ้ะ ".format(msg,chr))
@client.command()
async def smurf(ctx,x:int):
  res = player_country(x)
  await ctx.send(res)

@client.command()
async def country(ctx,x:int):
  res = where_u_from(x)
  await ctx.send(res)

@client.command()
async def name(ctx):
  res = bot_name()
  await ctx.send(res)

@client.command(pass_context=True)
async def mardman(ctx):
  if not ctx.message.author.voice:
    await ctx.send("TI 12 Champion!!!")
    await ctx.send(file=discord.File("mardman.png"))
  else:
    channel = ctx.author.voice.channel
    await channel.connect()
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.play(FFmpegPCMAudio('mardman2_cut.mp3'))
    voice.is_playing()
    await ctx.send("TI 12 Champion!!!")
    await ctx.send(file=discord.File("mardman.png"))

    
@client.command(pass_context=True)
async def พ่อหลวง(ctx):
  await ctx.send("คิดถึงคนบนฝ้า (ฟ้า)")
  await ctx.send(file=discord.File("human.jpg"))

@client.command(pass_context=True)
async def toey(ctx):
  await ctx.send("เ ต้ ย (TOEY) (1 มกราคม พ.ศ. 1 - ปัจจุบัน) เป็นนักฟิสิกส์ทฤษฎี ชาวไทยที่มีสัญชาติสวิสและอเมริกัน (ตามลำดับ) ซึ่งเป็นที่ยอมรับกันอย่างกว้างขวางว่าเป็นนักวิทยาศาสตร์ที่ยิ่งใหญ่ที่สุดในคริสต์ศตวรรษที่ 1-21 เขาเป็นผู้เสนอทฤษฎีสัมพัทธภาพ และมีส่วน ร่วมในการพัฒนากลศาสตร์ควอนตัม สถิติกลศาสตร์ และจักรวาลวิทยา เขาได้รับรางวัลโนเบลสาขาฟิสิกส์ในปี พ.ศ.1-2564 จากการอธิบายปฏิกิริยาโฟโตอิเล็กทริก และจาก' การทำประโยชน์แก่ฟิสิกส์ทฤษฎี'")


@client.command(pass_context=True)
async def kfc(ctx):
  await ctx.send("เเ ด ก ตี น กู ไ ป ก่ อ น น ะ สั ส")
  await ctx.send(file=discord.File("kfc.jpg"))


@client.command(pass_context=True)
async def ak47(ctx):
  await ctx.send("**พ รี่ ดี้**")
  await ctx.send("https://www.twitch.tv/noctisak47")

@client.command(pass_context=True)
async def บอล(ctx):
  await ctx.send("https://www.doofootball.com/")

@client.command(pass_context=True)
async def cal(ctx,*,cmd:str):
  async with ctx.typing():
    if "diff" in cmd:
      q1 = cmd
      q2 = q1.replace("diff","differrential")
      client = wolframalpha.Client(app_id)
      res = client.query(q2)
      answer = next(res.results).text
      await ctx.send("คำตอบคือ {}".format(answer))
    else:
      rquestion = cmd
      client = wolframalpha.Client(app_id)
      res = client.query(rquestion)
      answer = next(res.results).text
      await ctx.send("คำตอบคือ {}".format(answer))

@client.command(pass_context=True)
async def cpic(ctx,*,cmd:str):
  author = ctx.message.author
  async with ctx.typing():
    rquestion = cmd
    client = wolframalpha.Client(app_id)
    res = client.query(rquestion)
    answer = next(res.results)
    img = answer['subpod']
    img2 = img['img']
    src = img2['@src']
    imageURL = src
    embed = discord.Embed(
      colour = discord.Colour.blue()
    )
    embed.set_author(name="คำตอบของ {} ".format(rquestion))
    embed.set_image(url=imageURL)
    await ctx.send(embed = embed)

@client.command(pass_context=True)
async def diff(ctx,*,cmd:str):
  async with ctx.typing():
    fixed_chr = "derivative of "
    q = cmd
    q2 = fixed_chr+q
    x = urllib.parse.quote(q2)
    question = x.replace("%20","+")
    url = "http://api.wolframalpha.com/v2/query?appid=8YT7K4-VXP8XR6A5E&input={}&podstate=Step-by-step+solution&format=image".format(question)
    var_url = urlopen(url)
    my_dict = xmltodict.parse(var_url)
    try:
        res_url = my_dict["queryresult"]["pod"]["subpod"][1]["img"]["@src"]
        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        embed.set_author(name="คำตอบของ derivative of {} ".format(q))
        embed.set_image(url=res_url)
        await ctx.send(embed = embed)
    except :
        res_url = my_dict["queryresult"]["pod"][0]["subpod"][1]["img"]["@src"]
        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        embed.set_author(name="คำตอบของ derivative of {} ".format(q))
        embed.set_image(url=res_url)
        await ctx.send(embed = embed)
        


@client.command(pass_context=True)
async def update(ctx):
  author = ctx.message.author
  embed = discord.Embed(
    colour = discord.Colour.orange()
  )
  all_update = [
    ["Added ","==> ?counter เชคฮีโรที่ counter ตัวที่ถาม"],
   ["Update ","==> ไม่มี"]]
  embed.set_author(name="Update 8/09/2564")
  for i in all_update:
    embed.add_field(name=i[0],value=i[1],inline=False)
  await ctx.send(embed=embed)

@client.command(pass_context=True)
async def god(ctx):
  role = get(ctx.guild.roles, name = 'ทั่นเต้ย')
  await ctx.send(f"{role.mention}")

@client.command()
async def counter(ctx,*,hero:str):
  lis = counter_hero(hero)
  author = ctx.message.author
  embed1 = discord.Embed(
    colour = discord.Colour.orange()
  )
  embed1.set_author(name="***Hero ที่ชนะทาง {}***".format(hero))
  for i in range(0,len(lis),4):
    embed1.add_field(name=lis[i],value=lis[i+1],inline=False)
  await ctx.send(embed=embed1)

@client.command(pass_context=True)
async def cmd(ctx):
  author = ctx.message.author
  embed1 = discord.Embed(
    colour = discord.Colour.orange()
  )
  embed2 = discord.Embed(
    colour = discord.Colour.green()
  )
  embed3 = discord.Embed(
    colour = discord.Colour.red()
  )
  embed4 = discord.Embed(
    colour = discord.Colour.teal()
  )
  fun_command = [
    ["?smurf [steamID]","เชคว่าติดsmurf flag ไหม"],
    ["?country [steamID]","เชคว่าอยู่ประเทศอะไร (อาจไม่เจอ)"],
    ["?counter","เชคฮีโรที่ counter ตัวที่ถาม"],
    ["?name","ลองสิเดี๋ยวมึงก็รู้"],
    ["?mardman","อยากรู้ว่าคืออะไรก็ลองดู"],
    ["?toey","Toey's biography"],
    ["?kfc","ไอต้าวอ้วน"],
    ["?พ่อหลวง","คนบนฟ้า"],
    ["?god","เรียกหาท่านผู้นั้นออกมา"]
  ]
  song_command = [
    ["?join","เอาเต้ยเข้าห้องของมึง"],
    ["?leave","เชิญเต้ยออก"],
    ["?q ชื่อเพลง","เอาเพลงเข้าคิวเพลงเเรกจะเล่นเองเสมอ"],
    ["?p","เพื่อเล่นเพลงใน queue"],
    ["?remove [ลำดับเพลงที่จะเอาออก]","เลือกเพลงออก"],
    ["?pause ?resume ?stop ?skip","คงไม่ต้องบอกหรอกเนาะ"],
    ["?view","ดูเพลงใน queue"]
  ]
  math_command = [
    ["?cal [สิ่งที่อยากถาม]","ถามอะไรก็ได้ คณิต เคมี ประวัติศาสตร์ถามได้หมด"],
    ["?cpic [สิ่งที่อยากถาม]","เหมือน ?cal เเต่มีภาพให้"],
    ["?diff [โจทย์ differential]","เเสดงวิธีคิดออกมาเป็น step [เเค่เรื่อง diff เรื่องอื่นจะทยอยมา กุงงอยู่]"]
  ]
  etc_command = [
    ["?ak47","เปิดช่องพี่ดี้"],
    ["?บอล","ดูบอล"],
    ["?credit","ดู ref เผื่อมึงอยากทำ"],
    ["?trans","เเปลภาษา"]
  ]
  embed1.set_author(name="***Command หรอยๆ***")
  for i in fun_command:
    embed1.add_field(name=i[0],value=i[1],inline=False)
  await ctx.send(embed=embed1)

  embed2.set_author(name="***Command เพลง***")
  for i in song_command:
    embed2.add_field(name=i[0],value=i[1],inline=False)
  await ctx.send(embed=embed2)

  embed3.set_author(name="***Command อัจฉริยะ***")
  for i in math_command:
    embed3.add_field(name=i[0],value=i[1],inline=False)
  await ctx.send(embed=embed3)

  embed4.set_author(name="***Command อื่นๆ***")
  for i in etc_command:
    embed4.add_field(name=i[0],value=i[1],inline=False)
  await ctx.send(embed=embed4)

keep_alive()
client.run(os.getenv('TOKEN'))