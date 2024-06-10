import discord
from discord.ext import commands

# Replace 'TOKEN' with your bot's token
TOKEN = 'token'

# Add role names here
role_remove = "LegacyPronoun"
role_add_1 = "NewPronoun"
role_add_2 = "NewColor"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''You probably shouldn't use this if you don't know what it does.

En masse role replacer made by catgirlandamoth (Sadie). Special thanks to Astra, Pea and everyone else for the help! '''

bot = commands.Bot(command_prefix='m;', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRole) and "Role 'MauvePermissions' is required to run this command" in str(error):
        await ctx.send("I'm pretty sure you shouldn't be messing with this <3 (Lacking MauvePermissions role)")

@bot.command()
async def ping(ctx):
     await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(pass_context=True)
@commands.has_role("MauvePermissions")
async def replace (ctx,user:discord.Member):
  role = discord.utils.get(ctx.guild.roles, name=role_remove)
  ra1 = discord.utils.get(ctx.guild.roles, name=role_add_1)
  ra2 = discord.utils.get(ctx.guild.roles, name=role_add_2)

  if role in user.roles:
    await user.remove_roles(role)
    await user.add_roles(ra1)
    await user.add_roles(ra2)

    embed = discord.Embed(title="Role updater", description=f"{user.mention}'s roles have been updated" , color = discord.Color.blue())

    await ctx.send(embed=embed)

  else:
    await ctx.send("User probably doesn't have the role you're trying to replace")
        

bot.run(TOKEN)
