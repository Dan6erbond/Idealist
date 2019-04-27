import configparser
import discord
from discord.ext import commands

desc = "Support Bot for Idealist by Dan6erbond"
bot = commands.Bot("$", description=desc)


@bot.event
async def on_member_join(member):
    file = open("bot_intro.txt")
    bot_intro = file.read()
    file.close()
    await bot.get_channel(568012690761580547).send(bot_intro.format(member))


@bot.event
async def on_message(message):
    # check if we're in the introductions channel AND if the message has more than 25 words
    if message.channel.id == 568014240544325632 and len(message.content.split(" ")) > 25:
        role = message.channel.guild.get_role(568016105147334677) # get the verified members role
        await message.author.add_roles(role) # assign it to the user
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(str(bot.user) + ' is running.')


config = configparser.ConfigParser()
config.read("discord.ini")
bot.run(config["Idealist"]["token"])
