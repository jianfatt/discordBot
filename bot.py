import asyncio
import youtube_dl
import discord
import datetime
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
deleting_messages = False
song_queue = []

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

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)

    confirmation_message = await ctx.send(f'Cleared {amount} messages.')
    await asyncio.sleep(2)
    await confirmation_message.delete()


@bot.command()
async def cleartoday(ctx):
    today = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    start_of_day = datetime.datetime(today.year, today.month, today.day)
    end_of_day = start_of_day + datetime.timedelta(days=1)

    await ctx.channel.purge(after=start_of_day, before=end_of_day)

    confirmation_message = await ctx.send(f"Cleared all messages from today's chat history.")
    await asyncio.sleep(2)
    await confirmation_message.delete()


@bot.command()
async def clearall(ctx):
    global delete_messages
    if ctx.author.guild_permissions.manage_messages:
        delete_messages = True
        await ctx.send("Clearing all messages. This may take some time...")

        async for message in ctx.channel.history(limit=None):
            if not delete_messages:
                await ctx.send("Message deletion stopped.")
                return
            await message.delete()

        delete_messages = False
        await ctx.send("All messages have been cleared.")
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def stopclear(ctx):
    global delete_messages
    delete_messages = False
    await ctx.send("Message deletion stopped.")

load_dotenv()
bot.run(os.getenv("TOKEN"))
