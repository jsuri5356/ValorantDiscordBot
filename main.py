# main.py
# Special thanks to https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#positional and 
# https://python.plainenglish.io/send-an-embed-with-a-discord-bot-in-python-61d34c711046
import os, random, discord, requests, json, asyncio, interactions
from dotenv import load_dotenv
from discord.ext import commands
from requests import get
from interactions import Client

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
slash = interactions.Client(token= TOKEN)

@slash.command(
    name="random_map", 
    description="Get a random map!", 
    options= [
        interactions.Option(
            name="map_to_remove",
            description="Remove a map from the map list!",
            type=interactions.OptionType.STRING,
            required=False,
            choices=[
                interactions.Choice(name="Ascent", value="Ascent"), 
                interactions.Choice(name="Bind", value="Bind"), 
                interactions.Choice(name="Fracture", value="Fracture"),
                interactions.Choice(name="Icebox", value="Icebox"),
                interactions.Choice(name="Breeze", value="Breeze"),
                interactions.Choice(name="Split", value="Split"),
                interactions.Choice(name="Haven", value="Haven"),
                interactions.Choice(name="Pearl", value="Pearl"),
                interactions.Choice(name="Default", value="Default"),
            ], 
        ),
    ],
)
async def map_slash(ctx: interactions.CommandContext, map_to_remove : str = ""):
    theMap = ["Ascent", "Bind", "Fracture", "Icebox", "Breeze", "Split", "Haven", "Pearl"]
    removeMapList = map_to_remove.split(' ')
    removeMapList = [word.capitalize() for word in removeMapList]
    for i in range(len(removeMapList)):
        if(map_to_remove == "Default"):
            theMap.remove("Breeze")
            theMap.remove("Fracture")
        if map_to_remove in theMap:
            theMap.remove(removeMapList[i])
    if(len(theMap) == 0):
        await ctx.send("Why are you removing all the maps???")
        return;
    rng = random.SystemRandom()
    index = rng.randint(0,(len(theMap) - 1))
    await ctx.send("Your map is " + theMap[index])


@bot.command(name = "8ball", brief = "Go ahead, ask a quesiton")
async def eightBall(ctx, *ball):
    array = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    message = ' '.join(ball)
    if message == "":
        embed=discord.Embed(title="Error", color=0xFF0000, description = "Please enter a question you want answered! \ni.e `$8ball will I ever stop being being hardstuck gold`")
        await ctx.reply(embed = embed)
        return;
    rng = random.SystemRandom()
    index = rng.randint(0,(len(array) - 1))
    if(index <= 9):
        embed=discord.Embed(title=message.title(), color=0x00FF00, description = f"\n{array[index]}")
    elif(9 < index <= 14):
        embed=discord.Embed(title=message.title(), color=0xfcec03, description = f"\n{array[index]}")
    else:
        embed=discord.Embed(title=message.title(), color=0xFF0000, description = f"\n{array[index]}")
    embed.set_footer(text="8ball - Valorant Discord Bot")
    await ctx.reply(embed=embed)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Playing Valorant!'))

@bot.command(name='map', brief="Picks a random map", description = "Picks a random map, to delete a map just type the map out followed by a space i.e \n'$map icebox`\nthis will delete icebox out of the list of maps\n\ndoing `$map default` will delete Breeze and Fracture")
async def randomMap(ctx, *mapToRemove):
    theMap = ["Ascent", "Bind", "Fracture", "Icebox", "Breeze", "Split", "Haven", "Pearl"]
    removeMap = ', '.join(mapToRemove)
    removeMapList = removeMap.split(', ')
    removeMapList = [word.capitalize() for word in removeMapList]
    for i in range(len(removeMapList)):
        if(removeMapList[i] == "Default"):
            theMap.remove("Breeze")
            theMap.remove("Fracture")
        if removeMapList[i] in theMap:
            theMap.remove(removeMapList[i])
    if(len(theMap) == 0):
        await ctx.send("Why are you removing all the maps???")
        return;
    rng = random.SystemRandom()
    index = rng.randint(0,(len(theMap) - 1))
    await ctx.reply("Your map is " + theMap[index])

