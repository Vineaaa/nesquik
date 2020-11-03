from discord.ext import commands
import discord
import logging
import random
import array
intents = discord.Intents(guilds=True, members=True, messages=True, reactions=True)
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# general events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    activity = discord.Activity(name='the game of life | !help', type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)

@bot.event
async def on_member_join(member):
    await welc_chan.send(f'Welcome to the server {member.mention}! Make sure to read the rules!')
    await member.send("Hello, I'm Kougyoku! This is a test message.")
    return

# general commands
@commands.command()
@commands.guild_only()
async def pog(ctx):
    await ctx.send(file=discord.File('PogChamp.png'))

@commands.command()
@commands.guild_only()
async def djinn(ctx):
    with open("djinn_lib.txt", "r") as f:
        gif_list = [line.strip() for line in f]
        randgif = random.choice(gif_list)
        embed = discord.Embed(
            title = 'Transform my whole body into that of a great sorcerer!',
            color = discord.Color.teal()
            )
        embed.set_image(url = randgif)
        
    # send gif
    await ctx.send(embed=embed)
    
@commands.command()
@commands.guild_only()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
    
@commands.command()
@commands.guild_only()
async def coinflip(ctx):
    choices = ["Heads", "Tails"]
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

@commands.command()
async def help(ctx):
    embed = discord.Embed(
        title = '__Commands List__',
        color = discord.Color.dark_magenta()
        )
    # embed.set_author(name='Help') <-- Not needed right now I guess lol
    embed.add_field(name='!ping', value='Returns Pong & Latency of Bot', inline=False)
    embed.add_field(name='!coinflip', value='Does a coinflip', inline=False)
    embed.add_field(name='!djinn', value='Sends a gif of djinn equips', inline=False)
    embed.add_field(name='!help', value='Shows you this', inline=False)

    await ctx.message.author.send(embed=embed)
    
# mod/admin 
@commands.command()
@commands.has_permissions(ban_members=True)
@commands.guild_only()
async def ban(ctx, member : discord.Member, *, reason=None):
    guild = bot.get_guild(760745341476667412)
    await member.send(f'You have been banned from **{guild.name}** for reason: **{reason}**')
    await member.ban(reason=reason)

@commands.command()
@commands.guild_only()
async def kick(ctx, member : discord.Member, *, reason=None):
    admin_role = discord.utils.get(ctx.guild.roles, name= 'Authority')
    mod_role = discord.utils.get(ctx.guild.roles, name= 'Mod')
    guild = bot.get_guild(760745341476667412)
    if mod_role in ctx.author.roles:
        await member.send(f'You have been kicked from **{guild.name}** for reason: **{reason}**')
        await member.kick(reason=reason)
    elif admin_role in ctx.author.roles:
        await member.send(f'You have been kicked from **{guild.name}** for reason: **{reason}**')
        await member.kick(reason=reason)
    else:
        pass

@commands.command()
@commands.has_permissions(manage_channels=True)
@commands.guild_only()
async def set_welcome(ctx):
    global welc_chan
    welc_chan = bot.get_channel(ctx.channel.id)
    await ctx.send("**Member welcome set to this channel...**")
    
@commands.command()
@commands.has_permissions(manage_channels=True)
@commands.guild_only()
async def set_logs(ctx):
    global log_chan
    log_chan = bot.get_channel(ctx.channel.id)
    await ctx.send("**Logs set to this channel...**")
    
@bot.event
async def on_message_delete(message):
    # log_chan = bot.get_channel(765767364838686731)
    # origin_chan = bot.get_channel(message.channel)
    
    if message.author.bot: return
    else:
            try:
                await log_chan.send(f'**Message deleted in <#{message.channel.id}>**\n**__Content__**:\n{message.content}')
            except NameError:
                print("Must define log channel to show logs!")
        
# Error Handling
@bot.event
async def on_command_error(ctx, error):
    try:
        print(ctx.command.name + " was invoked incorrectly!")
        print(error)
    except AttributeError:
        print(error)
        
# Commands List   
try:    
    # Enabling/Adding commands to the bot!!
    command_list = [ping, coinflip, kick, ban, djinn, set_logs, help, pog, set_welcome]
    for x in command_list:
        bot.add_command(x)
except NameError:
    pass
    

# running the bot
bot.run("NzYwNzQ4NzM5NTgwMTMzNDA3.X3QkeQ.oS-NYPMPgBYuisbSVzWc1PN39Mc")
