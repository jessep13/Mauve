import discord
from discord.ext import commands
import asyncio

# Replace 'token here' with the token

TOKEN = 'token here'

# Just intents stuff

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''You probably shouldn't use this if you don't know what it does.

En masse role replacer made by catgirlandamoth (Sadie). Special thanks to Pea, Diane and all the rest on the rain discord for help!'''

bot = commands.Bot(command_prefix='m;', description=description, intents=intents)

# Sends a message in terminal to let us know the bot should be acceping commands
# Also sets presence. Lavender really is a pretty color.

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Game(name="Lavender is such a pretty color"))

# Very advanced error handling

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRole) and "Role 'MauvePermissions' is required to run this command" in str(error):
        await ctx.send("I'm pretty sure you shouldn't be messing with this <3 (Lacking MauvePermissions role)")

# Basic ping command

@bot.command()
async def ping(ctx):
     await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# Index command: Use caution on large servers. May lag and/or ratelimit
# I have goddamn idea how this works on larger servers. Probably need to put in something that makes this bot ratelimit itself

@bot.command()
@commands.has_role("MauvePermissions")
async def index(ctx):
    # There has got to be a more effecient way to do this
    # When I'm done I really should move all of these up to the top
    roles_to_check = ["LegacyPronoun1", "LegacyPronoun2", "LegacyPronoun3", "LegacyPronoun4", "LegacyPronoun5", "LegacyPronoun6", "LegacyPronoun7", "LegacyPronoun8", "LegacyPronoun9", "LegacyPronoun10", "LegacyPronoun11", "LegacyPronoun12"]
    members_by_role = {role: [] for role in roles_to_check}
    # I don't actually remember why this works
    for member in ctx.guild.members:
        for role in member.roles:
            if role.name in roles_to_check:
                members_by_role[role.name].append(member.name)

    embed = discord.Embed(title="Members with legacy roles", color=discord.Color.purple())
    # Basically just lists all of the users with the roles in question and then also summerizes the number of users with those roles
    # Also a mostly harmless command to make sure this works at scale (god I hope it does)
    for role, members in members_by_role.items():
        total_members = len(members)
        if total_members > 0:
            embed.add_field(name=f"{role} ({total_members} members)", value='\n'.join(members), inline=False)
        else:
            embed.add_field(name=role, value="No members found with this role.", inline=False)

    await ctx.send(embed=embed)

# It cannot be this fucking easy to do this
# Anyway, here we map out the roles we want gone and which ones replace them.
# Maybe move this to the top later?

role_mappings = {
    "LegacyPronoun1": ("NewPronoun1", "color1"),
    "LegacyPronoun2": ("NewPronoun2", "color2"),
    "LegacyPronoun3": ("NewPronoun3", "color3"),
    "LegacyPronoun4": ("NewPronoun4", "color4"),
    "LegacyPronoun5": ("NewPronoun5", "color5"),
    "LegacyPronoun6": ("NewPronoun6", "color6"),
    "LegacyPronoun7": ("NewPronoun7", "color7"),
    "LegacyPronoun8": ("NewPronoun8", "color8"),
    "LegacyPronoun9": ("NewPronoun9", "color9"),
    "LegacyPronoun10": ("NewPronoun10", "color10"),
    "LegacyPronoun11": ("NewPronoun11", "color11"),
    "LegacyPronoun12": ("NewPronoun12", "color12"),
}

# This is the actual replacement script

@bot.command()
@commands.has_role("MauvePermissions")
async def update_roles(ctx):
    confirmation_message = await ctx.send("You have 60 seconds to confirm this command. React with ✅ to confirm or ❌ to cancel.")

    await confirmation_message.add_reaction("✅")
    await confirmation_message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        if str(reaction.emoji) == "✅":
            await ctx.send("Confirmed. This will take a while. I am not kidding.")
            guild = ctx.guild
            for member in guild.members:
                for role_name, (new_role_name1, new_role_name2) in role_mappings.items():
                    role = discord.utils.get(guild.roles, name=role_name)
                    new_role1 = discord.utils.get(guild.roles, name=new_role_name1)
                    new_role2 = discord.utils.get(guild.roles, name=new_role_name2)
                    if role in member.roles:
                        await member.remove_roles(role)
                        await member.add_roles(new_role1, new_role2)
                        print(f"Updated roles for {member.name}: removed {role_name}, added {new_role_name1} and {new_role_name2}")
            await ctx.send("Roles have been updated successfully.")
        else:
            await ctx.send("Canceled. You live to confirm another day :3")
    except asyncio.TimeoutError:
        await ctx.send("Canceled. Timeout.")



# VERY FANCY LOG CODE GOES HERE ONCE I FINISH IT



bot.run(TOKEN)
