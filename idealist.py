import configparser
import discord
from datetime import datetime
from discord.ext import commands

desc = "Support Bot for Idealist by Dan6erbond"
bot = commands.Bot("$", description=desc)


@bot.event
async def on_command_error(ctx, error):
    print(error)

@bot.event
async def on_member_join(member):
    file = open("bot_intro.txt")
    bot_intro = file.read()
    file.close()
    await bot.get_channel(568012485320245262).send(bot_intro.format(member))


@bot.event
async def on_message(message):
    # check if we're in the introductions channel AND if the message has more than 25 words
    if message.channel.id == 568014240544325632 and len(message.content.split(" ")) > 50:
        keywords = ["skill", "set", "interest", "current", "project", "stuff", "i", "could", "use", "help", "with"]
        for keyword in keywords:
            if keyword not in message.content.lower():
                return
        await message.add_reaction("👍") # add the thumbsup reaction to show the user the introduction is good
        role = message.channel.guild.get_role(568016105147334677)  # get the verified members role
        await message.author.add_roles(role) # assign it to the user
    else:
        await bot.process_commands(message)


@bot.command(help="Submit an idea to #idea-lists through the bot.")
@commands.has_role(568016105147334677)
async def idea(ctx):
    def check(m):
        return m.author.id == ctx.author.id

    await ctx.send("❓ What do you want to call your idea?")
    name = await bot.wait_for("message", check=check)
    name = name.content

    await ctx.send("❓ Summarize your idea in between 20 and 200 words.")
    elevator_pitch = await bot.wait_for("message", check=check)
    elevator_pitch = elevator_pitch.content

    await ctx.send("❓ What phase of the idea are you in?")
    phase = await bot.wait_for("message", check=check)
    phase = phase.content

    await ctx.send("❓ What do you need help with?")
    support = await bot.wait_for("message", check=check)
    support = support.content

    '''
    await bot.get_channel(568044431933046787).send("New idea by {}!\n\n"
                                                   "**Idea Name:** {}\n"
                                                   "**Elevator Pitch:** {}\n"
                                                   "**Phase:** {}\n"
                                                   "**Would like to get support on:** {}".format(ctx.author.mention, name, elevator_pitch, phase, support))
                                                   '''

    embed = discord.Embed(
        colour=discord.Colour(0).from_rgb(52, 152, 219)
    )

    embed.set_author(name="New idea by {}!".format(str(ctx.author)))
    embed.set_footer(text="© Dan6erbond 2019", icon_url=bot.user.avatar_url)

    embed.timestamp = datetime.utcnow()

    embed.add_field(name="Idea Name", value=name, inline=False)
    embed.add_field(name="Elevator Pitch", value=elevator_pitch, inline=False)
    embed.add_field(name="Phase", value=phase, inline=False)
    embed.add_field(name="Would Like To Get Support On", value=support, inline=False)

    await bot.get_channel(568044431933046787).send(embed=embed)

    cat = None
    for category in guild.categories:
        if category.id == 568072269243351050:
            cat = category

    if cat is None:
        return

    await ctx.guild.create_text_channel(name.replace(" ", "-"), category=cat)


@bot.event
async def on_ready():
    print(str(bot.user) + ' is running.')


config = configparser.ConfigParser()
config.read("discord.ini")
bot.run(config["Idealist"]["token"])
