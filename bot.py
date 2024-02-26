import asyncio
import youtube_dl
import discord
import datetime
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

load_dotenv()
bot.run(os.getenv("TOKEN"))
