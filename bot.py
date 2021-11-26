import discord, os , dotenv, json, urlextract

from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='PROT')
# client = discord.Client()
# 
# @client.event
# async def on_ready():
#     print(f'{bot.user.name} has connected to Discord.')
#     # await channel.send(f'{bot.user.name} has connected to Discord')
# 
# @client.event
# async def on_join():
#     for guild in bot.guilds:
#         path = "servers/" + str(guild.id)
#         try:
#             os.mkdir(path)
# 
#             data = {
#                 "flags": ["flag"],
#                 "members": guild.members,
#             }
# 
#             path = path + "/settings.json"
# 
#             os.mkdir(path)
#         except FileExistsError:
#             path = "servers/" + str(guild.id) + "/settings.json"

# deletes messages in list "word"
@bot.event
async def on_message(message):
    msg_content = message.content.lower()
    path = "servers/" + str(message.guild.id) + ".json"
    data = json.load(open(path, 'r'))
    flags = data['flags']
    if any(flag in msg_content for flag in flags):
        await message.channel.send("You used a bad word!")

@bot.event
async def on_message(message):
    bad_webs = ["google", "www.foxnews"]
    msg_content = message.content.lower()
    #if link, check it, reply to message
    if "https://" in msg_content:
        name = msg_content.split("https://")[1].split(".com")[0]
        if name.lower() in bad_webs:
            await message.reply("BAD BOO")

@bot.command(name='add')
async def add_to_flags(ctx, arg):
    if ctx.message.author.guild_permissions.administrator:
        path = "servers/" + str(ctx.guild.id) + "/settings.json"
        serverSettings = json.load(open(path, 'r'))
        serverSettings['flags'] = serverSettings['flags'].append(arg)

        os.remove(path)

        json.dump(serverSettings, open(path, 'w'))
    else:
        await ctx.send("Only admins can add to the list of flags.")

            
@bot.command()
async def suggest(ctx):
    author = ctx.message.author
    msg = ctx.message.content
    flag = msg.split("suggest ")[1]
    text = discord.Embed(
        title=f"Should this be a flag?", description=flag, color=discord.Color((0x0000FF)))
    msg = await ctx.reply(embed=text)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# client.run(TOKEN)
bot.run(TOKEN)
