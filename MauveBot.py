import discord
from discord.ext import commands

# Replace 'TOKEN' with your bot's token
TOKEN = 'MTI0OTM3MjM1NDUyNjg0Mjk1MA.GGndBa.e2JBOeNXq4jcEdWeWs6EJZmg3aPTDU5DZ5kLlk'

# Add role names here
role_remove = "LegacyPronoun"
role_add_1 = "NewPronoun"
role_add_2 = "NewColor"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''You probably shouldn't use this if you don't know what it does.

En masse role replacer made by catgirlandamoth (Sadie). Special thanks to Astra and Pea for the help! '''

bot = commands.Bot(command_prefix='m;', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

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