@bot.command(name = 'agent', brief = "Picks a random map")
async def randomAgent(ctx, *agentToRemove):
    Agents = ["Brimstone", "Viper", "Omen", "Killjoy", "Cypher", "Sova", "Sage", "Phoenix", "Jett", "Reyna", "Raze", "Breach", "Skye", "Yoru", "Astra", "KAY/O", "Chamber", "Neon", "Fade", "Harbor"]
    removeAgent = ', '.join(agentToRemove)
    removeAgentList = removeAgent.split(', ')
    removeAgentList  = [word.capitalize() for word in removeAgentList]
    for i in range(len(removeAgentList )):
        if removeAgentList[i] in Agents:
            Agents.remove(removeAgentList[i])
    if(len(Agents) == 0):
        await ctx.send("Why are you removing all the agents???")
        return;
    theAgent = random.choice(Agents)
    await ctx.reply("Your agent is " + theAgent) 
    if theAgent == "Cypher" or theAgent == "Astra":
        await ctx.send("L agent")

@bot.command(name = 'say', brief = "sayyy")
async def say(ctx, *arg1):
    message = ' '.join(arg1)
    if ctx.author.id == bot.user.id or "everyone" in message:
        return;
    await ctx.send(message)
    await ctx.message.delete()

@bot.command(name = 'ping', brief = "Shows bots latency")
async def ping(ctx):
    await ctx.reply(f':ping_pong: {round (bot.latency * 1000)} ms') 

@bot.command(name = "yury", brief = "Yury when", description = 'The other day, I got a question about what the "yury when" phrase represents.\n\nFor those who do not know, this phrase was sent in multiple text channels, commonly followed by a gif of a monkey.\n\n"yury when" is an open ended statement.\nA fill in the blank, if you will.\nThe reason the sentence is never finished is to symbolize that no matter what he is doing, Yury will always be "monke," and the activity that he is currently engrossed in has no effect on this.\n\nSo the next time you think of "monke." Find it in yourself to have the courage to say "yury when" Preferably followed by a "monke" gif.\n\nThank you.')
async def yury(ctx):
    apikey = "LIVDSRZULELA"
    lmt = 20
    search_term = "monkey"
    r = requests.get("https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
    if r.status_code == 200:
        gifs = json.loads(r.content)
        randIndex = random.randint(0,lmt - 1)
        theYuryGif = gifs['results'][randIndex]['media'][0]['gif']['url']
        embed=discord.Embed(title="Yury When", url = theYuryGif, color=0xe3c9a4)
        embed.set_image(url=theYuryGif)
        await ctx.send(embed=embed)
    else:
        gifs = None

@bot.command(name = 'meow')
async def meow(ctx):
    await ctx.send("meow")

@bot.command(name = 'cat', brief = "random cat")
async def cat(ctx):
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    image = json.loads(r.content)
    theImage = image[0]['url']
    embed = discord.Embed(title="here cat", url= theImage, color=0xFFFFFF)
    embed.set_image(url=theImage)
    await ctx.reply(embed=embed)

@bot.command(name = "die", brief = "roll a die!")
async def sixDie(ctx):
    rng = random.SystemRandom()
    die = rng.randint(1, 20)
    await ctx.reply("The die has been rolled! Your number is " + str(die))

@bot.command(name = "goober", brief = "bans goober")
async def pooper(ctx):
    await ctx.send("Banning <@381444531792379905>")

@bot.command(name = "gif", brief = "Random gif with the name!")
async def gif(ctx, *randomGif):
    apikey = "LIVDSRZULELA"
    lmt = 8
    message = ' '.join(randomGif)
    search_term = message
    r = requests.get("https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
    if r.status_code == 200:
        gifs = json.loads(r.content)
        randIndex = random.randint(0,lmt - 1)
        theYuryGif = gifs['results'][randIndex]['media'][0]['gif']['url']
        embed=discord.Embed(title=message, url = theYuryGif, color=0xe3c9a4)
        embed.set_image(url=theYuryGif)
        await ctx.reply(embed=embed)
    else:
        gifs = None


@bot.command(name = "meme", brief = "add/display a meme!", description = "")
#async def meme(ctx, *memeKeyword):
    # if memeKeyword[0] == "add":
    #     message = ' '.join(memeKeyword)
    #     message = message.replace('add', '')
    #     await ctx.send(message)
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)


@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Error", description = f"{error}", color=0xFF0000) 
        await ctx.reply(embed=embed)


# for the bot to join the vc you're in rn voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #asyncio.set_event_loop(loop)
    task2 = loop.create_task(bot.start(TOKEN))
    task1 = loop.create_task(slash._ready())

    gathered = asyncio.gather(task1, task2)
    loop.run_until_complete(gathered)
