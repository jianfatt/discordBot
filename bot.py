import asyncio
import youtube_dl
import discord
import datetime
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@tasks.loop(seconds=1)
async def send_message(ctx):
    await ctx.channel.send("This is an auto-sent message!")

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def auto_message_start(ctx):
    send_message.start(ctx)
    await ctx.send("Auto-send message function started.")

@bot.command()
async def auto_message_stop(ctx):
    send_message.stop()
    await ctx.send("Auto-send message function stopped.")



load_dotenv()
bot.run(os.getenv("TOKEN"))
